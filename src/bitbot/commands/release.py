"""Release command for BitBot CLI."""

import hashlib
from pathlib import Path
from typing import TYPE_CHECKING

import typer
from beartype import beartype
from returns.result import Failure
from rich.progress import Progress, SpinnerColumn, TextColumn

from bitbot.core import db
from bitbot.core.app_registry import AppRegistry
from bitbot.core.db import PendingRelease
from bitbot.core.error_context import error_context
from bitbot.core.error_logger import LogLevel
from bitbot.core.errors import BitBotError
from bitbot.gh.releases.creator import create_bot_release
from bitbot.gh.releases.downloader import download_asset
from bitbot.gh.releases.patcher import patch_file

if TYPE_CHECKING:
    from rich.console import Console

    from bitbot.config_models import Config
    from bitbot.core.container import Container

app = typer.Typer()


@beartype
def process_single_release(  # noqa: PLR0913
    release: PendingRelease,
    source_repo: str,
    bot_repo: str,
    default_asset: str,
    console: "Console",
    registry: AppRegistry,
) -> tuple[bool, list[Path]]:
    """Process a single release. Returns (success, downloaded_files)."""
    app_id = release["app_id"]
    app_name = release["display_name"]
    version = release["version"]
    asset_name = release.get("asset_name") or default_asset
    release_id = release["release_id"]
    tag = release["tag"]
    downloaded_files: list[Path] = []

    # Validate app_id exists in config
    if not registry.exists(app_id):
        console.print(
            f"[red]✗[/red] {app_name}: Unknown app_id '{app_id}'. Valid: {', '.join(registry.ids)}"
        )
        return (False, downloaded_files)

    # Download
    download_result = download_asset(source_repo, release_id, asset_name)
    if isinstance(download_result, Failure):
        console.print(f"[red]✗[/red] {app_name}: {download_result.failure()}")
        return (False, downloaded_files)

    # Patch
    original_path = download_result.unwrap()
    downloaded_files.append(Path(original_path))
    patch_result = patch_file(str(original_path), asset_name)
    if isinstance(patch_result, Failure):
        console.print(f"[red]✗[/red] {app_name}: {patch_result.failure()}")
        return (False, downloaded_files)

    # Create release with canonical app_id from registry
    matched_app = registry.get_or_raise(app_id)
    patched_path = patch_result.unwrap()
    downloaded_files.append(Path(patched_path))
    release_tag = f"{tag}-{app_name.replace(' ', '-')}"
    title = f"{app_name} {version}"

    # Calculate SHA256 of patched file
    file_hash = hashlib.sha256(Path(patched_path).read_bytes()).hexdigest()
    notes = (
        f"app: {matched_app.id}\nversion: {version}\nasset_name: {asset_name}\nsha256: {file_hash}"
    )

    create_result = create_bot_release(bot_repo, release_tag, title, notes, patched_path)
    if isinstance(create_result, Failure):
        console.print(f"[red]✗[/red] {app_name}: {create_result.failure()}")
        return (False, downloaded_files)

    console.print(f"[green]✓[/green] {app_name} {version}")
    return (True, downloaded_files)


@beartype
@app.command()
def run(ctx: typer.Context) -> None:
    """Create GitHub releases from pending updates."""
    container: Container = ctx.obj["container"]
    console: Console = container.console()
    logger = container.logger()
    config: Config = container.config()
    registry: AppRegistry = container.app_registry()

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

                # Initialize database
                db.init()

                # Load pending releases
                queue_result = db.get_pending_releases()
                if isinstance(queue_result, Failure):
                    error = BitBotError(f"Queue error: {queue_result.failure()}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {queue_result.failure()}")
                    raise typer.Exit(code=1) from None

                pending = queue_result.unwrap()

                if not pending:
                    console.print("[yellow][i] No pending releases to process[/yellow]")
                    return

                # Process each release
                success_count = 0
                fail_count = 0
                all_downloaded_files: list[Path] = []

                for release in pending:
                    desc = f"Processing {release['display_name']} {release['version']}..."
                    progress.update(task, description=desc)

                    success, downloaded_files = process_single_release(
                        release, source_repo, bot_repo, default_asset, console, registry
                    )
                    all_downloaded_files.extend(downloaded_files)

                    if success:
                        success_count += 1
                        # Remove from queue on success
                        db.remove_pending_release(release["release_id"])
                    else:
                        fail_count += 1

                # Clean up downloaded files
                for file_path in all_downloaded_files:
                    try:
                        if file_path.exists():
                            file_path.unlink()
                    except OSError:
                        pass

                total = len(pending)
                if success_count == 0:
                    console.print(f"[red]✗[/red] All {total} releases failed")
                elif fail_count > 0:
                    msg = f"{success_count}/{total} succeeded ({fail_count} failed, will retry)"
                    console.print(f"[yellow]⚠[/yellow] {msg}")
                else:
                    console.print(f"[green]✓[/green] Processed {success_count}/{total} releases")

        except Exception as e:
            error = BitBotError(f"Unexpected error: {e}")
            logger.log_error(error, LogLevel.CRITICAL)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
