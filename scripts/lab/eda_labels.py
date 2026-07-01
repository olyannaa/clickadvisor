from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

DEFAULT_DATASET_PATH = Path("data/ml/expert_dataset/queries.jsonl")
DEFAULT_OUTPUT_DIR = Path("data/ml/expert_dataset/eda")
LABEL_FIELDS = ("rule_risk_label", "measured_risk_label", "final_risk_label", "label_source")


def main() -> None:
    args = parse_args()
    records = load_records(args.dataset)
    report = build_report(records)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "label_eda.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (args.output_dir / "label_eda.md").write_text(render_markdown(report), encoding="utf-8")
    print(f"Wrote label EDA for {len(records)} records to {args.output_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize reconciled labels and rule co-occurrence.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def load_records(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def build_report(records: list[dict[str, Any]]) -> dict[str, Any]:
    label_counts = {
        field: dict(Counter(str(record.get(field)) for record in records).most_common())
        for field in LABEL_FIELDS
    }
    source_by_final: dict[str, Counter[str]] = defaultdict(Counter)
    family_by_final: dict[str, Counter[str]] = defaultdict(Counter)
    rules_by_final: dict[str, Counter[str]] = defaultdict(Counter)
    rule_pairs: Counter[str] = Counter()
    high_examples: list[dict[str, Any]] = []

    for record in records:
        final_label = str(record.get("final_risk_label") or "unknown")
        source_by_final[final_label].update([str(record.get("source") or "unknown")])
        family_by_final[final_label].update([str(record.get("family") or "unknown")])
        rule_ids = [str(rule_id) for rule_id in record.get("rule_ids") or []]
        rules_by_final[final_label].update(rule_ids)
        for left_index, left in enumerate(rule_ids):
            for right in rule_ids[left_index + 1:]:
                rule_pairs.update([" + ".join(sorted((left, right)))])
        if final_label == "high" and len(high_examples) < 20:
            high_examples.append(
                {
                    "id": record.get("id"),
                    "source": record.get("source"),
                    "rule_risk_label": record.get("rule_risk_label"),
                    "measured_risk_label": record.get("measured_risk_label"),
                    "label_source": record.get("label_source"),
                    "rule_ids": rule_ids[:8],
                    "measured_risk_reasons": record.get("measured_risk_reasons"),
                }
            )

    return {
        "record_count": len(records),
        "label_counts": label_counts,
        "source_by_final": nested_counter(source_by_final),
        "family_by_final": nested_counter(family_by_final),
        "top_rules_by_final": {
            label: dict(counter.most_common(25))
            for label, counter in sorted(rules_by_final.items())
        },
        "top_rule_pairs": dict(rule_pairs.most_common(30)),
        "high_examples": high_examples,
    }


def nested_counter(payload: dict[str, Counter[str]]) -> dict[str, dict[str, int]]:
    return {label: dict(counter.most_common()) for label, counter in sorted(payload.items())}


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Label EDA", "", f"- Records: {report['record_count']}", ""]
    lines.extend(["## Label Counts", ""])
    for field, counts in report["label_counts"].items():
        lines.append(f"### {field}")
        for label, count in counts.items():
            lines.append(f"- `{label}`: {count}")
        lines.append("")

    lines.extend(["## Source by Final Label", ""])
    for label, counts in report["source_by_final"].items():
        lines.append(f"### {label}")
        for source, count in counts.items():
            lines.append(f"- `{source}`: {count}")
        lines.append("")

    lines.extend(["## Top Rules by Final Label", ""])
    for label, counts in report["top_rules_by_final"].items():
        lines.append(f"### {label}")
        for rule_id, count in counts.items():
            lines.append(f"- `{rule_id}`: {count}")
        lines.append("")

    lines.extend(["## Top Rule Pairs", ""])
    for pair, count in report["top_rule_pairs"].items():
        lines.append(f"- `{pair}`: {count}")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
