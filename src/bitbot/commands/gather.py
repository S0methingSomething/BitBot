"""Gather command for BitBot CLI."""

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
from bitbot.gh.releases.fetcher import get_github_data

if TYPE_CHECKING:
    from rich.console import Console

    from bitbot.config_models import Config
    from bitbot.core.container import Container

app = typer.Typer()


@beartype
def _parse_release_metadata(release: dict[str, Any]) -> tuple[str | None, str | None]:
    """Parse app name and version from release body."""
    body = release.get("body", "")
    app_name = None
    version = None

    for line in body.split("\n"):
        if line.startswith("app:"):
            app_name = line.split(":", 1)[1].strip()
        elif line.startswith("version:"):
            version = line.split(":", 1)[1].strip()

    return app_name, version


@beartype
@app.command()
def run(ctx: typer.Context) -> None:
    """Gather releases from bot repository and create releases.json."""
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

                bot_repo = config.github.bot_repo
                apps_config = {
                    app["id"]: app["displayName"] for app in config.model_dump().get("apps", [])
                }

                # Fetch all releases from bot repo using authenticated gh CLI
                releases_result = get_github_data(f"/repos/{bot_repo}/releases?per_page=100")
                if releases_result.is_err():
                    error = BitBotError(f"GitHub API error: {releases_result.unwrap_err()}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {releases_result.unwrap_err()}")
                    raise typer.Exit(code=1) from None

                releases = releases_result.unwrap()
                if not isinstance(releases, list):
                    error = BitBotError("Expected list of releases from GitHub API")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {error.message}")
                    raise typer.Exit(code=1) from None

                # Group releases by app
                apps_data: dict[str, Any] = {}
                for release in releases:
                    if not release.get("assets"):
                        continue

                    app_name, version = _parse_release_metadata(release)
                    if not app_name or not version:
                        continue

                    app_id = app_name.lower().replace(" ", "_")
                    display_name = apps_config.get(app_id, app_name)

                    release_data = {
                        "version": version,
                        "download_url": release["assets"][0]["browser_download_url"],
                        "published_at": release["published_at"],
                    }

                    if app_id not in apps_data:
                        apps_data[app_id] = {
                            "display_name": display_name,
                            "latest_release": release_data,
                            "previous_releases": [],
                        }
                    else:
                        # Subsequent releases are previous releases
                        apps_data[app_id]["previous_releases"].append(release_data)

                # Save to releases.json
                dist_dir = Path(paths.DIST_DIR)
                dist_dir.mkdir(parents=True, exist_ok=True)
                releases_file = dist_dir / "releases.json"

                with releases_file.open("w") as f:
                    json.dump(apps_data, f, indent=2)

                app_count = len(apps_data)
                console.print(f"[green]✓[/green] Gathered {app_count} app(s) from bot releases")

        except Exception as e:
            error = BitBotError(f"Unexpected error: {e}")
            logger.log_error(error, LogLevel.CRITICAL)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
