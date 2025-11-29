"""Maintain command for BitBot CLI."""

import re
from collections import defaultdict
from typing import TYPE_CHECKING, Any

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
def _extract_app_id(release: dict[str, Any]) -> str:
    """Extract app ID from release body or tag."""
    body = release.get("body", "")
    tag = release.get("tag_name", "")

    # Try to extract from body (structured format)
    for line in body.split("\n"):
        if line.startswith("app:"):
            return line.split(":", 1)[1].strip().lower().replace(" ", "_")

    # Fallback: extract from tag (e.g., "bitlife-v1.0.0" -> "bitlife")
    match = re.match(r"^([a-z_]+)-v", tag.lower())
    if match:
        return match.group(1)

    # Last resort: use tag as-is
    return tag.lower()


@beartype
@app.command()
def run(ctx: typer.Context) -> None:
    """Mark old releases as outdated (per app)."""
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
                configured_apps = {app["id"] for app in config.apps}

                # Fetch releases
                releases_result = get_github_data(f"/repos/{bot_repo}/releases")
                if releases_result.is_err():
                    error = BitBotError(f"GitHub error: {releases_result.unwrap_err()}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {releases_result.unwrap_err()}")
                    raise typer.Exit(code=1) from None

                releases_data = releases_result.unwrap()
                if not isinstance(releases_data, list):
                    console.print("[yellow][i] Unexpected response format[/yellow]")
                    return

                # Filter to stable releases (not draft, not prerelease)
                stable_releases = [
                    r for r in releases_data
                    if not r.get("draft", False) and not r.get("prerelease", False)
                ]

                if not stable_releases:
                    console.print("[yellow][i] No stable releases found[/yellow]")
                    return

                # Group releases by app
                releases_by_app: dict[str, list[dict[str, Any]]] = defaultdict(list)
                for release in stable_releases:
                    app_id = _extract_app_id(release)
                    releases_by_app[app_id].append(release)

                updated_count = 0

                for app_id, app_releases in releases_by_app.items():
                    # Sort by created_at descending (latest first)
                    app_releases.sort(
                        key=lambda r: r.get("created_at", ""),
                        reverse=True,
                    )

                    # If app not in config, mark ALL its releases as outdated
                    if app_id not in configured_apps:
                        for release in app_releases:
                            tag = release.get("tag_name", "")
                            title = release.get("name", "")
                            if not tag or not title or title.startswith(outdated_prefix):
                                continue
                            new_title = f"{outdated_prefix} {title}"
                            update_result = update_release_title(bot_repo, tag, new_title)
                            if update_result.is_ok():
                                console.print(f"[cyan]✓[/cyan] Marked {tag} (unconfigured app)")
                                updated_count += 1
                        continue

                    # For configured apps, mark older releases as outdated
                    if len(app_releases) <= 1:
                        continue

                    for release in app_releases[1:]:
                        tag = release.get("tag_name", "")
                        title = release.get("name", "")
                        if not tag or not title or title.startswith(outdated_prefix):
                            continue
                        new_title = f"{outdated_prefix} {title}"
                        update_result = update_release_title(bot_repo, tag, new_title)
                        if update_result.is_ok():
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
