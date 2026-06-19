from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

CATALOG_ROOT = Path("docs/rules/cards")
SCHEMA_PATH = Path("docs/rules/SCHEMA.yaml")
ALLOWED_TIERS = {"1A", "1B", "1C", "2", "3", "detector", "env"}
ALLOWED_STATUSES = {"proposed", "validated", "implemented", "deprecated"}


@dataclass(slots=True)
class ValidationIssue:
    path: Path
    message: str


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("card root must be a YAML object")
    return data


def load_schema(path: Path) -> dict[str, Any]:
    schema = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(schema, dict):
        raise ValueError("schema root must be a YAML object")
    return schema


def jsonschema_issues(card_path: Path, schema: dict[str, Any]) -> list[ValidationIssue]:
    validator = Draft202012Validator(schema)
    issues: list[ValidationIssue] = []
    for error in validator.iter_errors(load_yaml(card_path)):
        path_hint = ".".join(str(part) for part in error.absolute_path) or "root"
        issues.append(ValidationIssue(card_path, f"{path_hint}: {error.message}"))
    return issues


def semantic_issues(card_path: Path) -> list[ValidationIssue]:
    card = load_yaml(card_path)
    issues: list[ValidationIssue] = []

    tier = card.get("tier")
    status = card.get("status")
    opt_in = card.get("opt_in")
    proof = card.get("proof")
    ch_version = card.get("ch_version")

    if tier not in ALLOWED_TIERS:
        issues.append(ValidationIssue(card_path, f"unsupported tier: {tier!r}"))
    if status not in ALLOWED_STATUSES:
        issues.append(ValidationIssue(card_path, f"unsupported status: {status!r}"))
    if tier == "1A" and opt_in is True:
        issues.append(ValidationIssue(card_path, "tier 1A rules must not require opt-in"))
    if tier == "3" and status in {"validated", "implemented"} and not card.get("risks"):
        issues.append(ValidationIssue(card_path, "tier 3 rules must document risks"))
    if tier in {"1A", "1B", "1C"} and status in {"validated", "implemented"} and not proof:
        issues.append(
            ValidationIssue(card_path, "validated or implemented Tier 1 rules must include proof")
        )
    if tier in {"1A", "1B", "1C"}:
        introduced = ch_version.get("introduced") if isinstance(ch_version, dict) else None
        if not isinstance(introduced, str) or not introduced.strip():
            issues.append(
                ValidationIssue(card_path, "Tier 1 rules must define non-null ch_version.introduced")
            )
    return issues


def duplicate_id_issues(paths: list[Path]) -> list[ValidationIssue]:
    seen: dict[str, Path] = {}
    issues: list[ValidationIssue] = []
    for path in paths:
        card = load_yaml(path)
        rule_id = card.get("id")
        if isinstance(rule_id, str):
            if rule_id in seen:
                issues.append(ValidationIssue(path, f"duplicate id with {seen[rule_id]}"))
            else:
                seen[rule_id] = path
    return issues


def validate_catalog(cards_dir: Path, schema_path: Path) -> list[ValidationIssue]:
    schema = load_schema(schema_path)
    paths = sorted(cards_dir.rglob("*.yaml"))
    issues: list[ValidationIssue] = []
    for path in paths:
        issues.extend(jsonschema_issues(path, schema))
        issues.extend(semantic_issues(path))
    issues.extend(duplicate_id_issues(paths))
    return issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate rule catalog YAML cards.")
    parser.add_argument("--cards-dir", type=Path, default=CATALOG_ROOT)
    parser.add_argument("--schema", type=Path, default=SCHEMA_PATH)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    issues = validate_catalog(args.cards_dir, args.schema)
    if issues:
        for issue in issues:
            print(f"{issue.path}: {issue.message}")
        raise SystemExit(1)
    print(f"Validated {len(list(args.cards_dir.rglob('*.yaml')))} rule cards without issues.")


if __name__ == "__main__":
    main()
