from typer.testing import CliRunner

from clickadvisor.cli.app import app


def test_version_command() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "ClickAdvisor" in result.stdout
