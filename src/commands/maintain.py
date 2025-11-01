"""Maintain command for BitBot CLI."""
import sys
from pathlib import Path
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

sys.path.insert(0, str(Path(__file__).parent.parent))

app = typer.Typer()
console = Console()

@app.command()
def run() -> None:
    """Maintain releases."""
    try:
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            progress.add_task(description="Maintaining releases...", total=None)
            from maintain_releases import main as maintain_main
            try:
                maintain_main()
                console.print("[green]✓ Successfully maintained releases[/green]")
            except SystemExit as e:
                if e.code != 0:
                    console.print("[red]✗ Failed to maintain releases[/red]")
                    raise typer.Exit(code=e.code)
    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
