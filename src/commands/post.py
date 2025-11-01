"""Post command for BitBot CLI."""

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def run(
    page_url: str = typer.Option(None, "--page-url", help="Custom landing page URL"),
) -> None:
    """Post new releases to Reddit."""
    console.print("[yellow]Post command - TODO: Implement[/yellow]")
    # TODO: Import and call post_to_reddit logic


if __name__ == "__main__":
    app()
