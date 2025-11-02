"""Page command for BitBot CLI."""

import sys
from pathlib import Path

import typer
from beartype import beartype
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

sys.path.insert(0, str(Path(__file__).parent.parent))

from config_models import Config
from core.container import Container
from core.error_context import error_context
from core.error_logger import LogLevel, get_logger
from core.errors import BitBotError
from gh.page_generator import generate_landing_page

app = typer.Typer()


@beartype
@app.command()
def run(
    ctx: typer.Context,
    output: str = typer.Option("dist/index.html", "--output", "-o", help="Output path"),
) -> None:
    """Generate landing page."""
    # Get dependencies from container
    container: Container = ctx.obj["container"]
    console: Console = ctx.obj["console"]
    logger = get_logger(console=console)
    config: Config = container.get("config")

    with error_context(command="page"):
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                progress.add_task(description="Generating landing page...", total=None)

                # Prepare data (minimal for now)
                releases_data = {
                    "bot_repo": config.github.bot_repo,
                    "apps": [],
                }

                # Generate page
                result = generate_landing_page(releases_data, output)
                if result.is_err():
                    error = BitBotError(f"Generation error: {result.error}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {result.error}")
                    raise typer.Exit(code=1) from None

                output_path = result.unwrap()
                console.print(f"[green]✓[/green] Generated: {output_path}")

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
