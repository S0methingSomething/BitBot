"""Check command for BitBot CLI."""

import sys
from pathlib import Path

import typer
from beartype import beartype
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
    """Check Reddit comments for feedback."""
    with error_context(operation="check_comments"):
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                progress.add_task(description="Checking comments...", total=None)
                
                # LEGACY: from check_comments import main as check_main
                
                result = check_main()
                if result.is_err():
                    logger.log_error(result.error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {result.error.message}")
                    raise typer.Exit(code=1)
                
                console.print("[green]✓ Successfully checked comments[/green]")
                    
        except BitBotError as e:  # noqa: BLE001
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
