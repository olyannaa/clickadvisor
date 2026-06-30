"""Extract QueryFeatures from all synthetic_expanded benchmark cases and save to JSONL.

Output format (one JSON object per line):
{
    "case_id": "synthetic_expanded_r001_001",
    "features": {"has_count_distinct": 1, ...},
    "labels": ["exact_count_distinct_specialization", "approx_count_distinct_advisory"],
    "split": "train"
}

Labels come from known_issues[].type (semantic problem-type labels, not rule IDs).
Split assignment comes from benchmark/splits/synthetic_expanded_v1.yaml.
Negative cases have labels=[].
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from clickadvisor.ml.features import FeatureExtractor  # noqa: E402

CASES_DIR = REPO_ROOT / "benchmark" / "cases" / "synthetic_expanded"
SPLIT_PATH = REPO_ROOT / "benchmark" / "splits" / "synthetic_expanded_v1.yaml"
OUTPUT_PATH = REPO_ROOT / "data" / "ml" / "features_dataset.jsonl"


def load_split(split_path: Path) -> dict[str, str]:
    """Return {case_id: "train"|"test"} mapping."""
    payload = yaml.safe_load(split_path.read_text(encoding="utf-8"))
    mapping: dict[str, str] = {}
    for case_id in payload.get("train_case_ids", []):
        mapping[case_id] = "train"
    for case_id in payload.get("test_case_ids", []):
        mapping[case_id] = "test"
    return mapping


def main() -> None:
    extractor = FeatureExtractor()
    split_map = load_split(SPLIT_PATH)

    case_files = sorted(CASES_DIR.glob("*.yaml"))
    if not case_files:
        print(f"No YAML files found in {CASES_DIR}", file=sys.stderr)
        sys.exit(1)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    label_set: set[str] = set()
    train_count = 0
    test_count = 0
    skipped = 0

    with OUTPUT_PATH.open("w", encoding="utf-8") as out:
        for path in case_files:
            payload = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                skipped += 1
                continue

            case_id: str = payload.get("case_id", path.stem)
            sql: str = payload.get("sql", "")
            if not sql:
                skipped += 1
                continue

            known_issues = payload.get("known_issues") or []
            labels: list[str] = [
                issue["type"]
                for issue in known_issues
                if isinstance(issue, dict) and "type" in issue
            ]
            label_set.update(labels)

            split = split_map.get(case_id, "unknown")

            features = extractor.extract(sql).to_vector()

            record = {
                "case_id": case_id,
                "features": features,
                "labels": labels,
                "split": split,
            }
            out.write(json.dumps(record, ensure_ascii=False) + "\n")

            if split == "train":
                train_count += 1
            elif split == "test":
                test_count += 1

    total = train_count + test_count + skipped
    print(f"Written {total} records to {OUTPUT_PATH}")
    print(f"  train: {train_count}, test: {test_count}, skipped/unknown: {skipped}")
    print(f"  unique labels ({len(label_set)}):")
    for label in sorted(label_set):
        print(f"    {label}")


if __name__ == "__main__":
    main()
