import functools
from typing import Sequence

import click
import typer

from mbta.models import Route
from mbta.models import Stop
from mbta.shared import config
from mbta.shared import mbta_session

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
    typer.secho(f"Next departure time is {next_departure_time(route, direction, stop)}")


def select_route() -> Route:
    """"""
    routes = get_routes()
    typer.secho("Select a route from the list below:")
    for idx, route in enumerate(routes):
        idx_str = typer.style(f"{idx}.", bold=True)
        typer.echo(f"{idx_str} {route}")
    route_idx = int(typer.prompt("Route", type=click.Choice([str(idx) for idx, _ in enumerate(routes)])))
    return routes[route_idx]


def select_stop(route: Route) -> "Stop":
    stops = get_stops(route.id)
    typer.secho("Select a stop from the list below:")
    for idx, stop in enumerate(stops):
        idx_str = typer.style(f"{idx}.", bold=True)
        typer.echo(f"{idx_str} {stop}")
    stop_idx = int(typer.prompt("Stop", type=click.Choice([str(idx) for idx, _ in enumerate(stops)])))
    return stops[stop_idx]


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
