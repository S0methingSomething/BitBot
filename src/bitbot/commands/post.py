"""Post command for BitBot CLI."""

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

import praw
import typer
from beartype import beartype
from rich.progress import Progress, SpinnerColumn, TextColumn

from bitbot import paths
from bitbot.config_models import Config
from bitbot.core.error_context import error_context
from bitbot.core.error_logger import LogLevel, get_logger
from bitbot.core.errors import BitBotError
from bitbot.core.release_queue import load_pending_releases
from bitbot.core.state import load_bot_state, save_bot_state
from bitbot.reddit.client import init_reddit
from bitbot.reddit.posting.body_builder import generate_post_body
from bitbot.reddit.posting.poster import post_new_release

if TYPE_CHECKING:
    from rich.console import Console

    from bitbot.core.container import Container

app = typer.Typer()


def post_or_update(
    reddit: praw.Reddit,
    title: str,
    body: str,
    config: Config,
    existing_post_id: str | None,
) -> tuple[praw.models.Submission, bool]:
    """Post new or update existing Reddit post.

    Returns:
        Tuple of (submission, was_updated) where was_updated is True if existing post was updated.
    """
    if existing_post_id:
        try:
            submission = reddit.submission(id=existing_post_id)
            submission.edit(body)
        except Exception as e:
            # Log failure and fall back to new post
            msg = f"Failed to update post {existing_post_id}: {e}"
            raise BitBotError(msg) from e
        else:
            return (submission, True)

    submission = post_new_release(reddit, title, body, config)
    return (submission, False)


@beartype
@app.command()
def run(
    ctx: typer.Context,
    page_url: str = typer.Option(None, "--page-url", help="Landing page URL to post"),
) -> None:
    """Post new releases to Reddit."""
    # Get dependencies from container
    container: Container = ctx.obj["container"]
    console: Console = ctx.obj["console"]
    logger = get_logger(console=console)
    config: Config = container.get("config")

    with error_context(command="post", page_url=page_url):
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                progress.add_task(description="Posting to Reddit...", total=None)

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

                # Get landing page URL
                bot_repo = config.github.bot_repo
                owner, repo = bot_repo.split("/")
                page_url = page_url or f"https://{owner}.github.io/{repo}/"

                # Generate title
                date_str = datetime.now(UTC).strftime("%Y-%m-%d")
                title = f"New Updates - {date_str}"

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

                # Check if rolling update mode and existing post
                post_mode = config.reddit.post_mode
                state_result = load_bot_state()
                existing_post_id = None
                if post_mode == "rolling_update" and state_result.is_ok():
                    state = state_result.unwrap()
                    existing_post_id = state.active_post_id

                # Post or update
                submission, was_updated = post_or_update(
                    reddit, title, body, config, existing_post_id
                )

                if was_updated:
                    console.print(f"[green]✓[/green] Updated existing post: {submission.url}")
                else:
                    console.print(f"[green]✓[/green] Posted to Reddit: {submission.url}")

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

        except Exception as e:
            error = BitBotError(f"Unexpected error: {e}")
            logger.log_error(error, LogLevel.CRITICAL)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
