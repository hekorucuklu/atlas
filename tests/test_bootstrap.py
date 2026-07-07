from typer.testing import CliRunner

from apps.cli.main import app

runner = CliRunner()


def test_cli_help_exits_successfully() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Atlas command line interface" in result.output


def test_cli_version_exits_successfully() -> None:
    result = runner.invoke(app, ["version", "--short"])

    assert result.exit_code == 0
    assert result.output.strip() == "0.1.0"
