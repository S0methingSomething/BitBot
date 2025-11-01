"""Check command for BitBot CLI."""
import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def run() -> None:
    """Check Reddit comments for feedback."""
    console.print("[yellow]Check command - TODO: Implement[/yellow]")

if __name__ == "__main__":
    app()
