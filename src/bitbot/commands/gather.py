"""Gather command for BitBot CLI."""

import json
from pathlib import Path
from typing import TYPE_CHECKING

import requests
import typer
from beartype import beartype
from rich.progress import Progress, SpinnerColumn, TextColumn

from bitbot import paths
from bitbot.core.error_context import error_context
from bitbot.core.error_logger import LogLevel
from bitbot.core.errors import BitBotError

if TYPE_CHECKING:
    from rich.console import Console

    from bitbot.config_models import Config
    from bitbot.core.container import Container

app = typer.Typer()


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

                source_repo = config.github.source_repo
                apps_config = {
                    app["id"]: app["displayName"] for app in config.model_dump().get("apps", [])
                }

                # Fetch all releases from source repo
                url = f"https://api.github.com/repos/{source_repo}/releases"
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                releases = response.json()

                # Group releases by app
                apps_data = {}
                for release in releases:
                    if not release.get("assets"):
                        continue

                    body = release.get("body", "")
                    lines = body.split("\n")

                    # Parse metadata
                    app_name = None
                    version = None

                    for line in lines:
                        if line.startswith("app:"):
                            app_name = line.split(":", 1)[1].strip()
                        elif line.startswith("version:"):
                            version = line.split(":", 1)[1].strip()

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
                            "releases": [release_data],
                        }
                    else:
                        # Add to history (releases are newest first from API)
                        apps_data[app_id]["releases"].append(release_data)

                # Save to releases.json
                dist_dir = Path(paths.DIST_DIR)
                dist_dir.mkdir(parents=True, exist_ok=True)
                releases_file = dist_dir / "releases.json"

                with releases_file.open("w") as f:
                    json.dump(apps_data, f, indent=2)

                app_count = len(apps_data)
                console.print(f"[green]✓[/green] Gathered {app_count} app(s) from bot releases")

        except requests.RequestException as e:
            error = BitBotError(f"GitHub API error: {e}")
            logger.log_error(error, LogLevel.ERROR)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1) from None
        except Exception as e:
            error = BitBotError(f"Unexpected error: {e}")
            logger.log_error(error, LogLevel.CRITICAL)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
