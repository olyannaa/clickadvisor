import json

from typer.testing import CliRunner

from clickadvisor.cli.app import app


def test_analyze_accepts_environment_json(tmp_path) -> None:
    sql_path = tmp_path / "query.sql"
    env_path = tmp_path / "environment.json"
    sql_path.write_text("SELECT count() FROM events", encoding="utf-8")
    env_path.write_text(json.dumps({"settings": {"join_use_nulls": True}}), encoding="utf-8")

    result = CliRunner().invoke(
        app,
        [
            "analyze",
            "--sql",
            str(sql_path),
            "--environment",
            str(env_path),
            "--output-format",
            "json",
            "--ch-version",
            "25.3",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert any(finding["rule_id"] == "E-012" for finding in payload["findings"])


def test_analyze_rejects_invalid_environment_json(tmp_path) -> None:
    sql_path = tmp_path / "query.sql"
    env_path = tmp_path / "environment.json"
    sql_path.write_text("SELECT count() FROM events", encoding="utf-8")
    env_path.write_text("[1, 2, 3]", encoding="utf-8")

    result = CliRunner().invoke(
        app,
        ["analyze", "--sql", str(sql_path), "--environment", str(env_path)],
    )

    assert result.exit_code != 0
    assert "environment JSON must be an object" in result.stderr
