from __future__ import annotations

import argparse
import contextlib
import io
import json
from collections import Counter
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import sqlglot

DEFAULT_DATASET_PATH = Path("data/ml/expert_dataset/queries.jsonl")
DEFAULT_MANIFEST_PATH = Path("data/ml/expert_dataset/manifest.json")
MIN_RECORDS = 2000
MIN_REAL_RECORDS = 1000
MIN_SYNTHETIC_RECORDS = 500
REQUIRED_RISK_LABELS = {"no_known_risk", "low", "medium", "high"}
REQUIRED_CLASS_LABELS = {"low", "medium", "high"}
REQUIRED_LABEL_SOURCES = {"both", "rule_only", "measured_only"}


def main() -> None:
    args = parse_args()
    records = load_records(args.dataset)
    manifest = load_manifest(args.manifest)
    issues = validate_records(records, manifest)
    if issues:
        for issue in issues:
            print(issue)
        raise SystemExit(1)
    risks = Counter(record["risk"]["label"] for record in records)
    print(
        "Validated expert dataset: "
        f"{len(records)} records, "
        f"{sum(1 for record in records if not record['is_synthetic'])} real, "
        f"{sum(1 for record in records if record['is_synthetic'])} synthetic, "
        f"risk distribution={dict(sorted(risks.items()))}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the ClickAdvisor expert SQL dataset.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET_PATH)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH)
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


def load_manifest(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("manifest must be a JSON object")
    return payload


def validate_records(records: list[dict[str, Any]], manifest: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    ids: set[str] = set()
    hashes: set[str] = set()
    risks: Counter[str] = Counter()
    real_count = 0
    synthetic_count = 0
    require_rule_labeling = isinstance(manifest.get("rule_labeling"), dict)
    require_reconciliation = isinstance(manifest.get("risk_reconciliation"), dict)

    if len(records) < MIN_RECORDS:
        issues.append(f"dataset has {len(records)} records, expected at least {MIN_RECORDS}")

    for index, record in enumerate(records, start=1):
        prefix = f"record {index}"
        for key in [
            "id",
            "sql_hash",
            "sql",
            "source",
            "family",
            "license_class",
            "origin",
            "is_synthetic",
            "labels",
            "risk",
            "features",
            "label_method",
        ]:
            if key not in record:
                issues.append(f"{prefix}: missing {key}")
        if not isinstance(record.get("id"), str) or not record["id"]:
            issues.append(f"{prefix}: id must be a non-empty string")
        elif record["id"] in ids:
            issues.append(f"{prefix}: duplicate id {record['id']}")
        else:
            ids.add(record["id"])

        if not isinstance(record.get("sql_hash"), str) or not record["sql_hash"]:
            issues.append(f"{prefix}: sql_hash must be a non-empty string")
        elif record["sql_hash"] in hashes:
            issues.append(f"{prefix}: duplicate sql_hash {record['sql_hash']}")
        else:
            hashes.add(record["sql_hash"])

        sql = record.get("sql")
        if not isinstance(sql, str) or len(sql.strip()) < 8:
            issues.append(f"{prefix}: sql must be non-empty")
        else:
            try:
                with quiet_sqlglot():
                    sqlglot.parse_one(sql, dialect="clickhouse")
            except sqlglot.errors.ParseError as error:
                issues.append(f"{prefix}: sqlglot parse error: {error}")

        if record.get("is_synthetic") is True:
            synthetic_count += 1
            origin = record.get("origin")
            if not isinstance(origin, dict) or not origin.get("synthesis_method"):
                issues.append(f"{prefix}: synthetic record must include origin.synthesis_method")
        elif record.get("is_synthetic") is False:
            real_count += 1
        else:
            issues.append(f"{prefix}: is_synthetic must be boolean")

        labels = record.get("labels")
        if not isinstance(labels, list):
            issues.append(f"{prefix}: labels must be a list")
        elif any(not isinstance(label, dict) or "rule_id" not in label for label in labels):
            issues.append(f"{prefix}: labels must contain rule objects")

        risk = record.get("risk")
        if not isinstance(risk, dict) or risk.get("label") not in REQUIRED_RISK_LABELS:
            issues.append(f"{prefix}: risk.label must be one of {sorted(REQUIRED_RISK_LABELS)}")
        else:
            risks.update([risk["label"]])
            if not isinstance(risk.get("score"), int):
                issues.append(f"{prefix}: risk.score must be an integer")

        features = record.get("features")
        if not isinstance(features, dict) or not features:
            issues.append(f"{prefix}: features must be a non-empty object")

        if require_rule_labeling:
            validate_rule_label_fields(prefix, record, issues)
        if require_reconciliation:
            validate_reconciled_label_fields(prefix, record, issues)

    if real_count < MIN_REAL_RECORDS:
        issues.append(f"dataset has {real_count} real records, expected at least {MIN_REAL_RECORDS}")
    if synthetic_count < MIN_SYNTHETIC_RECORDS:
        issues.append(
            f"dataset has {synthetic_count} synthetic records, expected at least {MIN_SYNTHETIC_RECORDS}"
        )
    missing_risks = REQUIRED_RISK_LABELS - set(risks)
    if missing_risks:
        issues.append(f"dataset is missing risk labels: {sorted(missing_risks)}")

    if manifest.get("record_count") != len(records):
        issues.append("manifest record_count does not match JSONL")
    if manifest.get("real_record_count") != real_count:
        issues.append("manifest real_record_count does not match JSONL")
    if manifest.get("synthetic_record_count") != synthetic_count:
        issues.append("manifest synthetic_record_count does not match JSONL")

    return issues


def validate_rule_label_fields(prefix: str, record: dict[str, Any], issues: list[str]) -> None:
    if not isinstance(record.get("rule_findings"), list):
        issues.append(f"{prefix}: rule_findings must be a list")
    if not isinstance(record.get("rule_ids"), list):
        issues.append(f"{prefix}: rule_ids must be a list")
    if not isinstance(record.get("rule_findings_count"), int):
        issues.append(f"{prefix}: rule_findings_count must be an integer")
    if record.get("rule_risk_label") not in REQUIRED_CLASS_LABELS:
        issues.append(f"{prefix}: rule_risk_label must be one of {sorted(REQUIRED_CLASS_LABELS)}")
    if record.get("rule_max_severity") not in REQUIRED_CLASS_LABELS | {"none"}:
        issues.append(f"{prefix}: rule_max_severity must be low/medium/high/none")
    if not isinstance(record.get("rule_labeling_errors"), list):
        issues.append(f"{prefix}: rule_labeling_errors must be a list")
    if not isinstance(record.get("rules_skipped_version"), list):
        issues.append(f"{prefix}: rules_skipped_version must be a list")


def validate_reconciled_label_fields(
    prefix: str,
    record: dict[str, Any],
    issues: list[str],
) -> None:
    measured_label = record.get("measured_risk_label")
    if measured_label is not None and measured_label not in REQUIRED_CLASS_LABELS:
        issues.append(f"{prefix}: measured_risk_label must be low/medium/high/null")
    if record.get("final_risk_label") not in REQUIRED_CLASS_LABELS:
        issues.append(f"{prefix}: final_risk_label must be one of {sorted(REQUIRED_CLASS_LABELS)}")
    if record.get("label_source") not in REQUIRED_LABEL_SOURCES:
        issues.append(f"{prefix}: label_source must be one of {sorted(REQUIRED_LABEL_SOURCES)}")
    if not isinstance(record.get("risk_signal_disagreement"), bool):
        issues.append(f"{prefix}: risk_signal_disagreement must be boolean")
    if not isinstance(record.get("measured_risk_reasons"), list):
        issues.append(f"{prefix}: measured_risk_reasons must be a list")


@contextlib.contextmanager
def quiet_sqlglot() -> Iterator[None]:
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        yield


if __name__ == "__main__":
    main()
