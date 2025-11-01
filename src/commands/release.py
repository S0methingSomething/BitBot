"""Release command for BitBot CLI."""
import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def run() -> None:
    """Release command."""
    console.print("[yellow]Release command - TODO: Implement[/yellow]")

if __name__ == "__main__":
    app()
