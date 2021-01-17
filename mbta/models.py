from copy import deepcopy
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
        d = dict(deepcopy(d))
        field_names = {field.name for field in fields(cls)}
        return cls(id=d.pop("id"), **{key: value for key, value in d["attributes"].items() if key in field_names})


@dataclass
class Route(FromApiMixin):
    id: str
    direction_destinations: Sequence[str]
    direction_names: Sequence[str]
    long_name: str
    short_name: str
    sort_order: int

    def directions_strs(self) -> Sequence[str]:
        return [
            f"{name} ({self.direction_destinations[idx]})"
            for idx, name in self.direction_names
        ]

    def __str__(self) -> str:
        return self.long_name


@dataclass
class Stop(FromApiMixin):
    id: str
    name: str

    def __str__(self) -> str:
        return self.name


@dataclass
class Prediction:
    departure_time: datetime

    @classmethod
    def from_api(cls, d: Mapping[str, Any]) -> "Prediction":
        return cls(departure_time=datetime.fromisoformat(d["attributes"]["departure_time"]))
