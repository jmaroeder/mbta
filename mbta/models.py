import itertools
from dataclasses import dataclass
from dataclasses import fields
from datetime import datetime
from typing import Any
from typing import Mapping
from typing import Sequence


class FromApiMixin:
    """Mixin to build dataclasses from JSON-API objects."""

    @classmethod
    def from_api(cls, d: Mapping[str, Any]) -> Any:
        """Return a dataclass object from a JSON-API ``data`` result."""
        field_names = {field.name for field in fields(cls)}
        kwargs = {}
        for key, value in itertools.chain(  # noqa: WPS352
            d.items(),
            d.get("attributes", {}).items(),
        ):
            if key in field_names:
                kwargs[key] = value
        return cls(**kwargs)  # type: ignore[call-arg]


@dataclass
class Route(FromApiMixin):
    """
    Subset of Route object.

    See https://api-v3.mbta.com/docs/swagger/index.html#/Route
    """

    id: str
    direction_destinations: Sequence[str]
    direction_names: Sequence[str]
    long_name: str
    short_name: str
    sort_order: int

    def __str__(self) -> str:
        return self.long_name


@dataclass
class Stop(FromApiMixin):
    """
    Subset of Stop object.

    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop
    """

    id: str
    name: str

    def __str__(self) -> str:
        return self.name


@dataclass
class Prediction:
    """
    Subset of Prediction object.

    See https://api-v3.mbta.com/docs/swagger/index.html#/Prediction
    """

    departure_time: datetime

    @classmethod
    def from_api(cls, d: Mapping[str, Any]) -> "Prediction":
        """Return a Prediction object from a JSON-API ``data`` result."""
        return cls(departure_time=datetime.fromisoformat(d["attributes"]["departure_time"]))
