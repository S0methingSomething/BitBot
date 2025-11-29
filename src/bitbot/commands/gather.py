"""Gather command for BitBot CLI."""

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

import typer
from beartype import beartype
from returns.result import Failure
from rich.progress import Progress, SpinnerColumn, TextColumn

from bitbot import paths
from bitbot.core.error_context import error_context
from bitbot.core.error_logger import LogLevel
from bitbot.core.errors import BitBotError
from bitbot.gh.releases.fetcher import get_github_data

if TYPE_CHECKING:
    from rich.console import Console

    from bitbot.config_models import Config
    from bitbot.core.container import Container

app = typer.Typer()


@beartype
def _parse_release_metadata(release: dict[str, Any]) -> tuple[str | None, str | None]:
    """Parse app ID and version from release body."""
    body = release.get("body", "")
    app_id = None
    version = None

    for raw_line in body.split("\n"):
        line = raw_line.strip()
        if line.startswith("app:"):
            app_id = line.split(":", 1)[1].strip()
        elif line.startswith("version:"):
            version = line.split(":", 1)[1].strip()

    return app_id, version


@beartype
@app.command()
def run(ctx: typer.Context) -> None:
    """Gather releases from source repository and create releases.json."""
    container: Container = ctx.obj["container"]
    console: Console = container.console()
    logger = container.logger()
    config: Config = container.config()

    with error_context(command="gather"):
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                progress.add_task(description="Gathering releases...", total=None)

                source_repo = config.github.source_repo
                bot_repo = config.github.bot_repo
                apps_config = {
                    app["id"]: app["displayName"] for app in config.model_dump().get("apps", [])
                }

                # Fetch releases from source repo (has correct app IDs)
                source_result = get_github_data(f"/repos/{source_repo}/releases?per_page=100")
                if isinstance(source_result, Failure):
                    error = BitBotError(f"GitHub API error: {source_result.failure()}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {source_result.failure()}")
                    raise typer.Exit(code=1) from None

                source_releases = source_result.unwrap()
                if not isinstance(source_releases, list):
                    error = BitBotError("Expected list of releases from GitHub API")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {error.message}")
                    raise typer.Exit(code=1) from None

                # Fetch bot repo releases for download URLs
                bot_result = get_github_data(f"/repos/{bot_repo}/releases?per_page=100")
                bot_data = bot_result.unwrap() if isinstance(bot_result, Failure) is False else []
                bot_releases: list[dict[str, Any]] = bot_data if isinstance(bot_data, list) else []

                # Get latest releases from source (has correct app IDs)
                apps_data: dict[str, Any] = {}
                for release in source_releases:
                    app_id, version = _parse_release_metadata(release)
                    if not app_id or not version:
                        continue
                    if app_id not in apps_config:
                        continue

                    # Find download URL from bot repo
                    download_url = ""
                    for bot_rel in bot_releases:
                        if not bot_rel.get("assets"):
                            continue
                        _, bot_ver = _parse_release_metadata(bot_rel)
                        if bot_ver == version:
                            download_url = bot_rel["assets"][0]["browser_download_url"]
                            break

                    if not download_url:
                        continue

                    apps_data[app_id] = {
                        "display_name": apps_config[app_id],
                        "latest_release": {
                            "version": version,
                            "download_url": download_url,
                            "published_at": release["published_at"],
                        },
                        "previous_releases": [],
                    }

                # Get version history from bot repo (normalize app IDs)
                for release in bot_releases:
                    if not release.get("assets"):
                        continue
                    bot_app_id, version = _parse_release_metadata(release)
                    if not bot_app_id or not version:
                        continue

                    # Match to config ID via normalization
                    normalized = bot_app_id.lower().replace(" ", "_")
                    matched_id = None
                    for cfg_id in apps_config:
                        if cfg_id == bot_app_id or cfg_id.lower().replace(" ", "_") == normalized:
                            matched_id = cfg_id
                            break

                    if not matched_id or matched_id not in apps_data:
                        continue

                    # Skip if it's the latest version
                    if version == apps_data[matched_id]["latest_release"]["version"]:
                        continue

                    apps_data[matched_id]["previous_releases"].append({
                        "version": version,
                        "download_url": release["assets"][0]["browser_download_url"],
                        "published_at": release["published_at"],
                    })

                # Save to releases.json
                dist_dir = Path(paths.DIST_DIR)
                dist_dir.mkdir(parents=True, exist_ok=True)
                releases_file = dist_dir / "releases.json"

                with releases_file.open("w") as f:
                    json.dump(apps_data, f, indent=2)

                app_count = len(apps_data)
                console.print(f"[green]✓[/green] Gathered {app_count} app(s) from releases")

        except Exception as e:
            error = BitBotError(f"Unexpected error: {e}")
            logger.log_error(error, LogLevel.CRITICAL)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
