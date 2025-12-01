"""Gather command for BitBot CLI."""

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any
from urllib.parse import urlparse

import typer
from beartype import beartype
from returns.result import Failure, Success
from rich.progress import Progress, SpinnerColumn, TextColumn

from bitbot import paths
from bitbot.core import db
from bitbot.core.app_registry import AppRegistry
from bitbot.core.error_context import error_context
from bitbot.core.error_logger import LogLevel
from bitbot.core.errors import BitBotError
from bitbot.core.release_parser import parse_release_body
from bitbot.gh.releases.fetcher import get_github_data

if TYPE_CHECKING:
    from rich.console import Console

    from bitbot.config_models import Config
    from bitbot.core.container import Container

app = typer.Typer()


@beartype
def _queue_new_releases(
    source_releases: list[dict[str, Any]],
    registry: AppRegistry,
    console: "Console",
) -> int:
    """Detect and queue new releases from source repo. Returns count of queued releases."""
    # Get already processed release IDs
    processed_result = db.get_processed_releases()
    processed_ids = processed_result.unwrap() if isinstance(processed_result, Success) else set()

    queued = 0
    for release in source_releases:
        release_id = release.get("id")
        if not release_id or release_id in processed_ids:
            continue

        parsed = parse_release_body(release.get("body", ""))
        if not parsed.is_complete:
            continue

        matched_app = registry.get(parsed.app_id)  # type: ignore[arg-type]
        if not matched_app:
            continue

        # Queue this release for processing
        result = db.add_pending_release(
            release_id=release_id,
            app_id=matched_app.id,
            display_name=matched_app.display_name,
            version=parsed.version,  # type: ignore[arg-type]
            tag=release.get("tag_name", f"v{parsed.version}"),
            asset_name=parsed.asset_name,
        )

        if isinstance(result, Success):
            console.print(f"[cyan]→[/cyan] Queued: {matched_app.display_name} v{parsed.version}")
            queued += 1
            # Mark as processed so we don't queue again
            db.add_processed_release(release_id)

    return queued


@beartype
def _validate_url(url: str) -> bool:
    """Validate a URL is well-formed."""
    if not url:
        return False
    
    # Check for common malformed patterns
    if url.count("://") > 1:
        return False
    if "htttps" in url.lower() or "htttp" in url.lower():
        return False
    
    try:
        parsed = urlparse(url)
        if not parsed.scheme or parsed.scheme not in ("http", "https"):
            return False
        if not parsed.netloc:
            return False
        # Check for protocol in domain (sign of double-prefix bug)
        if "http" in parsed.netloc.lower():
            return False
        return True
    except Exception:
        return False


@beartype
def _build_releases_json(
    source_releases: list[dict[str, Any]],
    bot_releases: list[dict[str, Any]],
    registry: AppRegistry,
    console: "Console",
) -> dict[str, Any]:
    """Build releases.json from source and bot releases."""
    apps_data: dict[str, Any] = {}

    # Build index of bot releases by (app_id, version) for fast lookup
    bot_index: dict[tuple[str, str], str] = {}
    for bot_rel in bot_releases:
        if not bot_rel.get("assets"):
            continue
        bot_parsed = parse_release_body(bot_rel.get("body", ""))
        if not bot_parsed.is_complete:
            continue
        bot_app = registry.get(bot_parsed.app_id or "")
        if bot_app:
            url = bot_rel["assets"][0]["browser_download_url"]
            # Validate URL before adding to index
            if _validate_url(url):
                key = (bot_app.id, bot_parsed.version)  # type: ignore[arg-type]
                bot_index[key] = url
            else:
                console.print(f"[yellow]⚠ Skipping invalid URL for {bot_app.id}: {url[:50]}[/yellow]")

    # Get latest releases from source
    for release in source_releases:
        parsed = parse_release_body(release.get("body", ""))
        if not parsed.is_complete:
            continue

        matched_app = registry.get(parsed.app_id)  # type: ignore[arg-type]
        if not matched_app:
            continue

        app_id = matched_app.id
        version = parsed.version

        # Skip if we already have a newer version for this app
        if app_id in apps_data:
            continue

        # Find download URL from bot repo
        download_url = bot_index.get((app_id, version), "")  # type: ignore[arg-type]
        if not download_url:
            continue

        apps_data[app_id] = {
            "display_name": matched_app.display_name,
            "latest_release": {
                "version": version,
                "download_url": download_url,
                "published_at": release["published_at"],
            },
            "previous_releases": [],
        }

    # Get version history from bot repo
    for bot_rel in bot_releases:
        if not bot_rel.get("assets"):
            continue

        parsed = parse_release_body(bot_rel.get("body", ""))
        if not parsed.is_complete:
            continue

        matched_app = registry.get(parsed.app_id)  # type: ignore[arg-type]
        if not matched_app or matched_app.id not in apps_data:
            continue

        app_id = matched_app.id
        version = parsed.version

        # Skip if it's the latest version
        if version == apps_data[app_id]["latest_release"]["version"]:
            continue

        # Validate URL before adding
        url = bot_rel["assets"][0]["browser_download_url"]
        if not _validate_url(url):
            console.print(f"[yellow]⚠ Skipping invalid URL for {app_id} v{version}[/yellow]")
            continue

        apps_data[app_id]["previous_releases"].append(
            {
                "version": version,
                "download_url": url,
                "published_at": bot_rel["published_at"],
            }
        )

    return apps_data


@beartype
@app.command()
def run(ctx: typer.Context) -> None:
    """Gather releases from source repository, queue new ones, and create releases.json."""
    container: Container = ctx.obj["container"]
    console: Console = container.console()
    logger = container.logger()
    config: Config = container.config()
    registry: AppRegistry = container.app_registry()

    with error_context(command="gather"):
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                progress.add_task(description="Gathering releases...", total=None)

                # Initialize database
                db.init()

                source_repo = config.github.source_repo
                bot_repo = config.github.bot_repo

                # Fetch releases from source repo
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

                # Queue new releases for processing
                queued_count = _queue_new_releases(source_releases, registry, console)
                if queued_count > 0:
                    console.print(f"[green]✓[/green] Queued {queued_count} new release(s)")

                # Fetch bot repo releases for download URLs
                bot_result = get_github_data(f"/repos/{bot_repo}/releases?per_page=100")
                bot_data = bot_result.unwrap() if not isinstance(bot_result, Failure) else []
                bot_releases: list[dict[str, Any]] = bot_data if isinstance(bot_data, list) else []

                # Build releases.json
                apps_data = _build_releases_json(source_releases, bot_releases, registry, console)

                # Save to releases.json
                dist_dir = Path(paths.DIST_DIR)
                dist_dir.mkdir(parents=True, exist_ok=True)
                releases_file = dist_dir / "releases.json"

                with releases_file.open("w") as f:
                    json.dump(apps_data, f, indent=2)

                app_count = len(apps_data)
                console.print(f"[green]✓[/green] Gathered {app_count} app(s) into releases.json")

        except Exception as e:
            error = BitBotError(f"Unexpected error: {e}")
            logger.log_error(error, LogLevel.CRITICAL)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
