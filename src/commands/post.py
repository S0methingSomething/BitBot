"""Post command for BitBot CLI."""

import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.error_context import error_context
from core.error_logger import ErrorLogger, LogLevel
from core.errors import BitBotError

app = typer.Typer()
console = Console()
logger = ErrorLogger(console=console)


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
                
                # Import here to avoid circular imports
                from post_to_reddit import main as post_main
                
                # Temporarily override sys.argv for the old script
                old_argv = sys.argv
                sys.argv = ["post_to_reddit"]
                if page_url:
                    sys.argv.extend(["--page-url", page_url])
                
                try:
                    post_main()
                    console.print("[green]✓ Successfully posted to Reddit[/green]")
                except SystemExit as e:
                    if e.code != 0:
                        error = BitBotError("Post to Reddit failed")
                        logger.log_error(error, LogLevel.ERROR)
                        console.print("[red]✗ Failed to post to Reddit[/red]")
                        raise typer.Exit(code=e.code)
                finally:
                    sys.argv = old_argv
                    
        except BitBotError as e:
            logger.log_error(e, LogLevel.ERROR)
            console.print(f"[red]✗ Error:[/red] {e.message}")
            raise typer.Exit(code=1)
        except Exception as e:
            error = BitBotError(f"Unexpected error: {e}")
            logger.log_error(error, LogLevel.CRITICAL)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
