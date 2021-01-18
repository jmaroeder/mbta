from typing import Sequence

import pytest
from typer.testing import CliRunner

from mbta.main import app

runner = CliRunner()


@pytest.mark.parametrize(
    ("inputs", "expected_outputs", "exit_code"),
    [
        pytest.param("0\n0\n0\n", [], 0, id="found_departure"),
        pytest.param("0\n0\n1\n", [], 1, id="no_departures"),
    ],
)
def test_command_line(inputs: str, exit_code: int, expected_outputs: Sequence[str], mock_api) -> None:
    result = runner.invoke(app, input=inputs)
    print(result.stdout)
    for substr in expected_outputs or []:
        assert substr in result.stdout
    assert result.exit_code == exit_code


def test_warning_about_api_key() -> None:
    result = runner.invoke(app, input="0\n0\n0\n", env={"MBTA_API_KEY": ""})
    assert "making API calls without an API key" in result.stdout
    assert result.exit_code == 0
