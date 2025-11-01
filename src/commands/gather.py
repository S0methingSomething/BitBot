"""Gather command for BitBot CLI."""
import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def run() -> None:
    """Gather command."""
    console.print("[yellow]Gather command - TODO: Implement[/yellow]")

if __name__ == "__main__":
    app()
