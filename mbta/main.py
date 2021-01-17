import functools
from typing import Sequence
from typing import TypeVar
from typing import overload

import click
import typer

from mbta.models import Route
from mbta.models import Stop
from mbta.shared import config
from mbta.shared import mbta_session

T = TypeVar("T")

app = typer.Typer()


@app.command()
def main(api_key: str = typer.Option("", envvar="MBTA_API_KEY")) -> None:
    """Find the next train for the MBTA."""
    cfg = config()
    if api_key:
        cfg.api_key = api_key
    else:
        typer.secho("Warning: making API calls without an API key (pass --api-key to use one).", fg="yellow")
    route = select_route()
    stop = select_stop(route)
    direction = select_direction(route)

    typer.echo(f"Next departure time is {next_departure_time(route, direction, stop)}")


def select_route() -> Route:
    """Select a route."""
    routes = get_routes()
    return select_from_list(routes)


def select_stop(route: Route) -> "Stop":
    """Select a stop on the given route."""
    stops = get_stops(route.id)
    return select_from_list(stops)


def select_direction(route: Route) -> str:
    """Select a direction on the given route."""
    return select_from_list(route.direction_names, "direction")


def select_from_list(seq: Sequence[T], noun: str = None) -> T:
    """Present a list of choices, and return the selected choice."""
    if noun is None:
        noun = str(type(seq[0]).__name__.lower())
    typer.echo(f"Select a {noun} from the list below:")
    for idx, stop in enumerate(seq):
        idx_str = typer.style(f"{idx}.", bold=True)
        typer.echo(f"{idx_str} {stop}")
    chosen_idx = int(typer.prompt(f"", type=click.Choice([str(idx) for idx, _ in enumerate(seq)])))
    return seq[chosen_idx]


@functools.lru_cache(maxsize=None)
def get_routes() -> Sequence[Route]:
    session = mbta_session()
    response = session.get("routes?filter[type]=0,1")
    response.raise_for_status()
    return sorted(
        (Route.from_api(route_json) for route_json in response.json()["data"]),
        key=lambda route: route.sort_order
    )


@functools.lru_cache(maxsize=None)
def get_stops(route_id: str) -> Sequence[Stop]:
    session = mbta_session()
    response = session.get(f"stops?filter[route]={route_id}")
    response.raise_for_status()
    return [Stop.from_api(stop_json) for stop_json in response.json()["data"]]
