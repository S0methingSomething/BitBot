from beartype import beartype

"""Maintain command for BitBot CLI."""

import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

sys.path.insert(0, str(Path(__file__).parent.parent))  # noqa: E402

from core.error_context import error_context
from core.error_logger import ErrorLogger, LogLevel
from core.errors import BitBotError

app = typer.Typer()
console = Console()
logger = ErrorLogger(console=console)


@beartype  # type: ignore[misc]
@app.command()
def run() -> None:
    """Maintain releases."""
    with error_context(operation="maintain_releases"):
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                progress.add_task(description="Maintaining releases...", total=None)

                # LEGACY: from maintain_releases import main as maintainreleases_main  # noqa: PLC0415

                try:
                    maintainreleases_main()
                    console.print("[green]✓ Successfully maintained releases[/green]")
                except SystemExit as e:
                    if e.code != 0:
                        error = BitBotError("Maintain failed")
                        logger.log_error(error, LogLevel.ERROR)
                        console.print("[red]✗ Failed to maintain releases[/red]")
                        raise typer.Exit(code=e.code)

        except BitBotError as e:
            logger.log_error(e, LogLevel.ERROR)
            console.print(f"[red]✗ Error:[/red] {e.message}")
            raise typer.Exit(code=1)
        except Exception as e:  # noqa: BLE001
            error = BitBotError(f"Unexpected error: {e}")
            logger.log_error(error, LogLevel.CRITICAL)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
