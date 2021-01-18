import json
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import Mapping
from typing import Protocol

import pytest

from mbta.models import Prediction
from mbta.models import Route
from mbta.models import Stop


class FromApi(Protocol):
    """Protocol for a dataclass with a `from_api` method."""

    @classmethod
    def from_api(cls, d: Mapping[str, Any]) -> Any:
        ...


@pytest.mark.parametrize(
    ("model_cls", "json_file", "expected"),
    [
        pytest.param(
            Route,
            "data/route.json",
            Route(
                id="Red",
                direction_destinations=["Ashmont/Braintree", "Alewife"],
                direction_names=["South", "North"],
                long_name="Red Line",
                short_name="",
                sort_order=10010,
            ),
            id="Route",
        ),
        pytest.param(
            Stop,
            "data/stop.json",
            Stop(id="place-forhl", name="Forest Hills"),
            id="Stop",
        ),
        pytest.param(
            Prediction,
            "data/prediction.json",
            Prediction(departure_time=datetime.fromisoformat("2021-01-17T14:15:59-05:00")),
            id="Prediction",
        ),
    ],
)
def test_model_from_api(model_cls: FromApi, json_file: str, expected: Any) -> None:
    assert hasattr(model_cls, "from_api")
    json_str = (Path(__file__).parent / json_file).read_text()
    model_obj = model_cls.from_api(json.loads(json_str))
    assert model_obj == expected
