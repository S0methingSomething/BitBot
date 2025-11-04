"""Maintain command for BitBot CLI."""

from datetime import datetime
from typing import TYPE_CHECKING

import typer
from beartype import beartype
from rich.progress import Progress, SpinnerColumn, TextColumn

from bitbot.core.error_context import error_context
from bitbot.core.error_logger import LogLevel
from bitbot.core.errors import BitBotError
from bitbot.gh.releases.fetcher import get_github_data
from bitbot.gh.releases.updater import update_release_title

if TYPE_CHECKING:
    from rich.console import Console

    from bitbot.config_models import Config
    from bitbot.core.container import Container

app = typer.Typer()


@beartype
@app.command()
def run(ctx: typer.Context) -> None:
    """Mark old releases as outdated."""
    # Get dependencies from container
    container: Container = ctx.obj["container"]
    console: Console = container.console()
    logger = container.logger()
    config: Config = container.config()

    with error_context(command="maintain"):
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                progress.add_task(description="Maintaining releases...", total=None)

                bot_repo = config.github.bot_repo
                outdated_prefix = config.outdated_post_handling.get("prefix", "[OUTDATED]")

                # Fetch releases
                releases_result = get_github_data(f"/repos/{bot_repo}/releases")
                if releases_result.is_err():
                    error = BitBotError(f"GitHub error: {releases_result.error}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {releases_result.error}")
                    raise typer.Exit(code=1) from None
                releases = releases_result.unwrap()

                if not releases:
                    console.print("[yellow][i] No releases found[/yellow]")
                    return

                # Filter to only stable releases (not draft, not prerelease)
                stable_releases = [
                    r
                    for r in releases
                    if not r.get("draft", False) and not r.get("prerelease", False)
                ]

                if not stable_releases:
                    console.print("[yellow][i] No stable releases found[/yellow]")
                    return

                # Find latest release using GitHub's latest flag, fallback to created_at
                latest_release = next(
                    (r for r in stable_releases if r.get("latest", False)),
                    max(
                        stable_releases,
                        key=lambda r: datetime.fromisoformat(
                            r.get("created_at", "1970-01-01T00:00:00Z").replace("Z", "+00:00")
                        ),
                    ),
                )
                latest_tag = latest_release.get("tag_name", "")

                if not latest_tag:
                    console.print("[yellow][i] Could not determine latest release[/yellow]")
                    return

                # Mark old releases as outdated
                updated_count = 0
                for release in stable_releases:
                    tag = release.get("tag_name", "")
                    title = release.get("name", "")

                    if not tag or not title:
                        continue

                    # Skip latest release
                    if tag == latest_tag:
                        continue

                    # Skip if already marked
                    if title.startswith(outdated_prefix):
                        continue

                    # Update title
                    new_title = f"{outdated_prefix} {title}"
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

        except Exception as e:
            error = BitBotError(f"Unexpected error: {e}")
            logger.log_error(error, LogLevel.CRITICAL)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
