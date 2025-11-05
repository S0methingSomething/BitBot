"""Page command for BitBot CLI."""

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

import typer
from beartype import beartype
from rich.progress import Progress, SpinnerColumn, TextColumn

from bitbot import paths
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
    template: str = typer.Option(
        "default_landing_page.html", "--template", "-t", help="Template name"
    ),
) -> None:
    """Generate landing page from release data."""
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

                # Load releases data
                releases_file = Path(paths.DIST_DIR) / "releases.json"
                if not releases_file.exists():
                    console.print("[yellow]⚠[/yellow] No releases.json found, creating empty one")
                    releases_file.parent.mkdir(parents=True, exist_ok=True)
                    with releases_file.open("w") as f:
                        json.dump({}, f)

                with releases_file.open() as f:
                    all_releases_data = json.load(f)

                if not isinstance(all_releases_data, dict):
                    error = BitBotError("releases.json has invalid format")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {error.message}")
                    raise typer.Exit(code=1) from None

                # Prepare data for template
                releases_data: dict[str, Any] = {
                    "bot_repo": config.github.bot_repo,
                    "apps": [],
                }

                # Build apps list from releases data
                for app_id, app_data in all_releases_data.items():
                    if not isinstance(app_data, dict):
                        continue

                    latest = app_data.get("latest_release", {})
                    if not latest:
                        continue

                    # Get previous releases for history
                    previous = app_data.get("previous_releases", [])

                    releases_data["apps"].append(
                        {
                            "id": app_id,
                            "display_name": app_data.get("display_name", app_id),
                            "latest_release": {
                                "version": latest.get("version", "unknown"),
                                "download_url": latest.get("download_url", ""),
                                "published_at": latest.get("published_at", ""),
                            },
                            "releases": previous,  # Previous releases for history section
                        }
                    )

                # Sort apps by display name
                releases_data["apps"].sort(key=lambda x: x["display_name"].lower())

                if not releases_data["apps"]:
                    console.print("[yellow]⚠[/yellow] No release data found, generating empty page")

                # Generate page
                result = generate_landing_page(releases_data, output, template)
                if result.is_err():
                    error = BitBotError(f"Generation error: {result.error}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {result.error}")
                    raise typer.Exit(code=1) from None

                output_path = result.unwrap()
                app_count = len(releases_data["apps"])
                console.print(f"[green]✓[/green] Generated: {output_path} ({app_count} apps)")

        except Exception as e:
            error = BitBotError(f"Unexpected error: {e}")
            logger.log_error(error, LogLevel.CRITICAL)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
