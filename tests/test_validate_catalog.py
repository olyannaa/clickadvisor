from pathlib import Path

import yaml

from scripts.rules.validate_catalog import validate_catalog


def write_card(path: Path, **overrides: object) -> None:
    card = {
        "id": "R-901",
        "name": "sample_rule",
        "tier": "1A",
        "category": "predicate_canonicalization",
        "status": "proposed",
        "statement": "TODO",
        "preconditions": {"syntactic": [], "semantic": [], "data": []},
        "proof": {"status": "TODO", "notes": "TODO"},
        "ch_version": {"introduced": None, "deprecated": None, "last_validated": None},
        "example_before": "",
        "example_after": "",
        "expected_speedup": {"estimate": None, "measurement_method": None},
        "risks": [],
        "opt_in": False,
        "references": [],
    }
    card.update(overrides)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(card, sort_keys=False), encoding="utf-8")


def write_schema(path: Path) -> None:
    schema_source = Path("docs/rules/SCHEMA.yaml").read_text(encoding="utf-8")
    path.write_text(schema_source, encoding="utf-8")


def test_validate_catalog_accepts_valid_card(tmp_path: Path) -> None:
    cards_dir = tmp_path / "cards"
    schema_path = tmp_path / "SCHEMA.yaml"
    write_schema(schema_path)
    write_card(cards_dir / "rule.yaml")

    issues = validate_catalog(cards_dir, schema_path)
    assert issues == []


def test_validate_catalog_rejects_duplicate_ids(tmp_path: Path) -> None:
    cards_dir = tmp_path / "cards"
    schema_path = tmp_path / "SCHEMA.yaml"
    write_schema(schema_path)
    write_card(cards_dir / "one.yaml", id="R-999")
    write_card(cards_dir / "two.yaml", id="R-999", name="other_rule")

    issues = validate_catalog(cards_dir, schema_path)
    assert any("duplicate id" in issue.message for issue in issues)


def test_validate_catalog_rejects_tier_1a_opt_in(tmp_path: Path) -> None:
    cards_dir = tmp_path / "cards"
    schema_path = tmp_path / "SCHEMA.yaml"
    write_schema(schema_path)
    write_card(cards_dir / "rule.yaml", tier="1A", opt_in=True)

    issues = validate_catalog(cards_dir, schema_path)
    assert any("must not require opt-in" in issue.message for issue in issues)


def test_validate_catalog_rejects_missing_required_field(tmp_path: Path) -> None:
    cards_dir = tmp_path / "cards"
    schema_path = tmp_path / "SCHEMA.yaml"
    write_schema(schema_path)
    write_card(cards_dir / "rule.yaml")
    data = yaml.safe_load((cards_dir / "rule.yaml").read_text(encoding="utf-8"))
    del data["category"]
    (cards_dir / "rule.yaml").write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    issues = validate_catalog(cards_dir, schema_path)
    assert any("required property" in issue.message for issue in issues)


def test_validate_catalog_requires_proof_for_validated_tier1(tmp_path: Path) -> None:
    cards_dir = tmp_path / "cards"
    schema_path = tmp_path / "SCHEMA.yaml"
    write_schema(schema_path)
    write_card(cards_dir / "rule.yaml", status="validated", proof="")

    issues = validate_catalog(cards_dir, schema_path)
    assert any("must include proof" in issue.message for issue in issues)
