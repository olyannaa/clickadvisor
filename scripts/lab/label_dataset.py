from __future__ import annotations

import argparse
import contextlib
import io
import json
from collections import Counter
from collections.abc import Iterable, Iterator
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from clickadvisor.core.models import Finding, QueryContext
from clickadvisor.rules.base import Rule
from clickadvisor.rules.registry import get_all_rules

DEFAULT_DATASET_PATH = Path("data/ml/expert_dataset/queries.jsonl")
DEFAULT_MANIFEST_PATH = Path("data/ml/expert_dataset/manifest.json")
SEVERITY_ORDER = {"none": 0, "low": 1, "medium": 2, "high": 3}
TIER_ORDER = {
    "none": 0,
    "rag": 1,
    "detector": 2,
    "1A": 3,
    "1B": 4,
    "1C": 5,
    "2": 6,
}


def main() -> None:
    args = parse_args()
    records = load_records(args.dataset)
    rules = get_all_rules()
    counters: Counter[str] = Counter()
    processed = 0

    for index, record in enumerate(records, start=1):
        if args.limit is not None and processed >= args.limit:
            break
        label_record(record, rules, ch_version=args.ch_version)
        processed += 1
        status = str(record.get("rule_labeling_status") or "unknown")
        counters[status] += 1
        risk = str(record.get("rule_risk_label") or "none")
        counters[f"risk:{risk}"] += 1
        if args.progress_every and index % args.progress_every == 0:
            print(f"labeled {index}/{len(records)} records")

    write_records(args.dataset, records)
    update_manifest(args.manifest, counters, processed, args)
    print_summary(counters, processed)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Add ClickAdvisor rule-engine labels to expert dataset JSONL.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET_PATH)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--ch-version", default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--progress-every", type=int, default=1000)
    return parser.parse_args()


def load_records(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {error}") from error
            if not isinstance(payload, dict):
                raise ValueError(f"{path}:{line_number}: record must be a JSON object")
            records.append(payload)
    return records


def write_records(path: Path, records: Iterable[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def label_record(record: dict[str, Any], rules: list[Rule], *, ch_version: str | None) -> None:
    sql = str(record.get("sql") or "")
    context = QueryContext(sql=sql, ch_version=ch_version)
    findings: list[Finding] = []
    errors: list[dict[str, str]] = []
    skipped_version: list[str] = []

    for rule in rules:
        if ch_version and not rule.is_applicable_for_version(ch_version):
            skipped_version.append(rule.rule_id)
            continue
        try:
            with quiet_rule_output():
                finding = rule.check(context)
        except Exception as error:
            errors.append(
                {
                    "rule_id": rule.rule_id,
                    "rule_name": rule.name,
                    "error_type": type(error).__name__,
                    "error": trim_error(str(error)),
                }
            )
            continue
        if finding is not None:
            findings.append(finding)

    finding_rows = [finding_to_dict(finding) for finding in findings if finding.tier != "rag"]
    severities = [str(row["severity"]) for row in finding_rows]
    tiers = [str(row["tier"]) for row in finding_rows]
    max_severity = max(severities, key=lambda item: SEVERITY_ORDER.get(item, -1), default="none")
    max_tier = max(tiers, key=lambda item: TIER_ORDER.get(item, -1), default="none")

    record["rule_findings"] = finding_rows
    record["rule_ids"] = [str(row["rule_id"]) for row in finding_rows]
    record["rule_findings_count"] = len(finding_rows)
    record["rule_max_severity"] = max_severity
    record["rule_max_tier"] = max_tier
    record["rule_risk_label"] = severity_to_risk(max_severity)
    record["rule_labeling_status"] = status_for(findings=finding_rows, errors=errors)
    record["rule_labeling_errors"] = errors
    record["rules_skipped_version"] = sorted(skipped_version)


def finding_to_dict(finding: Finding) -> dict[str, Any]:
    row = asdict(finding)
    return {
        "rule_id": row["rule_id"],
        "rule_name": row["rule_name"],
        "tier": row["tier"],
        "severity": row["severity"],
        "confidence": row["confidence"],
        "description": row["description"],
        "suggestion": row["suggestion"],
        "ch_version_introduced": row["ch_version_introduced"],
    }


def severity_to_risk(severity: str) -> str:
    if severity in {"low", "medium", "high"}:
        return severity
    return "low"


def status_for(*, findings: list[dict[str, Any]], errors: list[dict[str, str]]) -> str:
    if errors and findings:
        return "partial_error"
    if errors:
        return "error"
    return "ok"


def trim_error(text: str) -> str:
    return " ".join(text.strip().split())[:500]


@contextlib.contextmanager
def quiet_rule_output() -> Iterator[None]:
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        yield


def update_manifest(
    path: Path,
    counters: Counter[str],
    processed: int,
    args: argparse.Namespace,
) -> None:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["rule_labeling"] = {
        "created_at": datetime.now(UTC).isoformat(),
        "script": "scripts/lab/label_dataset.py",
        "records_processed": processed,
        "ch_version": args.ch_version,
        "limit": args.limit,
        "counts": dict(sorted(counters.items())),
    }
    path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def print_summary(counters: Counter[str], processed: int) -> None:
    parts = ", ".join(f"{key}={value}" for key, value in sorted(counters.items()))
    print(f"Rule labeling complete: processed={processed}, {parts}")


if __name__ == "__main__":
    main()
