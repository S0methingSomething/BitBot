"""Release command for BitBot CLI."""

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
from core.release_queue import clear_pending_releases, load_pending_releases
from gh.releases.creator import create_bot_release
from gh.releases.downloader import download_asset
from gh.releases.patcher import patch_file

app = typer.Typer()
console = Console()
logger = get_logger(console=console)


@beartype
@app.command()
def run() -> None:
    """Create GitHub releases from pending updates."""
    with error_context(command="release"):
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task(description="Processing releases...", total=None)

                # Load config
                config_result = load_config()
                if config_result.is_err():
                    error = BitBotError(f"Config error: {config_result.error}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {config_result.error}")
                    raise typer.Exit(code=1) from None
                config = config_result.unwrap()

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

                # Clear queue
                clear_result = clear_pending_releases()
                if clear_result.is_err():
                    console.print("[yellow]⚠[/yellow] Failed to clear queue")

                console.print(f"[green]✓[/green] Processed {success_count}/{len(pending)} releases")

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
