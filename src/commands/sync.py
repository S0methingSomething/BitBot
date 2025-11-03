"""Sync command for BitBot CLI."""

import typer
from beartype import beartype
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.core.error_context import error_context
from src.core.error_logger import LogLevel, get_logger
from src.core.errors import BitBotError

app = typer.Typer()
console = Console()
logger = get_logger(console=console)


@beartype
@app.command()
def run() -> None:
    """Sync Reddit state."""
    with error_context(operation="sync_reddit_history"):
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                progress.add_task(description="Syncing Reddit state...", total=None)
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
