from pathlib import Path

import yaml

from scripts.benchmark.validate_cases import validate_cases


def write_case(path: Path, **overrides: object) -> None:
    payload = {
        "status": "proposed",
        "case_id": "case_001",
        "source": "synthetic",
        "sql": "SELECT 1",
        "schema_files": [],
        "known_issues": [],
        "expected_rules_to_fire": [],
        "expected_findings_count": 0,
        "expected_improvement": None,
        "synthetic_explain_path": None,
        "notes": "TODO",
    }
    payload.update(overrides)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def write_schema(path: Path) -> None:
    path.write_text(Path("benchmark/SCHEMA.yaml").read_text(encoding="utf-8"), encoding="utf-8")


def test_validate_cases_accepts_valid_case(tmp_path: Path) -> None:
    cases_dir = tmp_path / "cases"
    schema_path = tmp_path / "SCHEMA.yaml"
    write_schema(schema_path)
    write_case(cases_dir / "case.yaml")
    assert validate_cases(cases_dir, schema_path) == []


def test_validate_cases_rejects_duplicate_case_ids(tmp_path: Path) -> None:
    cases_dir = tmp_path / "cases"
    schema_path = tmp_path / "SCHEMA.yaml"
    write_schema(schema_path)
    write_case(cases_dir / "a.yaml", case_id="dup_case")
    write_case(cases_dir / "b.yaml", case_id="dup_case")
    issues = validate_cases(cases_dir, schema_path)
    assert any("duplicate case_id" in issue.message for issue in issues)


def test_validate_cases_rejects_missing_required_field(tmp_path: Path) -> None:
    cases_dir = tmp_path / "cases"
    schema_path = tmp_path / "SCHEMA.yaml"
    write_schema(schema_path)
    write_case(cases_dir / "case.yaml")
    payload = yaml.safe_load((cases_dir / "case.yaml").read_text(encoding="utf-8"))
    del payload["source"]
    (cases_dir / "case.yaml").write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    issues = validate_cases(cases_dir, schema_path)
    assert any("required property" in issue.message for issue in issues)


def test_validate_cases_rejects_mismatched_synthetic_source(tmp_path: Path) -> None:
    cases_dir = tmp_path / "cases"
    schema_path = tmp_path / "SCHEMA.yaml"
    write_schema(schema_path)
    write_case(cases_dir / "case.yaml", case_id="synthetic_01", source="tpch")
    issues = validate_cases(cases_dir, schema_path)
    assert any("source=synthetic" in issue.message for issue in issues)


def test_validate_cases_rejects_missing_issue_id(tmp_path: Path) -> None:
    cases_dir = tmp_path / "cases"
    schema_path = tmp_path / "SCHEMA.yaml"
    write_schema(schema_path)
    write_case(
        cases_dir / "case.yaml",
        known_issues=[
            {
                "type": "rule_match",
                "detected_by_rule": "R-001",
                "severity": "high",
                "description": "COUNT(DISTINCT x) can be rewritten.",
            }
        ],
        expected_rules_to_fire=["R-001"],
        expected_findings_count=1,
    )
    issues = validate_cases(cases_dir, schema_path)
    assert any("issue_id" in issue.message for issue in issues)


def test_validate_cases_rejects_mismatched_known_issues_and_rules(tmp_path: Path) -> None:
    cases_dir = tmp_path / "cases"
    schema_path = tmp_path / "SCHEMA.yaml"
    write_schema(schema_path)
    write_case(
        cases_dir / "case.yaml",
        known_issues=[
            {
                "issue_id": "I-1",
                "type": "rule_match",
                "detected_by_rule": "R-001",
                "severity": "high",
                "description": "COUNT(DISTINCT x) can be rewritten.",
            }
        ],
        expected_rules_to_fire=["D-005"],
        expected_findings_count=1,
    )
    issues = validate_cases(cases_dir, schema_path)
    assert any("preserve known_issues" in issue.message for issue in issues)
