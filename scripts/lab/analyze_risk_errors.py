from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.metrics import f1_score, matthews_corrcoef, precision_recall_fscore_support

from scripts.lab.run_risk_baseline_ladder import (
    LABELS,
    build_model_input,
    labels_for,
    rows_for_ids,
)

DEFAULT_DATASET_PATH = Path("data/ml/expert_dataset/queries.jsonl")
DEFAULT_FEATURES_PATH = Path("data/ml/expert_dataset/features/features.jsonl")
DEFAULT_SPLIT_PATH = Path("data/ml/expert_dataset/splits/risk_split_v1.json")
DEFAULT_OUTPUT_DIR = Path("data/ml/expert_dataset/eda/risk_error_analysis")


def main() -> None:
    args = parse_args()
    records_by_id = load_dataset(args.dataset)
    feature_rows = load_jsonl(args.features)
    rows_by_id = {str(row["id"]): row for row in feature_rows}
    split = json.loads(args.split.read_text(encoding="utf-8"))
    train_rows = rows_for_ids(rows_by_id, split["train_ids"])
    holdout_rows = rows_for_ids(rows_by_id, split["holdout_ids"])
    predictions = predict_holdout(args.model, train_rows, holdout_rows, args.random_state)
    enriched_rows = enrich_rows(holdout_rows, predictions, records_by_id)
    report = build_report(enriched_rows, args)
    write_outputs(report, enriched_rows, args)
    print(
        "Wrote risk error analysis: "
        f"holdout={len(enriched_rows)}, model={args.model}, output={args.output_dir}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze holdout risk-label errors by label source.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET_PATH)
    parser.add_argument("--features", type=Path, default=DEFAULT_FEATURES_PATH)
    parser.add_argument("--split", type=Path, default=DEFAULT_SPLIT_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--model", default="random_forest_all_features")
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument("--sample-size", type=int, default=25)
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def load_dataset(path: Path) -> dict[str, dict[str, Any]]:
    return {str(record["id"]): record for record in load_jsonl(path)}


def predict_holdout(
    model_name: str,
    train_rows: list[dict[str, Any]],
    holdout_rows: list[dict[str, Any]],
    random_state: int,
) -> np.ndarray:
    x_train, x_holdout, estimator = build_model_input(
        model_name,
        train_rows,
        holdout_rows,
        random_state=random_state,
    )
    estimator.fit(x_train, labels_for(train_rows))
    predictions = np.asarray(estimator.predict(x_holdout), dtype=object)
    if predictions.ndim > 1:
        predictions = predictions.ravel()
    return predictions


def enrich_rows(
    holdout_rows: list[dict[str, Any]],
    predictions: np.ndarray,
    records_by_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []
    for row, predicted in zip(holdout_rows, predictions, strict=True):
        record = records_by_id[str(row["id"])]
        measured = record.get("measured_metrics") if isinstance(record.get("measured_metrics"), dict) else {}
        enriched.append(
            {
                "id": row["id"],
                "source": row.get("source"),
                "family": row.get("family"),
                "target": row["target"],
                "predicted": str(predicted),
                "correct": row["target"] == str(predicted),
                "label_source": row.get("label_source"),
                "rule_risk_label": row.get("rule_risk_label"),
                "measured_risk_label": row.get("measured_risk_label"),
                "rule_ids": row.get("rule_ids") or [],
                "rule_findings_count": row["features"].get("rule_findings_count"),
                "rule_max_severity": record.get("rule_max_severity"),
                "rule_max_tier": record.get("rule_max_tier"),
                "measured_risk_reasons": record.get("measured_risk_reasons") or [],
                "read_rows": measured.get("read_rows"),
                "query_duration_ms": measured.get("query_duration_ms"),
                "memory_usage": measured.get("memory_usage"),
                "sql_hash": record.get("sql_hash"),
                "sql": record.get("sql"),
            }
        )
    return enriched


def build_report(rows: list[dict[str, Any]], args: argparse.Namespace) -> dict[str, Any]:
    high_fn = [row for row in rows if row["target"] == "high" and row["predicted"] != "high"]
    high_fp = [row for row in rows if row["target"] != "high" and row["predicted"] == "high"]
    slices = {
        "all_holdout": rows,
        "rule_only": [row for row in rows if row["label_source"] == "rule_only"],
        "measured_only": [row for row in rows if row["label_source"] == "measured_only"],
        "both": [row for row in rows if row["label_source"] == "both"],
        "both_high_core": [
            row for row in rows if row["label_source"] == "both" and row["target"] == "high"
        ],
    }
    return {
        "created_at": datetime.now(UTC).isoformat(),
        "script": "scripts/lab/analyze_risk_errors.py",
        "model": args.model,
        "split": "holdout",
        "holdout_records": len(rows),
        "slice_metrics": {
            name: metrics_for_slice(slice_rows)
            for name, slice_rows in slices.items()
            if slice_rows
        },
        "high_false_negatives": summarize_error_set(high_fn),
        "high_false_positives": summarize_error_set(high_fp),
        "top_rule_ids_in_high_fn": dict(rule_counter(high_fn).most_common(20)),
        "top_rule_ids_in_high_fp": dict(rule_counter(high_fp).most_common(20)),
        "rule_family_error_breakdown": rule_family_breakdown(rows),
        "source_family_error_breakdown": source_family_breakdown(rows),
        "label_source_error_breakdown": label_source_breakdown(rows),
        "high_fn_samples": sample_rows(high_fn, args.sample_size),
        "high_fp_samples": sample_rows(high_fp, args.sample_size),
        "interpretation": interpretation_for(rows, high_fn, high_fp),
    }


def metrics_for_slice(rows: list[dict[str, Any]]) -> dict[str, Any]:
    y_true = np.asarray([row["target"] for row in rows], dtype=object)
    y_pred = np.asarray([row["predicted"] for row in rows], dtype=object)
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true,
        y_pred,
        labels=LABELS,
        zero_division=0,
    )
    return {
        "records": len(rows),
        "label_counts": dict(Counter(str(value) for value in y_true).most_common()),
        "predicted_counts": dict(Counter(str(value) for value in y_pred).most_common()),
        "macro_f1": float(f1_score(y_true, y_pred, labels=LABELS, average="macro", zero_division=0)),
        "mcc": safe_mcc(y_true, y_pred),
        "per_label": {
            label: {
                "precision": float(precision[index]),
                "recall": float(recall[index]),
                "f1": float(f1[index]),
                "support": int(support[index]),
            }
            for index, label in enumerate(LABELS)
        },
    }


def safe_mcc(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    if len({str(value) for value in y_true} | {str(value) for value in y_pred}) < 2:
        return 0.0
    return float(matthews_corrcoef(y_true, y_pred))


def summarize_error_set(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "records": len(rows),
        "by_label_source": dict(Counter(str(row["label_source"]) for row in rows).most_common()),
        "by_source": dict(Counter(str(row["source"]) for row in rows).most_common(20)),
        "by_family": dict(Counter(str(row["family"]) for row in rows).most_common(20)),
        "by_rule_risk_label": dict(Counter(str(row["rule_risk_label"]) for row in rows).most_common()),
        "by_measured_risk_label": dict(Counter(str(row["measured_risk_label"]) for row in rows).most_common()),
        "by_predicted_label": dict(Counter(str(row["predicted"]) for row in rows).most_common()),
    }


def rule_counter(rows: list[dict[str, Any]]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for row in rows:
        rule_ids = row.get("rule_ids") or ["<no_rule>"]
        counter.update(str(rule_id) for rule_id in rule_ids)
    return counter


def rule_family_breakdown(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    payload: dict[str, Counter[str]] = {}
    for row in rows:
        families = {rule_family(rule_id) for rule_id in row.get("rule_ids") or ["<no_rule>"]}
        for family in families:
            payload.setdefault(family, Counter())
            payload[family]["records"] += 1
            if not row["correct"]:
                payload[family]["errors"] += 1
            if row["target"] == "high" and row["predicted"] != "high":
                payload[family]["high_fn"] += 1
            if row["target"] != "high" and row["predicted"] == "high":
                payload[family]["high_fp"] += 1
    return {
        family: dict(counter)
        for family, counter in sorted(
            payload.items(),
            key=lambda item: (-item[1]["errors"], item[0]),
        )
    }


def rule_family(rule_id: str) -> str:
    if rule_id.startswith("R-"):
        return "rewrite_rules"
    if rule_id.startswith("D-"):
        return "detectors"
    if rule_id.startswith("E-"):
        return "environment"
    return "no_rule"


def source_family_breakdown(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], Counter[str]] = {}
    for row in rows:
        key = (str(row["source"]), str(row["family"]))
        grouped.setdefault(key, Counter())
        grouped[key]["records"] += 1
        if not row["correct"]:
            grouped[key]["errors"] += 1
        if row["target"] == "high" and row["predicted"] != "high":
            grouped[key]["high_fn"] += 1
        if row["target"] != "high" and row["predicted"] == "high":
            grouped[key]["high_fp"] += 1
    rows_out = []
    for (source, family), counts in grouped.items():
        records = counts["records"]
        errors = counts["errors"]
        rows_out.append(
            {
                "source": source,
                "family": family,
                "records": records,
                "errors": errors,
                "error_rate": errors / records if records else 0.0,
                "high_fn": counts["high_fn"],
                "high_fp": counts["high_fp"],
            }
        )
    return sorted(rows_out, key=lambda row: (-row["errors"], -row["error_rate"], row["source"]))


def label_source_breakdown(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    payload: dict[str, dict[str, Any]] = {}
    for source in sorted({str(row["label_source"]) for row in rows}):
        source_rows = [row for row in rows if str(row["label_source"]) == source]
        errors = [row for row in source_rows if not row["correct"]]
        payload[source] = {
            "records": len(source_rows),
            "errors": len(errors),
            "error_rate": len(errors) / len(source_rows) if source_rows else 0.0,
            "high_fn": sum(1 for row in source_rows if row["target"] == "high" and row["predicted"] != "high"),
            "high_fp": sum(1 for row in source_rows if row["target"] != "high" and row["predicted"] == "high"),
        }
    return payload


def sample_rows(rows: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    samples: list[dict[str, Any]] = []
    for row in rows[:limit]:
        samples.append(
            {
                "id": row["id"],
                "source": row["source"],
                "family": row["family"],
                "target": row["target"],
                "predicted": row["predicted"],
                "label_source": row["label_source"],
                "rule_risk_label": row["rule_risk_label"],
                "measured_risk_label": row["measured_risk_label"],
                "rule_ids": row["rule_ids"][:10],
                "measured_risk_reasons": row["measured_risk_reasons"],
                "read_rows": row["read_rows"],
                "query_duration_ms": row["query_duration_ms"],
                "memory_usage": row["memory_usage"],
                "sql": compact_sql(str(row["sql"] or "")),
            }
        )
    return samples


def compact_sql(sql: str) -> str:
    return " ".join(sql.split())[:500]


def interpretation_for(
    rows: list[dict[str, Any]],
    high_fn: list[dict[str, Any]],
    high_fp: list[dict[str, Any]],
) -> dict[str, str]:
    measured_only = [row for row in rows if row["label_source"] == "measured_only"]
    both = [row for row in rows if row["label_source"] == "both"]
    measured_only_metrics = metrics_for_slice(measured_only) if measured_only else None
    both_metrics = metrics_for_slice(both) if both else None
    measured_f1 = measured_only_metrics["macro_f1"] if measured_only_metrics else 0.0
    both_f1 = both_metrics["macro_f1"] if both_metrics else 0.0
    return {
        "measured_only": (
            f"Measured-only holdout macro-F1 is {measured_f1:.3f}. "
            "This is the key check for whether the model generalizes beyond direct rule-derived labels."
        ),
        "both_core": (
            f"Both-source holdout macro-F1 is {both_f1:.3f}. "
            "This slice is the most reliable core because rule and measured signals agree."
        ),
        "high_fn": (
            f"High false negatives: {len(high_fn)}. These are the highest product-risk misses "
            "and should be inspected before changing thresholds or model choice."
        ),
        "high_fp": (
            f"High false positives: {len(high_fp)}. These show where risk-like features over-prioritize "
            "queries whose final label is low or medium."
        ),
        "runtime_policy": (
            "Production runtime should remain rule-first. ML is useful for triage, prioritization, "
            "and review queues, not as a source of deterministic recommendations."
        ),
    }


def write_outputs(
    report: dict[str, Any],
    rows: list[dict[str, Any]],
    args: argparse.Namespace,
) -> None:
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "error_analysis.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (args.output_dir / "error_analysis.md").write_text(render_markdown(report), encoding="utf-8")
    with (args.output_dir / "holdout_predictions.csv").open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        fieldnames = [
            "id",
            "target",
            "predicted",
            "correct",
            "label_source",
            "rule_risk_label",
            "measured_risk_label",
            "source",
            "family",
            "rule_ids",
            "read_rows",
            "query_duration_ms",
            "memory_usage",
            "sql_hash",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: csv_value(row.get(key)) for key in fieldnames})


def csv_value(value: Any) -> Any:
    if isinstance(value, list):
        return " ".join(str(item) for item in value)
    return value


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Risk Error Analysis",
        "",
        f"- Model: `{report['model']}`",
        f"- Split: `{report['split']}`",
        f"- Holdout records: {report['holdout_records']}",
        "",
        "## Slice Metrics",
        "",
        "| Slice | Records | Macro-F1 | MCC | High precision | High recall | High F1 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name, metrics in report["slice_metrics"].items():
        high = metrics["per_label"]["high"]
        lines.append(
            "| "
            f"{name} | "
            f"{metrics['records']} | "
            f"{metrics['macro_f1']:.3f} | "
            f"{metrics['mcc']:.3f} | "
            f"{high['precision']:.3f} | "
            f"{high['recall']:.3f} | "
            f"{high['f1']:.3f} |"
        )

    lines.extend(["", "## High False Negatives", ""])
    lines.extend(summary_lines(report["high_false_negatives"]))
    lines.extend(["", "## High False Positives", ""])
    lines.extend(summary_lines(report["high_false_positives"]))
    lines.extend(["", "## Label Source Error Breakdown", ""])
    for label_source, payload in report["label_source_error_breakdown"].items():
        lines.append(
            "- "
            f"`{label_source}`: records={payload['records']}, errors={payload['errors']}, "
            f"error_rate={payload['error_rate']:.3f}, high_fn={payload['high_fn']}, "
            f"high_fp={payload['high_fp']}"
        )

    lines.extend(["", "## Top Rules in High FN", ""])
    lines.extend(counter_lines(report["top_rule_ids_in_high_fn"]))
    lines.extend(["", "## Top Rules in High FP", ""])
    lines.extend(counter_lines(report["top_rule_ids_in_high_fp"]))
    lines.extend(["", "## Interpretation", ""])
    for text in report["interpretation"].values():
        lines.append(f"- {text}")
    lines.append("")
    return "\n".join(lines)


def summary_lines(payload: dict[str, Any]) -> list[str]:
    lines = [f"- Records: {payload['records']}"]
    for key in (
        "by_label_source",
        "by_source",
        "by_family",
        "by_rule_risk_label",
        "by_measured_risk_label",
        "by_predicted_label",
    ):
        value = payload[key]
        compact = ", ".join(f"{name}={count}" for name, count in value.items()) or "none"
        lines.append(f"- `{key}`: {compact}")
    return lines


def counter_lines(payload: dict[str, int]) -> list[str]:
    if not payload:
        return ["- none"]
    return [f"- `{name}`: {count}" for name, count in payload.items()]


if __name__ == "__main__":
    main()
