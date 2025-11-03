"""Page command for BitBot CLI."""

from typing import TYPE_CHECKING

import typer
from beartype import beartype
from rich.progress import Progress, SpinnerColumn, TextColumn

from bitbot.core.error_context import error_context
from bitbot.core.error_logger import LogLevel
from bitbot.core.errors import BitBotError
from bitbot.gh.page_generator import generate_landing_page

if TYPE_CHECKING:
    from rich.console import Console

    from bitbot.config_models import Config
    from bitbot.core.container import Container

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
    console: Console = container.console()
    logger = container.logger()
    config: Config = container.config()

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

        except Exception as e:
            error = BitBotError(f"Unexpected error: {e}")
            logger.log_error(error, LogLevel.CRITICAL)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
