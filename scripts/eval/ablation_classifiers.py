from __future__ import annotations

import argparse
import csv
import json
from datetime import UTC, datetime
from pathlib import Path

from rich.console import Console
from rich.table import Table

from clickadvisor.ml.classifier import ClassifierMetrics, evaluate_classifiers
from clickadvisor.ml.dataset import build_examples, load_benchmark_cases, load_split, split_examples

DEFAULT_CASES_DIR = Path("benchmark/cases/synthetic_expanded")
DEFAULT_SPLIT_PATH = Path("benchmark/splits/synthetic_expanded_v1.yaml")
DEFAULT_RESULTS_DIR = Path("eval/results")

console = Console()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run classifier ablation on synthetic benchmark features.")
    parser.add_argument("--cases-dir", type=Path, default=DEFAULT_CASES_DIR)
    parser.add_argument("--split-path", type=Path, default=DEFAULT_SPLIT_PATH)
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS_DIR)
    parser.add_argument("--run-id", default=None, help="Stable output directory name. Defaults to timestamp.")
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument(
        "--models",
        nargs="*",
        default=None,
        help="Subset of models: logistic_regression random_forest catboost.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cases = load_benchmark_cases(args.cases_dir)
    examples = build_examples(cases)
    train_examples, test_examples = split_examples(examples, load_split(args.split_path))
    metrics = evaluate_classifiers(
        train_examples,
        test_examples,
        random_state=args.random_state,
        model_names=args.models,
    )

    print_results(metrics)
    output_dir = write_results(
        metrics,
        args.results_dir,
        args.run_id,
        cases_dir=args.cases_dir,
        split_path=args.split_path,
        random_state=args.random_state,
    )
    console.print(f"Saved classifier ablation results to {output_dir}")


def print_results(metrics: list[ClassifierMetrics]) -> None:
    table = Table(title="Classifier ablation")
    table.add_column("Model")
    table.add_column("Train F1 macro", justify="right")
    table.add_column("Train F1 micro", justify="right")
    table.add_column("Test F1 macro", justify="right")
    table.add_column("Test F1 micro", justify="right")
    table.add_column("Precision", justify="right")
    table.add_column("Recall", justify="right")

    for item in metrics:
        table.add_row(
            item.model,
            f"{item.train_f1_macro:.3f}",
            f"{item.train_f1_micro:.3f}",
            f"{item.test_f1_macro:.3f}",
            f"{item.test_f1_micro:.3f}",
            f"{item.test_precision_macro:.3f}",
            f"{item.test_recall_macro:.3f}",
        )
    console.print(table)


def write_results(
    metrics: list[ClassifierMetrics],
    results_dir: Path,
    run_id: str | None,
    *,
    cases_dir: Path,
    split_path: Path,
    random_state: int,
) -> Path:
    run_name = run_id or f"classifier_ablation_{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}"
    output_dir = results_dir / run_name
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = [metric.as_row() for metric in metrics]
    (output_dir / "metrics.json").write_text(
        json.dumps(rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (output_dir / "metadata.json").write_text(
        json.dumps(
            {
                "experiment": "classifier_ablation",
                "cases_dir": str(cases_dir),
                "split_path": str(split_path),
                "random_state": random_state,
                "created_at": datetime.now(UTC).isoformat(),
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    with (output_dir / "metrics.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else ["model"])
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "summary.md").write_text(markdown_summary(metrics), encoding="utf-8")
    return output_dir


def markdown_summary(metrics: list[ClassifierMetrics]) -> str:
    lines = [
        "# Classifier Ablation",
        "",
        "| Model | Train F1 macro | Train F1 micro | Test F1 macro | Test F1 micro | Precision | Recall |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for item in metrics:
        lines.append(
            "| "
            f"{item.model} | "
            f"{item.train_f1_macro:.3f} | "
            f"{item.train_f1_micro:.3f} | "
            f"{item.test_f1_macro:.3f} | "
            f"{item.test_f1_micro:.3f} | "
            f"{item.test_precision_macro:.3f} | "
            f"{item.test_recall_macro:.3f} |"
        )
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
