from typer.testing import CliRunner

from mbta.main import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, input="TODO\n")
    assert result.exit_code == 0
