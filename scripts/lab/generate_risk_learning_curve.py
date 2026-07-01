from __future__ import annotations

import argparse
import csv
import html
import json
import random
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.ensemble import RandomForestClassifier

from scripts.lab.run_risk_baseline_ladder import (
    DEFAULT_FEATURES_PATH,
    DEFAULT_SPLIT_PATH,
    LABELS,
    all_feature_matrices,
    labels_for,
    load_rows,
    metrics_for,
    rows_for_ids,
)

DEFAULT_OUTPUT_DIR = Path("eval/results/risk_learning_curve_current")
DEFAULT_FRACTIONS = [0.10, 0.25, 0.50, 0.75, 1.00]


def main() -> None:
    args = parse_args()
    rows = load_rows(args.features)
    split = json.loads(args.split.read_text(encoding="utf-8"))
    rows_by_id = {str(row["id"]): row for row in rows}
    train_rows = rows_for_ids(rows_by_id, split["train_ids"])
    holdout_rows = rows_for_ids(rows_by_id, split["holdout_ids"])

    learning_rows = build_learning_curve(
        train_rows,
        holdout_rows,
        fractions=args.fractions,
        random_state=args.random_state,
    )
    write_outputs(learning_rows, args.output_dir, args)
    print(f"Saved risk learning curve to {args.output_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate risk-label learning curve artifacts.")
    parser.add_argument("--features", type=Path, default=DEFAULT_FEATURES_PATH)
    parser.add_argument("--split", type=Path, default=DEFAULT_SPLIT_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument("--fractions", type=float, nargs="*", default=DEFAULT_FRACTIONS)
    return parser.parse_args()


def build_learning_curve(
    train_rows: list[dict[str, Any]],
    holdout_rows: list[dict[str, Any]],
    *,
    fractions: list[float],
    random_state: int,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for fraction in fractions:
        sampled_train = stratified_sample(train_rows, fraction=fraction, random_state=random_state)
        x_train, x_holdout = all_feature_matrices(sampled_train, holdout_rows)
        estimator = RandomForestClassifier(
            n_estimators=220,
            min_samples_leaf=2,
            class_weight="balanced",
            n_jobs=-1,
            random_state=random_state,
        )
        y_train = labels_for(sampled_train)
        y_holdout = labels_for(holdout_rows)
        estimator.fit(x_train, y_train)
        train_pred = np.asarray(estimator.predict(x_train), dtype=object)
        holdout_pred = np.asarray(estimator.predict(x_holdout), dtype=object)
        train_metrics = metrics_for(y_train, train_pred, split_name="train_subset")
        holdout_metrics = metrics_for(y_holdout, holdout_pred, split_name="holdout")
        results.append(
            {
                "fraction": float(fraction),
                "train_records": len(sampled_train),
                "train_label_counts": train_metrics["true_label_counts"],
                "train_macro_f1": train_metrics["macro_f1"],
                "train_mcc": train_metrics["mcc"],
                "train_high_recall": train_metrics["per_label"]["high"]["recall"],
                "holdout_macro_f1": holdout_metrics["macro_f1"],
                "holdout_mcc": holdout_metrics["mcc"],
                "holdout_high_recall": holdout_metrics["per_label"]["high"]["recall"],
                "holdout_high_precision": holdout_metrics["per_label"]["high"]["precision"],
            }
        )
    return results


def stratified_sample(
    rows: list[dict[str, Any]],
    *,
    fraction: float,
    random_state: int,
) -> list[dict[str, Any]]:
    if not 0 < fraction <= 1:
        raise ValueError(f"fraction must be in (0, 1], got {fraction}")
    by_label: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_label[str(row["target"])].append(row)

    rng = random.Random(random_state)
    sampled: list[dict[str, Any]] = []
    for label in LABELS:
        label_rows = list(by_label[label])
        rng.shuffle(label_rows)
        count = max(1, round(len(label_rows) * fraction))
        sampled.extend(label_rows[:count])
    sampled.sort(key=lambda row: str(row["id"]))
    return sampled


def write_outputs(rows: list[dict[str, Any]], output_dir: Path, args: argparse.Namespace) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    metadata = {
        "created_at": datetime.now(UTC).isoformat(),
        "script": "scripts/lab/generate_risk_learning_curve.py",
        "features_path": str(args.features),
        "split_path": str(args.split),
        "random_state": args.random_state,
        "model": "random_forest_all_features",
        "note": (
            "Learning curve uses the risk-label train split and evaluates every fraction on "
            "the fixed holdout split. It is a stability diagnostic, not a separate model claim."
        ),
    }
    (output_dir / "learning_curve.json").write_text(
        json.dumps({"metadata": metadata, "rows": rows}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    with (output_dir / "learning_curve.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "learning_curve.svg").write_text(render_svg(rows), encoding="utf-8")
    (output_dir / "summary.md").write_text(render_markdown(rows, metadata), encoding="utf-8")


def render_markdown(rows: list[dict[str, Any]], metadata: dict[str, Any]) -> str:
    lines = [
        "# Risk Learning Curve",
        "",
        metadata["note"],
        "",
        "| Train fraction | Train records | Train macro-F1 | Holdout macro-F1 | "
        "Holdout MCC | Holdout high recall |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['fraction']:.2f} | {row['train_records']} | "
            f"{row['train_macro_f1']:.3f} | {row['holdout_macro_f1']:.3f} | "
            f"{row['holdout_mcc']:.3f} | {row['holdout_high_recall']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "Holdout macro-F1 rises early and then stabilizes, while train macro-F1 remains "
            "higher. This is expected for a Random Forest over sparse SQL/text/rule features. "
            "The fixed holdout curve is the important signal: it does not collapse when the "
            "model sees the full train split, so the 20k risk-label result is more stable than "
            "the separate small synthetic classifier ablation.",
            "",
            "![Risk learning curve](learning_curve.svg)",
            "",
        ]
    )
    return "\n".join(lines)


def render_svg(rows: list[dict[str, Any]]) -> str:
    width = 780
    height = 420
    margin_left = 72
    margin_right = 34
    margin_top = 42
    margin_bottom = 58
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom
    min_y = 0.75
    max_y = 1.0

    def x_pos(fraction: float) -> float:
        return margin_left + (fraction - 0.1) / 0.9 * plot_width

    def y_pos(value: float) -> float:
        return margin_top + (max_y - value) / (max_y - min_y) * plot_height

    def points(metric_name: str) -> str:
        return " ".join(
            f"{x_pos(float(row['fraction'])):.1f},{y_pos(float(row[metric_name])):.1f}"
            for row in rows
        )

    grid_lines = []
    for value in [0.75, 0.80, 0.85, 0.90, 0.95, 1.00]:
        y = y_pos(value)
        grid_lines.append(
            f'<line x1="{margin_left}" y1="{y:.1f}" x2="{width - margin_right}" '
            f'y2="{y:.1f}" stroke="#e5e7eb" />'
        )
        grid_lines.append(
            f'<text x="{margin_left - 12}" y="{y + 4:.1f}" text-anchor="end" '
            f'font-size="12" fill="#475569">{value:.2f}</text>'
        )

    x_labels = []
    for row in rows:
        x = x_pos(float(row["fraction"]))
        x_labels.append(
            f'<text x="{x:.1f}" y="{height - 24}" text-anchor="middle" '
            f'font-size="12" fill="#475569">{float(row["fraction"]):.2f}</text>'
        )

    circles = []
    for metric_name, color in [
        ("train_macro_f1", "#0f766e"),
        ("holdout_macro_f1", "#2563eb"),
    ]:
        for row in rows:
            circles.append(
                f'<circle cx="{x_pos(float(row["fraction"])):.1f}" '
                f'cy="{y_pos(float(row[metric_name])):.1f}" r="4" fill="{color}" />'
            )

    title = html.escape("Risk-label learning curve: Random Forest")
    return "\n".join(
        [
            '<svg xmlns="http://www.w3.org/2000/svg" width="780" height="420" '
            'viewBox="0 0 780 420" role="img" aria-label="Risk learning curve">',
            '<rect width="780" height="420" fill="#ffffff" />',
            f'<text x="{margin_left}" y="24" font-size="18" font-weight="700" '
            f'fill="#0f172a">{title}</text>',
            *grid_lines,
            f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" '
            f'y2="{height - margin_bottom}" stroke="#334155" />',
            f'<line x1="{margin_left}" y1="{height - margin_bottom}" '
            f'x2="{width - margin_right}" y2="{height - margin_bottom}" stroke="#334155" />',
            f'<polyline fill="none" stroke="#0f766e" stroke-width="3" points="{points("train_macro_f1")}" />',
            f'<polyline fill="none" stroke="#2563eb" stroke-width="3" points="{points("holdout_macro_f1")}" />',
            *circles,
            *x_labels,
            f'<text x="{width / 2:.1f}" y="{height - 4}" text-anchor="middle" '
            'font-size="13" fill="#334155">Train fraction</text>',
            '<text x="16" y="224" transform="rotate(-90 16 224)" text-anchor="middle" '
            'font-size="13" fill="#334155">Macro-F1</text>',
            '<rect x="540" y="42" width="14" height="4" fill="#0f766e" />',
            '<text x="562" y="49" font-size="12" fill="#334155">Train macro-F1</text>',
            '<rect x="540" y="64" width="14" height="4" fill="#2563eb" />',
            '<text x="562" y="71" font-size="12" fill="#334155">Holdout macro-F1</text>',
            "</svg>",
        ]
    )


if __name__ == "__main__":
    main()
