from typing import Annotated

import typer

APP_NAME = "atlas"
VERSION = "0.1.0"

app = typer.Typer(
    name=APP_NAME,
    help="Atlas command line interface.",
    no_args_is_help=True,
)


@app.command()
def version(
    short: Annotated[
        bool,
        typer.Option("--short", help="Print only the version number."),
    ] = False,
) -> None:
    """Print the CLI version."""
    if short:
        typer.echo(VERSION)
        return

    typer.echo(f"{APP_NAME} {VERSION}")


if __name__ == "__main__":
    app()
