from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol

import numpy as np
from scipy import sparse
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix,
    f1_score,
    matthews_corrcoef,
    precision_recall_fscore_support,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

try:
    from catboost import CatBoostClassifier
except ImportError:  # pragma: no cover - catboost is optional.
    CatBoostClassifier = None

DEFAULT_FEATURES_PATH = Path("data/ml/expert_dataset/features/features.jsonl")
DEFAULT_SPLIT_PATH = Path("data/ml/expert_dataset/splits/risk_split_v1.json")
DEFAULT_RESULTS_DIR = Path("eval/results")
LABELS = ["low", "medium", "high"]


class Estimator(Protocol):
    def fit(self, x: Any, y: Any) -> Any: ...

    def predict(self, x: Any) -> Any: ...


def main() -> None:
    args = parse_args()
    rows = load_rows(args.features)
    split = json.loads(args.split.read_text(encoding="utf-8"))
    rows_by_id = {str(row["id"]): row for row in rows}
    model_names = args.models or default_model_names()
    results = run_models(rows_by_id, split, model_names, random_state=args.random_state)
    output_dir = write_results(results, rows_by_id, split, args)
    print_summary(results)
    print(f"Saved risk baseline ladder results to {output_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run risk-label baseline ladder.")
    parser.add_argument("--features", type=Path, default=DEFAULT_FEATURES_PATH)
    parser.add_argument("--split", type=Path, default=DEFAULT_SPLIT_PATH)
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS_DIR)
    parser.add_argument("--run-id", default="risk_baseline_ladder_current")
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument(
        "--models",
        nargs="*",
        default=None,
        help=(
            "Subset of models: dummy_most_frequent dummy_stratified "
            "tfidf_logistic_regression structured_rule_logistic_regression "
            "random_forest_all_features catboost_tabular"
        ),
    )
    return parser.parse_args()


def default_model_names() -> list[str]:
    names = [
        "dummy_most_frequent",
        "dummy_stratified",
        "tfidf_logistic_regression",
        "structured_rule_logistic_regression",
        "random_forest_all_features",
    ]
    if CatBoostClassifier is not None:
        names.append("catboost_tabular")
    return names


def load_rows(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def run_models(
    rows_by_id: dict[str, dict[str, Any]],
    split: dict[str, Any],
    model_names: list[str],
    *,
    random_state: int,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for model_name in model_names:
        fold_metrics: list[dict[str, Any]] = []
        for fold in split["folds"]:
            train_rows = rows_for_ids(rows_by_id, fold["train_ids"])
            valid_rows = rows_for_ids(rows_by_id, fold["valid_ids"])
            fold_metrics.append(
                train_and_evaluate(
                    model_name,
                    train_rows,
                    valid_rows,
                    random_state=random_state,
                    split_name=f"fold_{fold['fold']}",
                )
            )

        train_rows = rows_for_ids(rows_by_id, split["train_ids"])
        test_rows = rows_for_ids(rows_by_id, split["test_ids"])
        holdout_rows = rows_for_ids(rows_by_id, split["holdout_ids"])
        test_metrics = train_and_evaluate(
            model_name,
            train_rows,
            test_rows,
            random_state=random_state,
            split_name="test",
        )
        holdout_metrics = train_and_evaluate(
            model_name,
            train_rows,
            holdout_rows,
            random_state=random_state,
            split_name="holdout",
        )
        results.append(
            {
                "model": model_name,
                "cv": summarize_cv(fold_metrics),
                "folds": fold_metrics,
                "test": test_metrics,
                "holdout": holdout_metrics,
            }
        )
    return results


def rows_for_ids(rows_by_id: dict[str, dict[str, Any]], ids: list[str]) -> list[dict[str, Any]]:
    return [rows_by_id[str(row_id)] for row_id in ids]


def train_and_evaluate(
    model_name: str,
    train_rows: list[dict[str, Any]],
    eval_rows: list[dict[str, Any]],
    *,
    random_state: int,
    split_name: str,
) -> dict[str, Any]:
    x_train, x_eval, estimator = build_model_input(
        model_name,
        train_rows,
        eval_rows,
        random_state=random_state,
    )
    y_train = labels_for(train_rows)
    y_eval = labels_for(eval_rows)
    estimator.fit(x_train, y_train)
    predictions = np.asarray(estimator.predict(x_eval), dtype=object)
    if predictions.ndim > 1:
        predictions = predictions.ravel()
    return metrics_for(y_eval, predictions, split_name=split_name)


def build_model_input(
    model_name: str,
    train_rows: list[dict[str, Any]],
    eval_rows: list[dict[str, Any]],
    *,
    random_state: int,
) -> tuple[Any, Any, Estimator]:
    if model_name == "dummy_most_frequent":
        return (
            np.zeros((len(train_rows), 1)),
            np.zeros((len(eval_rows), 1)),
            DummyClassifier(strategy="most_frequent", random_state=random_state),
        )
    if model_name == "dummy_stratified":
        return (
            np.zeros((len(train_rows), 1)),
            np.zeros((len(eval_rows), 1)),
            DummyClassifier(strategy="stratified", random_state=random_state),
        )
    if model_name == "tfidf_logistic_regression":
        vectorizer = TfidfVectorizer(
            min_df=2,
            max_features=5000,
            ngram_range=(1, 2),
            token_pattern=r"(?u)\b[\w_]{2,}\b|[<>=!*]+",
        )
        x_train = vectorizer.fit_transform(texts_for(train_rows))
        x_eval = vectorizer.transform(texts_for(eval_rows))
        return x_train, x_eval, logistic_regression(random_state)
    if model_name == "structured_rule_logistic_regression":
        x_train, x_eval = numeric_matrices(train_rows, eval_rows)
        estimator = Pipeline(
            [
                ("scale", StandardScaler(with_mean=False)),
                ("model", logistic_regression(random_state)),
            ]
        )
        return x_train, x_eval, estimator
    if model_name == "random_forest_all_features":
        x_train, x_eval = all_feature_matrices(train_rows, eval_rows)
        estimator = RandomForestClassifier(
            n_estimators=220,
            min_samples_leaf=2,
            class_weight="balanced",
            n_jobs=-1,
            random_state=random_state,
        )
        return x_train, x_eval, estimator
    if model_name == "catboost_tabular" and CatBoostClassifier is not None:
        x_train, x_eval = numeric_matrices(train_rows, eval_rows)
        estimator = CatBoostClassifier(
            iterations=160,
            depth=5,
            learning_rate=0.08,
            loss_function="MultiClass",
            auto_class_weights="Balanced",
            random_seed=random_state,
            verbose=False,
            allow_writing_files=False,
        )
        return x_train, x_eval, estimator
    raise ValueError(f"Unknown or unavailable model: {model_name}")


def logistic_regression(random_state: int) -> LogisticRegression:
    return LogisticRegression(
        max_iter=1200,
        class_weight="balanced",
        solver="lbfgs",
        random_state=random_state,
    )


def texts_for(rows: list[dict[str, Any]]) -> list[str]:
    return [str(row.get("normalized_sql") or "") for row in rows]


def labels_for(rows: list[dict[str, Any]]) -> np.ndarray:
    return np.asarray([str(row["target"]) for row in rows], dtype=object)


def numeric_matrices(
    train_rows: list[dict[str, Any]],
    eval_rows: list[dict[str, Any]],
) -> tuple[np.ndarray, np.ndarray]:
    vectorizer = DictVectorizer(sparse=False)
    x_train = vectorizer.fit_transform([row["features"] for row in train_rows])
    x_eval = vectorizer.transform([row["features"] for row in eval_rows])
    return np.asarray(x_train, dtype=float), np.asarray(x_eval, dtype=float)


def all_feature_matrices(
    train_rows: list[dict[str, Any]],
    eval_rows: list[dict[str, Any]],
) -> tuple[sparse.csr_matrix, sparse.csr_matrix]:
    dict_vectorizer = DictVectorizer(sparse=True)
    x_train_num = dict_vectorizer.fit_transform([row["features"] for row in train_rows])
    x_eval_num = dict_vectorizer.transform([row["features"] for row in eval_rows])
    text_vectorizer = TfidfVectorizer(
        min_df=2,
        max_features=5000,
        ngram_range=(1, 2),
        token_pattern=r"(?u)\b[\w_]{2,}\b|[<>=!*]+",
    )
    x_train_text = text_vectorizer.fit_transform(texts_for(train_rows))
    x_eval_text = text_vectorizer.transform(texts_for(eval_rows))
    return (
        sparse.hstack([x_train_num, x_train_text], format="csr"),
        sparse.hstack([x_eval_num, x_eval_text], format="csr"),
    )


def metrics_for(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    *,
    split_name: str,
) -> dict[str, Any]:
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true,
        y_pred,
        labels=LABELS,
        zero_division=0,
    )
    per_label = {
        label: {
            "precision": float(precision[index]),
            "recall": float(recall[index]),
            "f1": float(f1[index]),
            "support": int(support[index]),
        }
        for index, label in enumerate(LABELS)
    }
    matrix = confusion_matrix(y_true, y_pred, labels=LABELS)
    return {
        "split": split_name,
        "records": int(len(y_true)),
        "macro_f1": float(f1_score(y_true, y_pred, labels=LABELS, average="macro", zero_division=0)),
        "mcc": float(matthews_corrcoef(y_true, y_pred)),
        "per_label": per_label,
        "confusion_matrix": matrix.astype(int).tolist(),
        "confusion_matrix_labels": LABELS,
        "true_label_counts": dict(Counter(str(label) for label in y_true).most_common()),
        "predicted_label_counts": dict(Counter(str(label) for label in y_pred).most_common()),
    }


def summarize_cv(fold_metrics: list[dict[str, Any]]) -> dict[str, Any]:
    macro_f1 = np.asarray([fold["macro_f1"] for fold in fold_metrics], dtype=float)
    mcc = np.asarray([fold["mcc"] for fold in fold_metrics], dtype=float)
    per_label: dict[str, dict[str, float]] = {}
    for label in LABELS:
        for metric_name in ("precision", "recall", "f1"):
            values = np.asarray(
                [fold["per_label"][label][metric_name] for fold in fold_metrics],
                dtype=float,
            )
            per_label[f"{label}_{metric_name}_mean"] = {
                "mean": float(values.mean()),
                "std": float(values.std(ddof=0)),
            }
    return {
        "fold_count": len(fold_metrics),
        "macro_f1_mean": float(macro_f1.mean()),
        "macro_f1_std": float(macro_f1.std(ddof=0)),
        "mcc_mean": float(mcc.mean()),
        "mcc_std": float(mcc.std(ddof=0)),
        "per_label": per_label,
    }


def write_results(
    results: list[dict[str, Any]],
    rows_by_id: dict[str, dict[str, Any]],
    split: dict[str, Any],
    args: argparse.Namespace,
) -> Path:
    output_dir = args.results_dir / args.run_id
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "metrics.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    rows = flat_metric_rows(results)
    with (output_dir / "metrics.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else ["model"])
        writer.writeheader()
        writer.writerows(rows)

    metadata = {
        "created_at": datetime.now(UTC).isoformat(),
        "script": "scripts/lab/run_risk_baseline_ladder.py",
        "features_path": str(args.features),
        "split_path": str(args.split),
        "random_state": args.random_state,
        "labels": LABELS,
        "record_count": len(rows_by_id),
        "split_summary": split.get("summary"),
        "methodology_note": (
            "Risk-label baselines are triage models over deterministic rule labels plus "
            "measured metric labels. They are not intended to replace the rule engine."
        ),
        "unavailable_models": {
            "lightgbm": "not installed in current Poetry environment",
            "catboost": None if CatBoostClassifier is not None else "not installed",
        },
    }
    (output_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "summary.md").write_text(render_markdown(results, metadata), encoding="utf-8")
    return output_dir


def flat_metric_rows(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in results:
        cv = result["cv"]
        for split_name in ("test", "holdout"):
            split_metrics = result[split_name]
            rows.append(
                {
                    "model": result["model"],
                    "split": split_name,
                    "cv_macro_f1_mean": cv["macro_f1_mean"],
                    "cv_macro_f1_std": cv["macro_f1_std"],
                    "cv_mcc_mean": cv["mcc_mean"],
                    "cv_mcc_std": cv["mcc_std"],
                    "macro_f1": split_metrics["macro_f1"],
                    "mcc": split_metrics["mcc"],
                    "records": split_metrics["records"],
                    "low_precision": split_metrics["per_label"]["low"]["precision"],
                    "low_recall": split_metrics["per_label"]["low"]["recall"],
                    "medium_precision": split_metrics["per_label"]["medium"]["precision"],
                    "medium_recall": split_metrics["per_label"]["medium"]["recall"],
                    "high_precision": split_metrics["per_label"]["high"]["precision"],
                    "high_recall": split_metrics["per_label"]["high"]["recall"],
                }
            )
    return rows


def render_markdown(results: list[dict[str, Any]], metadata: dict[str, Any]) -> str:
    lines = [
        "# Risk Baseline Ladder",
        "",
        metadata["methodology_note"],
        "",
        "## Cross-Validation Summary",
        "",
        "| Model | CV macro-F1 | CV MCC | Test macro-F1 | Test MCC | Holdout macro-F1 | Holdout MCC |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for result in results:
        cv = result["cv"]
        test = result["test"]
        holdout = result["holdout"]
        lines.append(
            "| "
            f"{result['model']} | "
            f"{cv['macro_f1_mean']:.3f} +/- {cv['macro_f1_std']:.3f} | "
            f"{cv['mcc_mean']:.3f} +/- {cv['mcc_std']:.3f} | "
            f"{test['macro_f1']:.3f} | "
            f"{test['mcc']:.3f} | "
            f"{holdout['macro_f1']:.3f} | "
            f"{holdout['mcc']:.3f} |"
        )
    lines.extend(["", "## High-Class Recall", ""])
    for result in results:
        lines.append(
            "- "
            f"`{result['model']}`: "
            f"test={result['test']['per_label']['high']['recall']:.3f}, "
            f"holdout={result['holdout']['per_label']['high']['recall']:.3f}"
        )
    lines.append("")
    return "\n".join(lines)


def print_summary(results: list[dict[str, Any]]) -> None:
    for result in results:
        cv = result["cv"]
        print(
            f"{result['model']}: "
            f"cv_macro_f1={cv['macro_f1_mean']:.3f}+/-{cv['macro_f1_std']:.3f}, "
            f"test_macro_f1={result['test']['macro_f1']:.3f}, "
            f"holdout_macro_f1={result['holdout']['macro_f1']:.3f}"
        )


if __name__ == "__main__":
    main()
