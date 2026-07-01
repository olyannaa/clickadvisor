from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

DEFAULT_DATASET_PATH = Path("data/ml/expert_dataset/queries.jsonl")
DEFAULT_MANIFEST_PATH = Path("data/ml/expert_dataset/manifest.json")
RISK_ORDER = {"low": 0, "medium": 1, "high": 2}
METRICS = ("read_rows", "query_duration_ms", "memory_usage")


def main() -> None:
    args = parse_args()
    records = load_records(args.dataset)
    ok_records = [
        record for record in records
        if isinstance(record.get("measured_metrics"), dict)
        and record["measured_metrics"].get("status") == "ok"
    ]
    thresholds = build_thresholds(ok_records)
    counters: Counter[str] = Counter()
    for record in records:
        reconcile_record(record, thresholds, counters)
    write_records(args.dataset, records)
    update_manifest(args.manifest, thresholds, counters)
    print_summary(thresholds, counters)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Add measured and final risk labels to expert dataset.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET_PATH)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH)
    return parser.parse_args()


def load_records(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_records(path: Path, records: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def build_thresholds(ok_records: list[dict[str, Any]]) -> dict[str, Any]:
    metric_values = {metric: values_for(ok_records, metric) for metric in METRICS}
    memory_p90 = percentile(metric_values["memory_usage"], 90)
    memory_non_zero_p90 = percentile(
        [value for value in metric_values["memory_usage"] if value > 0],
        90,
    )
    memory_high = memory_p90
    memory_threshold_source = "p90"
    if memory_high == 0 and memory_non_zero_p90 is not None:
        memory_high = memory_non_zero_p90
        memory_threshold_source = "non_zero_p90"

    return {
        "ok_record_count": len(ok_records),
        "low": {
            "read_rows_lte": percentile(metric_values["read_rows"], 50),
            "query_duration_ms_lte": percentile(metric_values["query_duration_ms"], 50),
        },
        "high": {
            "read_rows_gt": percentile(metric_values["read_rows"], 90),
            "query_duration_ms_gt": percentile(metric_values["query_duration_ms"], 90),
            "memory_usage_gt": memory_high,
            "memory_usage_source": memory_threshold_source,
        },
        "raw_percentiles": {
            metric: {
                "p50": percentile(values, 50),
                "p90": percentile(values, 90),
                "p95": percentile(values, 95),
                "p99": percentile(values, 99),
            }
            for metric, values in metric_values.items()
        },
        "non_zero_memory_p90": memory_non_zero_p90,
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
    return sorted(values)


def percentile(values: list[int], percentile_value: int) -> int | None:
    if not values:
        return None
    if percentile_value <= 0:
        return values[0]
    if percentile_value >= 100:
        return values[-1]
    position = (len(values) - 1) * percentile_value / 100
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return values[int(position)]
    fraction = position - lower
    return round(values[lower] * (1 - fraction) + values[upper] * fraction)


def reconcile_record(
    record: dict[str, Any],
    thresholds: dict[str, Any],
    counters: Counter[str],
) -> None:
    rule_label = normalize_rule_label(str(record.get("rule_risk_label") or "low"))
    measured_label, measured_status, reasons = measured_label_for(record, thresholds)
    if measured_label is None:
        final_label = rule_label
        label_source = "rule_only"
        disagreement = False
    else:
        final_label = max_label(rule_label, measured_label)
        if rule_label == measured_label:
            label_source = "both"
            disagreement = False
        elif final_label == rule_label:
            label_source = "rule_only"
            disagreement = True
        else:
            label_source = "measured_only"
            disagreement = True

    record["measured_risk_label"] = measured_label
    record["measured_risk_status"] = measured_status
    record["measured_risk_reasons"] = reasons
    record["final_risk_label"] = final_label
    record["label_source"] = label_source
    record["risk_signal_disagreement"] = disagreement

    counters[f"measured:{measured_label or 'none'}"] += 1
    counters[f"final:{final_label}"] += 1
    counters[f"label_source:{label_source}"] += 1
    counters[f"measured_status:{measured_status}"] += 1
    if disagreement:
        counters["risk_signal_disagreement"] += 1


def measured_label_for(
    record: dict[str, Any],
    thresholds: dict[str, Any],
) -> tuple[str | None, str, list[str]]:
    measured = record.get("measured_metrics")
    if not isinstance(measured, dict) or measured.get("status") != "ok":
        return None, "not_applicable", []

    read_rows = int(measured.get("read_rows") or 0)
    duration = int(measured.get("query_duration_ms") or 0)
    memory = int(measured.get("memory_usage") or 0)
    high_thresholds = thresholds["high"]
    low_thresholds = thresholds["low"]
    high_reasons: list[str] = []
    if high_thresholds["read_rows_gt"] is not None and read_rows > high_thresholds["read_rows_gt"]:
        high_reasons.append("read_rows_gt_p90")
    if (
        high_thresholds["query_duration_ms_gt"] is not None
        and duration > high_thresholds["query_duration_ms_gt"]
    ):
        high_reasons.append("query_duration_ms_gt_p90")
    if high_thresholds["memory_usage_gt"] is not None and memory > high_thresholds["memory_usage_gt"]:
        high_reasons.append(f"memory_usage_gt_{high_thresholds['memory_usage_source']}")
    if high_reasons:
        return "high", "ok", high_reasons
    if (
        low_thresholds["read_rows_lte"] is not None
        and low_thresholds["query_duration_ms_lte"] is not None
        and read_rows <= low_thresholds["read_rows_lte"]
        and duration <= low_thresholds["query_duration_ms_lte"]
    ):
        return "low", "ok", ["read_rows_lte_p50", "query_duration_ms_lte_p50"]
    return "medium", "ok", ["between_p50_and_p90"]


def normalize_rule_label(label: str) -> str:
    return label if label in RISK_ORDER else "low"


def max_label(left: str, right: str) -> str:
    return left if RISK_ORDER[left] >= RISK_ORDER[right] else right


def update_manifest(
    path: Path,
    thresholds: dict[str, Any],
    counters: Counter[str],
) -> None:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["risk_reconciliation"] = {
        "created_at": datetime.now(UTC).isoformat(),
        "script": "scripts/lab/reconcile_risk_labels.py",
        "thresholds": thresholds,
        "counts": dict(sorted(counters.items())),
        "rule": "final_risk_label = max(rule_risk_label, measured_risk_label); non-ok measured records use rule_only.",
    }
    path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def print_summary(thresholds: dict[str, Any], counters: Counter[str]) -> None:
    parts = ", ".join(f"{key}={value}" for key, value in sorted(counters.items()))
    print(f"Risk reconciliation complete: thresholds={thresholds}; {parts}")


if __name__ == "__main__":
    main()
