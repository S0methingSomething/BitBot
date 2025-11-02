"""Maintain command for BitBot CLI."""

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
from gh.releases.fetcher import get_github_data
from gh.releases.updater import update_release_title

app = typer.Typer()


@beartype
@app.command()
def run(ctx: typer.Context) -> None:
    """Mark old releases as outdated."""
    # Get dependencies from container
    container: Container = ctx.obj["container"]
    console: Console = ctx.obj["console"]
    logger = get_logger(console=console)
    config: Config = container.get("config")

    with error_context(command="maintain"):
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                progress.add_task(description="Maintaining releases...", total=None)

                bot_repo = config.github.bot_repo

                # Fetch releases
                releases_result = get_github_data(f"/repos/{bot_repo}/releases")
                if releases_result.is_err():
                    error = BitBotError(f"GitHub error: {releases_result.error}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {releases_result.error}")
                    raise typer.Exit(code=1) from None
                releases = releases_result.unwrap()

                if not isinstance(releases, list) or not releases:
                    console.print("[yellow][i] No releases found[/yellow]")
                    return

                # Mark old releases as outdated
                updated_count = 0
                for i, release in enumerate(releases):
                    tag = release.get("tag_name", "")
                    title = release.get("name", "")

                    if not tag or not title:
                        continue

                    # Skip most recent release
                    if i == 0:
                        continue

                    # Skip if already marked
                    if title.startswith("[OUTDATED]"):
                        continue

                    # Update title
                    new_title = f"[OUTDATED] {title}"
                    update_result = update_release_title(bot_repo, tag, new_title)
                    if update_result.is_err():
                        console.print(f"[yellow]⚠[/yellow] Failed to update {tag}")
                        continue

                    console.print(f"[cyan]✓[/cyan] Marked {tag} as outdated")
                    updated_count += 1

                if updated_count == 0:
                    console.print("[green]✓[/green] All releases up to date")
                else:
                    console.print(f"[green]✓[/green] Updated {updated_count} release(s)")

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
