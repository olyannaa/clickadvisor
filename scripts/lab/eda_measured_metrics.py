from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

DEFAULT_DATASET_PATH = Path("data/ml/expert_dataset/queries.jsonl")
DEFAULT_OUTPUT_DIR = Path("data/ml/expert_dataset/eda")
METRICS = ("read_rows", "query_duration_ms", "memory_usage")
PERCENTILES = (0, 1, 5, 10, 25, 50, 75, 90, 95, 99, 100)


def main() -> None:
    args = parse_args()
    records = load_records(args.dataset)
    ok_records = [
        record for record in records
        if isinstance(record.get("measured_metrics"), dict)
        and record["measured_metrics"].get("status") == "ok"
    ]
    report = build_report(records, ok_records)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "measured_metrics_eda.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (args.output_dir / "measured_metrics_eda.md").write_text(
        render_markdown(report),
        encoding="utf-8",
    )
    print(f"Wrote measured metrics EDA for {len(ok_records)} ok records to {args.output_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize measured ClickHouse replay metrics.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def load_records(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def build_report(records: list[dict[str, Any]], ok_records: list[dict[str, Any]]) -> dict[str, Any]:
    status_counts = Counter(
        (record.get("measured_metrics") or {}).get("status", "missing")
        for record in records
    )
    source_counts = Counter(str(record.get("source") or "unknown") for record in ok_records)
    family_counts = Counter(str(record.get("family") or "unknown") for record in ok_records)

    metrics = {
        metric: metric_summary(values_for(ok_records, metric))
        for metric in METRICS
    }
    return {
        "record_count": len(records),
        "ok_record_count": len(ok_records),
        "status_counts": dict(sorted(status_counts.items())),
        "ok_source_counts": dict(source_counts.most_common()),
        "ok_family_counts": dict(family_counts.most_common()),
        "metrics": metrics,
        "notes": [
            "Histograms use log10(value + 1) buckets because replay latency and scanned rows are heavy-tailed.",
            "When an all-record percentile is zero, use non_zero_percentiles for threshold design.",
        ],
    }


def values_for(records: list[dict[str, Any]], metric: str) -> list[int]:
    values: list[int] = []
    for record in records:
        measured = record["measured_metrics"]
        value = measured.get(metric)
        if isinstance(value, int):
            values.append(value)
        elif isinstance(value, float):
            values.append(int(value))
    return values


def metric_summary(values: list[int]) -> dict[str, Any]:
    sorted_values = sorted(values)
    non_zero = [value for value in sorted_values if value > 0]
    return {
        "count": len(sorted_values),
        "zero_count": sum(1 for value in sorted_values if value == 0),
        "non_zero_count": len(non_zero),
        "percentiles": {
            f"p{percentile}": percentile_value(sorted_values, percentile)
            for percentile in PERCENTILES
        },
        "non_zero_percentiles": {
            f"p{percentile}": percentile_value(non_zero, percentile)
            for percentile in PERCENTILES
        },
        "log10_histogram": log_histogram(sorted_values),
    }


def percentile_value(values: list[int], percentile: int) -> int | None:
    if not values:
        return None
    if percentile <= 0:
        return values[0]
    if percentile >= 100:
        return values[-1]
    position = (len(values) - 1) * percentile / 100
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return values[int(position)]
    fraction = position - lower
    return round(values[lower] * (1 - fraction) + values[upper] * fraction)


def log_histogram(values: list[int], buckets: int = 12) -> list[dict[str, Any]]:
    if not values:
        return []
    transformed = [math.log10(value + 1) for value in values]
    lo = min(transformed)
    hi = max(transformed)
    if lo == hi:
        return [{"range": f"{lo:.2f}..{hi:.2f}", "count": len(values), "bar": "#"}]
    width = (hi - lo) / buckets
    counts = [0 for _ in range(buckets)]
    for value in transformed:
        index = min(int((value - lo) / width), buckets - 1)
        counts[index] += 1
    max_count = max(counts) or 1
    rows: list[dict[str, Any]] = []
    for index, count in enumerate(counts):
        start = lo + index * width
        end = start + width
        rows.append(
            {
                "range": f"{start:.2f}..{end:.2f}",
                "count": count,
                "bar": "#" * max(1, round(count / max_count * 40)) if count else "",
            }
        )
    return rows


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Measured Metrics EDA",
        "",
        f"- Total records: {report['record_count']}",
        f"- `measured_metrics.status = ok`: {report['ok_record_count']}",
        f"- Status counts: `{report['status_counts']}`",
        "",
        "## Percentiles",
        "",
        "| Metric | zero | non-zero | P50 | P90 | P95 | P99 | max | non-zero P90 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    metrics = report["metrics"]
    for metric in METRICS:
        summary = metrics[metric]
        percentiles = summary["percentiles"]
        non_zero_percentiles = summary["non_zero_percentiles"]
        lines.append(
            "| "
            f"{metric} | "
            f"{summary['zero_count']} | "
            f"{summary['non_zero_count']} | "
            f"{percentiles['p50']} | "
            f"{percentiles['p90']} | "
            f"{percentiles['p95']} | "
            f"{percentiles['p99']} | "
            f"{percentiles['p100']} | "
            f"{non_zero_percentiles['p90']} |"
        )
    lines.extend(["", "## Log10 Histograms", ""])
    for metric in METRICS:
        lines.extend([f"### {metric}", "", "```text"])
        for row in metrics[metric]["log10_histogram"]:
            lines.append(f"{row['range']:>13} | {row['count']:>5} {row['bar']}")
        lines.extend(["```", ""])
    lines.extend(["## Source Breakdown", ""])
    for source, count in report["ok_source_counts"].items():
        lines.append(f"- `{source}`: {count}")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
