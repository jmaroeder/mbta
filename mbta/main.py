import functools
from typing import Sequence

import click
import typer

from mbta.models import Route
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


@functools.lru_cache(maxsize=None)
def get_routes() -> Sequence[Route]:
    session = mbta_session()
    response = session.get("routes?filter[type]=0,1")
    response.raise_for_status()
    return sorted(
        (Route.from_api(route_json) for route_json in response.json()["data"]),
        key=lambda route: route.sort_order
    )
