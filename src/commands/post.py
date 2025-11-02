"""Post command for BitBot CLI."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import typer
from beartype import beartype
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

sys.path.insert(0, str(Path(__file__).parent.parent))

import paths
from core.config import load_config
from core.error_context import error_context
from core.error_logger import LogLevel, get_logger
from core.errors import BitBotError
from core.release_queue import load_pending_releases
from core.state import load_bot_state, save_bot_state
from reddit.client import init_reddit
from reddit.posting.body_builder import generate_post_body
from reddit.posting.poster import post_new_release

app = typer.Typer()
console = Console()
logger = get_logger(console=console)


@beartype
@app.command()
def run(
    page_url: str = typer.Option(None, "--page-url", help="Landing page URL to post"),
) -> None:
    """Post new releases to Reddit."""
    with error_context(command="post", page_url=page_url):
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                progress.add_task(description="Posting to Reddit...", total=None)

                # Load config
                config_result = load_config()
                if config_result.is_err():
                    error = BitBotError(f"Config error: {config_result.error}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {config_result.error}")
                    raise typer.Exit(code=1) from None
                config = config_result.unwrap()

                # Check for pending releases
                queue_result = load_pending_releases()
                if queue_result.is_err():
                    error = BitBotError(f"Queue error: {queue_result.error}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {queue_result.error}")
                    raise typer.Exit(code=1) from None
                pending = queue_result.unwrap()

                if not pending:
                    console.print("[yellow][i] No releases to post[/yellow]")
                    return

                # Load releases data
                releases_file = Path(paths.DIST_DIR) / "releases.json"
                if not releases_file.exists():
                    error = BitBotError("releases.json not found - run gather first")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {error.message}")
                    raise typer.Exit(code=1) from None

                with releases_file.open() as f:
                    all_releases_data = json.load(f)

                # Build changelog data from pending releases
                changelog_data: dict[str, dict[str, Any]] = {
                    "added": {},
                    "updated": {},
                    "removed": {},
                }
                for release in pending:
                    app_data = all_releases_data.get(release.app_id, {})
                    latest = app_data.get("latest_release", {})
                    changelog_data["updated"][release.app_id] = {
                        "new": {
                            "display_name": release.display_name,
                            "version": release.version,
                            "url": latest.get("download_url", ""),
                        },
                        "old": latest.get("version", "unknown"),
                    }

                # Get landing page URL from config or use default
                bot_repo = config["github"]["botRepo"]
                page_url = (
                    page_url
                    or f"https://{bot_repo.split('/')[0]}.github.io/{bot_repo.split('/')[1]}/"
                )

                # Generate title
                post_identifier = config["reddit"].get("postIdentifier", "[BitBot]")
                date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                title = f"{post_identifier} New Updates - {date_str}"

                # Generate body using proper body builder
                body = generate_post_body(config, changelog_data, all_releases_data, page_url)

                # Init Reddit
                reddit_result = init_reddit(config)
                if reddit_result.is_err():
                    error = BitBotError(f"Reddit error: {reddit_result.error}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {reddit_result.error}")
                    raise typer.Exit(code=1) from None
                reddit = reddit_result.unwrap()

                # Post
                submission = post_new_release(reddit, title, body, config)

                # Update state with post ID tracking
                state_result = load_bot_state()
                if state_result.is_ok():
                    state = state_result.unwrap()
                    state.active_post_id = submission.id
                    # Track all post IDs for robust detection
                    if submission.id not in state.all_post_ids:
                        state.all_post_ids.append(submission.id)
                    save_result = save_bot_state(state)
                    if save_result.is_err():
                        console.print("[yellow]⚠[/yellow] Failed to update state")

                console.print(f"[green]✓[/green] Posted to Reddit: {submission.url}")

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
