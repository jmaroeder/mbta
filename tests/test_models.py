import json
from typing import Any
from typing import Mapping
from typing import Protocol

import pytest

from mbta.models import Route
from mbta.models import Stop


class FromApi(Protocol):
    @classmethod
    def from_api(cls, d: Mapping[str, Any]) -> Any:
        ...


@pytest.mark.parametrize(
    ("model_cls", "json_str", "expected"),
    [
        (Route, """{"attributes": {"color": "DA291C", "description": "Rapid Transit", "direction_destinations": ["Ashmont/Braintree", "Alewife"], "direction_names": ["South", "North"], "fare_class": "Rapid Transit", "long_name": "Red Line", "short_name": "", "sort_order": 10010, "text_color": "FFFFFF", "type": 1}, "id": "Red", "links": {"self": "/routes/Red"}, "relationships": {"line": {"data": {"id": "line-Red", "type": "line"}}, "route_patterns": {}}, "type": "route"}""", Route(id="Red", direction_destinations=["Ashmont/Braintree", "Alewife"], direction_names=["South", "North"], long_name="Red Line", short_name="", sort_order=10010)),
    ]
)
def test_model_from_api(model_cls: FromApi, json_str: str, expected: Any) -> None:
    assert hasattr(model_cls, "from_api")
    obj = model_cls.from_api(json.loads(json_str))
    assert obj == expected
