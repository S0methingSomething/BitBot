"""Release command for BitBot CLI."""

from typing import TYPE_CHECKING

import typer
from beartype import beartype
from rich.progress import Progress, SpinnerColumn, TextColumn

from bitbot.core.error_context import error_context
from bitbot.core.error_logger import LogLevel
from bitbot.core.errors import BitBotError
from bitbot.core.release_queue import clear_pending_releases, load_pending_releases
from bitbot.gh.releases.creator import create_bot_release
from bitbot.gh.releases.downloader import download_asset
from bitbot.gh.releases.patcher import patch_file

if TYPE_CHECKING:
    from rich.console import Console

    from bitbot.config_models import Config
    from bitbot.core.container import Container

app = typer.Typer()


@beartype
@app.command()
def run(ctx: typer.Context) -> None:
    """Create GitHub releases from pending updates."""
    # Get dependencies from container
    container: Container = ctx.obj["container"]
    console: Console = container.console()
    logger = container.logger()
    config: Config = container.config()

    with error_context(command="release"):
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task(description="Processing releases...", total=None)

                source_repo = config.github.source_repo
                bot_repo = config.github.bot_repo
                default_asset = config.github.asset_file_name

                # Load pending releases
                queue_result = load_pending_releases()
                if queue_result.is_err():
                    error = BitBotError(f"Queue error: {queue_result.error}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {queue_result.error}")
                    raise typer.Exit(code=1) from None
                pending = queue_result.unwrap()

                if not pending:
                    console.print("[yellow][i] No pending releases to process[/yellow]")
                    return

                # Process each release
                success_count = 0
                successful_releases = []
                for release in pending:
                    app_name = release.display_name
                    version = release.version
                    asset_name = release.asset_name or default_asset

                    progress.update(task, description=f"Processing {app_name} {version}...")

                    # Download
                    download_result = download_asset(source_repo, release.release_id, asset_name)
                    if download_result.is_err():
                        console.print(f"[red]✗[/red] {app_name}: {download_result.error}")
                        continue

                    # Patch
                    original_path = download_result.unwrap()
                    patch_result = patch_file(str(original_path), asset_name)
                    if patch_result.is_err():
                        console.print(f"[red]✗[/red] {app_name}: {patch_result.error}")
                        continue

                    # Create release
                    patched_path = patch_result.unwrap()
                    release_tag = f"{release.tag}-{app_name.replace(' ', '-')}"
                    title = f"{app_name} {version}"
                    notes = f"Updated {app_name} to version {version}"

                    create_result = create_bot_release(
                        bot_repo, release_tag, title, notes, patched_path
                    )
                    if create_result.is_err():
                        console.print(f"[red]✗[/red] {app_name}: {create_result.error}")
                        continue

                    console.print(f"[green]✓[/green] {app_name} {version}")
                    success_count += 1
                    successful_releases.append(release)

                # Clear queue after processing
                clear_result = clear_pending_releases()
                if clear_result.is_err():
                    console.print("[yellow]⚠[/yellow] Failed to clear queue")

                console.print(f"[green]✓[/green] Processed {success_count}/{len(pending)} releases")

        except Exception as e:
            error = BitBotError(f"Unexpected error: {e}")
            logger.log_error(error, LogLevel.CRITICAL)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
