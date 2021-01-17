import json
from datetime import datetime
from typing import Any
from typing import Mapping
from typing import Protocol

import pytest

from mbta.models import Prediction
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
        (Stop, """{"attributes": {"address": "Washington St and Hyde Park Ave, Jamaica Plain, MA 02130", "at_street": null, "description": null, "latitude": 42.300523, "location_type": 1, "longitude": -71.113686, "municipality": "Boston", "name": "Forest Hills", "on_street": null, "platform_code": null, "platform_name": null, "vehicle_type": null, "wheelchair_boarding": 1}, "id": "place-forhl", "links": {"self": "/stops/place-forhl"}, "relationships": {"child_stops": {}, "facilities": {"links": {"related": "/facilities/?filter[stop]=place-forhl"}}, "parent_station": {"data": null}, "recommended_transfers": {}, "zone": {"data": {"id": "CR-zone-1A", "type": "zone"}}}, "type": "stop"}""", Stop(id="place-forhl", name="Forest Hills")),
        (Prediction, """{"attributes": {"arrival_time": "2021-01-17T14:15:28-05:00", "departure_time": "2021-01-17T14:15:59-05:00", "direction_id": 0, "schedule_relationship": null, "status": null, "stop_sequence": 280}, "id": "prediction-46460806-70115-280", "relationships": {"route": {"data": {"id": "Green-B", "type": "route"}}, "stop": {"data": {"id": "70115", "type": "stop"}}, "trip": {"data": {"id": "46460806", "type": "trip"}}, "vehicle": {"data": {"id": "G-10023", "type": "vehicle"}}}, "type": "prediction"}""", Prediction(departure_time=datetime.fromisoformat("2021-01-17T14:15:59-05:00"))),
    ]
)
def test_model_from_api(model_cls: FromApi, json_str: str, expected: Any) -> None:
    assert hasattr(model_cls, "from_api")
    obj = model_cls.from_api(json.loads(json_str))
    assert obj == expected
