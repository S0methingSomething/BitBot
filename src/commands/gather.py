"""Gather command for BitBot CLI."""

import sys
from pathlib import Path

import typer
from beartype import beartype
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.error_context import error_context
from core.error_logger import LogLevel, get_logger
from core.errors import BitBotError

app = typer.Typer()
console = Console()
logger = get_logger(console=console)


@beartype
@app.command()
def run() -> None:
    """Gather post data."""
    with error_context(operation="gather_post_data"):
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                progress.add_task(description="Gathering post data...", total=None)
                msg = "Legacy script moved - needs refactoring"
                raise NotImplementedError(msg)

        except BitBotError as e:
            logger.log_error(e, LogLevel.ERROR)
            console.print(f"[red]✗ Error:[/red] {e.message}")
            raise typer.Exit(code=1) from None
        except Exception as e:
            error = BitBotError(f"Unexpected error: {e}")
            logger.log_error(error, LogLevel.CRITICAL)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
