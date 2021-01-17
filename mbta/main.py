import typer

app = typer.Typer()


@app.command()
def main(api_key: str = typer.Option("", envvar="MBTA_API_KEY")) -> None:
    """Find the next train for the MBTA."""
    if not api_key:
        typer.secho("Warning: making API calls without an API key (pass --api-key to use).", fg="yellow")
    typer.echo("TODO")
