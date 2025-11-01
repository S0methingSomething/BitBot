"""Check command for BitBot CLI."""

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
    """Check Reddit comments for feedback."""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(description="Checking comments...", total=None)
            
            from check_comments import main as check_main
            
            try:
                check_main()
                console.print("[green]✓ Successfully checked comments[/green]")
            except SystemExit as e:
                if e.code != 0:
                    console.print("[red]✗ Failed to check comments[/red]")
                    raise typer.Exit(code=e.code)
                
    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
