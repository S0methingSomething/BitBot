"""Post command for BitBot CLI."""

import sys
from pathlib import Path

import typer
from beartype import beartype
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.error_context import error_context
from core.error_logger import LogLevel, get_logger
from core.errors import BitBotError

app = typer.Typer()
console = Console()
logger = get_logger(console=console)


@beartype  # type: ignore[misc]
@app.command()
def run(
    page_url: str = typer.Option(None, "--page-url", help="Custom landing page URL"),
) -> None:
    """Post new releases to Reddit."""
    with error_context(operation="post_to_reddit", page_url=page_url):
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                progress.add_task(description="Posting to Reddit...", total=None)
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
