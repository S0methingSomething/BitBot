"""Gather command for BitBot CLI."""

from typing import TYPE_CHECKING

import typer
from beartype import beartype
from rich.progress import Progress, SpinnerColumn, TextColumn

from bitbot.core.error_context import error_context
from bitbot.core.error_logger import LogLevel
from bitbot.core.errors import BitBotError
from bitbot.core.release_queue import add_release
from bitbot.core.state import load_release_state, save_release_state
from bitbot.gh.releases.fetcher import get_source_releases
from bitbot.gh.releases.parser import parse_release_description
from bitbot.models import PendingRelease

if TYPE_CHECKING:
    from rich.console import Console

    from bitbot.config_models import Config
    from bitbot.core.container import Container

app = typer.Typer()


@beartype
@app.command()
def run(ctx: typer.Context) -> None:
    """Gather new releases from source repository."""
    # Get dependencies from container
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
                state_modified = False
                for release in releases:
                    release_id = release["id"]
                    if release_id in processed_ids:
                        continue

                    tag = release.get("tag_name", "unknown")
                    description = release.get("body", "")

                    if not description:
                        console.print(
                            f"[yellow]⚠[/yellow] Release {tag} has no description, skipping"
                        )
                        continue

                    apps = parse_release_description(description, apps_config)

                    if not apps:
                        console.print(
                            f"[yellow]⚠[/yellow] Release {tag} has no parseable apps, skipping"
                        )
                        continue

                    # Try to queue all apps for this release
                    all_queued = True
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
                            error_msg = f"Failed to queue {app['display_name']}: {add_result.error}"
                            console.print(f"[yellow]⚠[/yellow] {error_msg}")
                            all_queued = False
                            # Don't break - try to queue remaining apps

                    # Only mark as processed if ALL apps queued successfully
                    if all_queued:
                        processed_ids.append(release_id)
                        state_modified = True
                        new_count += len(apps)
                        console.print(f"[cyan]Release {tag}:[/cyan] {len(apps)} app(s) queued")
                    else:
                        console.print(
                            f"[red]✗[/red] Release {tag} partially failed - will retry next run"
                        )

                # Save state only if modified
                if state_modified:
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

        except Exception as e:
            error = BitBotError(f"Unexpected error: {e}")
            logger.log_error(error, LogLevel.CRITICAL)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
