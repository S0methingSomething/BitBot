"""Release command for BitBot CLI."""

import hashlib
from pathlib import Path
from typing import TYPE_CHECKING

import typer
from beartype import beartype
from rich.progress import Progress, SpinnerColumn, TextColumn

from bitbot.core.error_context import error_context
from bitbot.core.error_logger import LogLevel
from bitbot.core.errors import BitBotError
from bitbot.core.release_queue import load_pending_releases, save_pending_releases
from bitbot.gh.releases.creator import create_bot_release
from bitbot.gh.releases.downloader import download_asset
from bitbot.gh.releases.patcher import patch_file
from bitbot.models import PendingRelease

if TYPE_CHECKING:
    from rich.console import Console

    from bitbot.config_models import Config
    from bitbot.core.container import Container

app = typer.Typer()


@beartype
def process_single_release(
    release: PendingRelease,
    source_repo: str,
    bot_repo: str,
    default_asset: str,
    console: "Console",
) -> tuple[bool, list[Path]]:
    """Process a single release. Returns (success, downloaded_files)."""
    app_name = release.display_name
    version = release.version
    asset_name = release.asset_name or default_asset
    downloaded_files: list[Path] = []

    # Download
    download_result = download_asset(source_repo, release.release_id, asset_name)
    if download_result.is_err():
        console.print(f"[red]✗[/red] {app_name}: {download_result.error}")
        return (False, downloaded_files)

    # Patch
    original_path = download_result.unwrap()
    downloaded_files.append(Path(original_path))
    patch_result = patch_file(str(original_path), asset_name)
    if patch_result.is_err():
        console.print(f"[red]✗[/red] {app_name}: {patch_result.error}")
        return (False, downloaded_files)

    # Create release
    patched_path = patch_result.unwrap()
    downloaded_files.append(Path(patched_path))
    release_tag = f"{release.tag}-{app_name.replace(' ', '-')}"
    title = f"{app_name} {version}"

    # Calculate SHA256 of patched file
    file_hash = hashlib.sha256(Path(patched_path).read_bytes()).hexdigest()
    notes = f"app: {app_name}\nversion: {version}\nasset_name: {asset_name}\nsha256: {file_hash}"

    create_result = create_bot_release(bot_repo, release_tag, title, notes, patched_path)
    if create_result.is_err():
        console.print(f"[red]✗[/red] {app_name}: {create_result.error}")
        return (False, downloaded_files)

    console.print(f"[green]✓[/green] {app_name} {version}")
    return (True, downloaded_files)


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
                failed_releases = []
                all_downloaded_files = []

                for release in pending:
                    progress.update(
                        task, description=f"Processing {release.display_name} {release.version}..."
                    )

                    success, downloaded_files = process_single_release(
                        release, source_repo, bot_repo, default_asset, console
                    )
                    all_downloaded_files.extend(downloaded_files)

                    if success:
                        success_count += 1
                    else:
                        failed_releases.append(release)

                # Clean up downloaded files
                for file_path in all_downloaded_files:
                    try:
                        if file_path.exists():
                            file_path.unlink()
                    except OSError:
                        pass  # Ignore cleanup errors

                # Update queue: keep only failed releases
                if failed_releases:
                    save_result = save_pending_releases(failed_releases)
                    if save_result.is_err():
                        msg = f"Failed to save queue: {save_result.error}"
                        console.print(f"[yellow]⚠[/yellow] {msg}")
                else:
                    # All succeeded, clear queue
                    save_result = save_pending_releases([])
                    if save_result.is_err():
                        msg = f"Failed to clear queue: {save_result.error}"
                        console.print(f"[yellow]⚠[/yellow] {msg}")

                if success_count == 0:
                    console.print(f"[red]✗[/red] All {len(pending)} releases failed")
                elif failed_releases:
                    msg = (
                        f"Processed {success_count}/{len(pending)} releases "
                        f"({len(failed_releases)} failed, will retry)"
                    )
                    console.print(f"[yellow]⚠[/yellow] {msg}")
                else:
                    msg = f"Processed {success_count}/{len(pending)} releases"
                    console.print(f"[green]✓[/green] {msg}")

        except Exception as e:
            error = BitBotError(f"Unexpected error: {e}")
            logger.log_error(error, LogLevel.CRITICAL)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
