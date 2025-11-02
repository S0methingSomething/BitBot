"""Gather command for BitBot CLI."""

import sys
from pathlib import Path

import typer
from beartype import beartype
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import load_config
from core.error_context import error_context
from core.error_logger import LogLevel, get_logger
from core.errors import BitBotError
from core.release_queue import add_release
from core.state import load_release_state, save_release_state
from gh.releases.fetcher import get_source_releases
from gh.releases.parser import parse_release_description
from models import PendingRelease

app = typer.Typer()
console = Console()
logger = get_logger(console=console)


@beartype
@app.command()
def run() -> None:
    """Gather new releases from source repository."""
    with error_context(command="gather"):
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                progress.add_task(description="Gathering releases...", total=None)

                # Load config
                config_result = load_config()
                if config_result.is_err():
                    error = BitBotError(f"Config error: {config_result.error}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {config_result.error}")
                    raise typer.Exit(code=1) from None
                config = config_result.unwrap()

                source_repo = config.github.source_repo
                apps_config = config.model_dump().get("apps", [])

                # Load release state
                state_result = load_release_state()
                if state_result.is_err():
                    error = BitBotError(f"State error: {state_result.error}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {state_result.error}")
                    raise typer.Exit(code=1) from None
                processed_ids = state_result.unwrap()

                # Fetch releases
                releases_result = get_source_releases(source_repo)
                if releases_result.is_err():
                    error = BitBotError(f"GitHub error: {releases_result.error}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {releases_result.error}")
                    raise typer.Exit(code=1) from None
                releases = releases_result.unwrap()

                # Filter and process new releases
                new_count = 0
                for release in releases:
                    release_id = release["id"]
                    if release_id in processed_ids:
                        continue

                    tag = release.get("tag_name", "unknown")
                    description = release.get("body", "")
                    apps = parse_release_description(description, apps_config)

                    if apps:
                        for app in apps:
                            pending = PendingRelease(
                                release_id=release_id,
                                tag=tag,
                                app_id=app["app_id"],
                                display_name=app["display_name"],
                                version=app.get("version", "unknown"),
                                asset_name=app.get("asset_name"),
                            )
                            add_result = add_release(pending)
                            if add_result.is_err():
                                console.print(
                                    f"[yellow]⚠[/yellow] Failed to queue " f"{app['display_name']}"
                                )
                                continue
                            new_count += 1

                        processed_ids.append(release_id)
                        console.print(f"[cyan]Release {tag}:[/cyan] {len(apps)} app(s)")

                # Save state
                if processed_ids:
                    save_result = save_release_state(processed_ids)
                    if save_result.is_err():
                        error = BitBotError(f"State save error: {save_result.error}")
                        logger.log_error(error, LogLevel.ERROR)
                        console.print(f"[red]✗ Error:[/red] {save_result.error}")
                        raise typer.Exit(code=1) from None

                if new_count == 0:
                    console.print("[green]✓[/green] No new releases found")
                else:
                    console.print(f"[green]✓[/green] Queued {new_count} app update(s)")

        except BitBotError as e:
            logger.log_error(e, LogLevel.ERROR)
            console.print(f"[red]✗ Error:[/red] {e.message}")
            raise typer.Exit(code=1) from None
        except Exception as e:
            import traceback

            traceback.print_exc()
            error = BitBotError(f"Unexpected error: {e}")
            logger.log_error(error, LogLevel.CRITICAL)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
