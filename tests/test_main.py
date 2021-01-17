from typer.testing import CliRunner

from mbta.main import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, input="0\n0\n0\n")
    assert result.exit_code == 1

    result = runner.invoke(app, input="0\n1\n0\n")
    assert result.exit_code == 0
