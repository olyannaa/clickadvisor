from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

DEFAULT_CASES_DIR = Path("benchmark/cases")
DEFAULT_SCHEMA_PATH = Path("benchmark/SCHEMA.yaml")


@dataclass(slots=True)
class ValidationIssue:
    path: Path
    message: str


def load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("benchmark case root must be a YAML object")
    return payload


def load_schema(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("benchmark schema root must be a YAML object")
    return payload


def validate_case(path: Path, schema: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    validator = Draft202012Validator(schema)
    payload = load_yaml(path)
    for error in validator.iter_errors(payload):
        pointer = ".".join(str(part) for part in error.absolute_path) or "root"
        issues.append(ValidationIssue(path=path, message=f"{pointer}: {error.message}"))
    return issues


def duplicate_id_issues(paths: list[Path]) -> list[ValidationIssue]:
    seen: dict[str, Path] = {}
    issues: list[ValidationIssue] = []
    for path in paths:
        payload = load_yaml(path)
        case_id = payload.get("case_id")
        if isinstance(case_id, str):
            if case_id in seen:
                issues.append(ValidationIssue(path=path, message=f"duplicate case_id with {seen[case_id]}"))
            else:
                seen[case_id] = path
    return issues


def semantic_issues(path: Path) -> list[ValidationIssue]:
    payload = load_yaml(path)
    issues: list[ValidationIssue] = []
    case_id = payload.get("case_id")
    sql = payload.get("sql")
    source = payload.get("source")
    if isinstance(case_id, str) and case_id.startswith("synthetic_") and source != "synthetic":
        issues.append(ValidationIssue(path=path, message="synthetic_* case_id must use source=synthetic"))
    if isinstance(sql, str) and not sql.strip():
        issues.append(ValidationIssue(path=path, message="sql must not be empty"))
    if isinstance(payload.get("schema_files"), list):
        for entry in payload["schema_files"]:
            if not isinstance(entry, str):
                issues.append(ValidationIssue(path=path, message="schema_files entries must be strings"))
    known_issues = payload.get("known_issues")
    if isinstance(known_issues, list):
        issue_ids: set[str] = set()
        for index, issue in enumerate(known_issues, start=1):
            if not isinstance(issue, dict):
                continue
            issue_id = issue.get("issue_id")
            if isinstance(issue_id, str):
                if issue_id in issue_ids:
                    issues.append(ValidationIssue(path=path, message=f"known_issues[{index - 1}].issue_id duplicates {issue_id}"))
                issue_ids.add(issue_id)
        expected_count = payload.get("expected_findings_count")
        if isinstance(expected_count, int) and expected_count != len(known_issues):
            issues.append(
                ValidationIssue(
                    path=path,
                    message="expected_findings_count must match number of known_issues",
                )
            )
    expected_rules = payload.get("expected_rules_to_fire")
    if isinstance(expected_rules, list) and isinstance(known_issues, list):
        matched_rules = [issue.get("detected_by_rule") for issue in known_issues if isinstance(issue, dict)]
        if len(expected_rules) != len(known_issues):
            issues.append(
                ValidationIssue(
                    path=path,
                    message="expected_rules_to_fire length must match number of known_issues",
                )
            )
        elif expected_rules != matched_rules:
            issues.append(
                ValidationIssue(
                    path=path,
                    message="expected_rules_to_fire must preserve known_issues detected_by_rule order",
                )
            )
    return issues


def validate_cases(cases_dir: Path, schema_path: Path) -> list[ValidationIssue]:
    schema = load_schema(schema_path)
    case_paths = sorted(path for path in cases_dir.rglob("*.yaml") if path.name != "README.yaml")
    issues: list[ValidationIssue] = []
    for path in case_paths:
        issues.extend(validate_case(path, schema))
        issues.extend(semantic_issues(path))
    issues.extend(duplicate_id_issues(case_paths))
    return issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate benchmark case YAML files.")
    parser.add_argument("--cases-dir", type=Path, default=DEFAULT_CASES_DIR)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA_PATH)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    issues = validate_cases(args.cases_dir, args.schema)
    if issues:
        for issue in issues:
            print(f"{issue.path}: {issue.message}")
        raise SystemExit(1)
    print(f"Validated {len(list(args.cases_dir.rglob('*.yaml')))} benchmark cases without issues.")


if __name__ == "__main__":
    main()
