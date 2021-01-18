import functools
from datetime import datetime
from datetime import timezone
from typing import Iterable
from typing import List
from typing import Optional
from typing import Sequence
from typing import TypeVar

import click
import typer

from mbta.models import Prediction
from mbta.models import Route
from mbta.models import Stop
from mbta.shared import config
from mbta.shared import mbta_session

DEFAULT_ROUTE_TYPES = (0, 1)  # light rail, heavy rail
T = TypeVar("T")

app = typer.Typer()

API_KEY_OPTION = typer.Option("", envvar="MBTA_API_KEY")


@app.command()
def main(api_key: str = API_KEY_OPTION) -> None:
    """Find the next train for the MBTA."""
    cfg = config()
    if api_key:
        cfg.api_key = api_key
    else:
        typer.secho("Warning: making API calls without an API key (pass --api-key to use one).", fg="yellow")
    route = select_route()
    stop = select_stop(route)
    direction_id = select_direction(route)
    next_departure = next_departure_time(route=route, direction_id=direction_id, stop=stop)
    if not next_departure:
        typer.echo("No departures found after the current time!")
        raise typer.Exit(1)
    typer.echo(f"Next departure time is {next_departure}.")


def select_route() -> Route:
    """Select a route."""
    routes = get_routes()
    return select_from_list(routes)


def select_stop(route: Route) -> Stop:
    """Select a stop on the given route."""
    stops = get_stops(route.id)
    return select_from_list(stops)


def select_direction(route: Route) -> int:
    """Select a direction on the given route."""
    return select_idx_from_list(route.direction_names, "direction")


def next_departure_time(route: Route, direction_id: int, stop: Stop) -> Optional[datetime]:
    """Get the next predicted departure time."""
    predictions = get_predictions(route=route, direction_id=direction_id, stop=stop)
    now = datetime.now(tz=timezone.utc)
    for prediction in predictions:
        if prediction.departure_time > now:
            return prediction.departure_time
    return None


def select_from_list(seq: Sequence[T], noun: str = None) -> T:
    """Present a list of choices, and return the thing itself."""
    chosen_idx = select_idx_from_list(seq, noun)
    return seq[chosen_idx]


def select_idx_from_list(seq: Sequence[T], noun: str = None) -> int:
    """Present a list of choices, and return the index of the selected choice."""
    if noun is None:
        noun = str(type(seq[0]).__name__.lower())
    typer.echo(f"Select a {noun} from the list below:")
    choices: List[str] = []
    for idx, stop in enumerate(seq):
        choices.append(f"{idx}")
        idx_str = typer.style(f"{idx}.", bold=True)
        typer.echo(f"{idx_str} {stop}")
    return int(typer.prompt("", type=click.Choice(choices)))


@functools.lru_cache(maxsize=None)
def get_routes(route_types: Iterable[int] = DEFAULT_ROUTE_TYPES) -> Sequence[Route]:
    """Get all routes of the given types."""
    session = mbta_session()
    filter_types = ",".join(str(route_type) for route_type in route_types)
    response = session.get("routes", params={"filter[type]": filter_types})
    response.raise_for_status()
    return sorted(
        (Route.from_api(route_json) for route_json in response.json()["data"]), key=lambda route: route.sort_order
    )


@functools.lru_cache(maxsize=None)
def get_stops(route_id: str) -> Sequence[Stop]:
    """Get all the stops for the given route."""
    session = mbta_session()
    response = session.get("stops", params={"filter[route]": route_id})
    response.raise_for_status()
    return [Stop.from_api(stop_json) for stop_json in response.json()["data"]]


def get_predictions(route: Route, direction_id: int, stop: Stop) -> Sequence[Prediction]:
    """Get departure predictions for the given route, direction, and stop, sorted by ascending departure time."""
    session = mbta_session()
    response = session.get(
        "predictions", params={"filter[route]": route.id, "filter[direction_id]": direction_id, "filter[stop]": stop.id}
    )
    response.raise_for_status()
    return sorted(
        (
            Prediction.from_api(prediction_json)
            for prediction_json in response.json()["data"]
            if prediction_json.get("attributes", {}).get("departure_time")
        ),
        key=lambda prediction: prediction.departure_time,
    )
