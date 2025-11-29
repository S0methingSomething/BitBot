"""Post command for BitBot CLI."""

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

import praw
import typer
from beartype import beartype
from returns.result import Failure, Success
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from bitbot import paths
from bitbot.config_models import Config
from bitbot.core.error_context import error_context
from bitbot.core.error_logger import ErrorLogger, LogLevel
from bitbot.core.errors import BitBotError
from bitbot.core.state import load_account_state, save_account_state
from bitbot.models import AccountState
from bitbot.reddit.client import init_reddit
from bitbot.reddit.parser import parse_versions_from_post
from bitbot.reddit.posting.body_builder import generate_post_body
from bitbot.reddit.posting.poster import post_new_release, update_post
from bitbot.reddit.posting.title_generator import generate_dynamic_title
from bitbot.reddit.posts import get_bot_posts

if TYPE_CHECKING:
    from bitbot.core.container import Container

app = typer.Typer()


@beartype
def _verify_account_state(
    reddit: praw.Reddit,
    config: Config,
    state: AccountState,
    console: Console,
) -> AccountState:
    """Verify account state against actual Reddit post."""
    console.print("[dim]Verifying state against Reddit...[/dim]")
    try:
        posts_result = get_bot_posts(reddit, config)
        if isinstance(posts_result, Success):
            posts = posts_result.unwrap()
            if posts:
                latest_post = posts[0]
                reddit_versions = parse_versions_from_post(latest_post, config)

                # Compare with local state
                if reddit_versions != state.online:
                    console.print(
                        f"[yellow]⚠ State mismatch detected![/yellow]\n"
                        f"  Local: {state.online}\n"
                        f"  Reddit: {reddit_versions}\n"
                        f"  Using Reddit as source of truth"
                    )
                    state.online = reddit_versions
                    save_account_state(state)
                else:
                    console.print("[green]✓[/green] State verified")
    except Exception as e:
        console.print(f"[yellow]⚠ Verification failed: {e}[/yellow]")
        # Continue with local state
    return state


@beartype
def _load_releases_data(console: Console, logger: ErrorLogger) -> dict[str, Any]:
    """Load releases.json file."""
    releases_file = Path(paths.DIST_DIR) / "releases.json"
    if not releases_file.exists():
        error = BitBotError(
            "releases.json not found. Run 'bitbot gather' first to collect release data."
        )
        logger.log_error(error, LogLevel.ERROR)
        console.print(f"[red]✗ Error:[/red] {error.message}")
        raise typer.Exit(code=1) from None

    with releases_file.open() as f:
        all_releases_data = json.load(f)

    if not isinstance(all_releases_data, dict):
        error = BitBotError("releases.json has invalid format")
        logger.log_error(error, LogLevel.ERROR)
        console.print(f"[red]✗ Error:[/red] {error.message}")
        raise typer.Exit(code=1) from None

    return all_releases_data


@beartype
def should_create_new_post(
    reddit: praw.Reddit, existing_post_id: str | None, config: Config
) -> bool:
    """Check if enough time has passed to create a new post."""
    if not existing_post_id:
        return True  # No existing post, create new one

    try:
        submission = reddit.submission(id=existing_post_id)
        post_created_at = datetime.fromtimestamp(submission.created_utc, tz=UTC)
        now = datetime.now(UTC)
        days_elapsed = (now - post_created_at).days

        days_before_new = config.reddit.rolling.get("days_before_new_post", 7)
    except Exception:
        # If can't get post info, assume we should update existing
        return False
    else:
        return days_elapsed >= days_before_new


@beartype
def post_or_update(
    reddit: praw.Reddit,
    title: str,
    body: str,
    config: Config,
    existing_post_id: str | None,
) -> tuple[praw.models.Submission, bool] | None:
    """Post new or update existing Reddit post.

    Returns:
        Tuple of (submission, was_updated) or None if shouldn't post.
    """
    post_mode = config.reddit.post_mode

    if post_mode == "rolling_update":
        # Check if we should create new post based on time
        if should_create_new_post(reddit, existing_post_id, config):
            # Time to create new post
            result = post_new_release(reddit, title, body, config)
            if isinstance(result, Failure):
                msg = f"Failed to create post: {result.failure()}"
                raise BitBotError(msg)
            return (result.unwrap(), False)

        # Update existing post
        if not existing_post_id:
            return None  # No existing post to update

        result = update_post(reddit, existing_post_id, body, config)
        if isinstance(result, Failure):
            msg = f"Failed to update post {existing_post_id}: {result.failure()}"
            raise BitBotError(msg)
        return (result.unwrap(), True)

    # new_post mode: always create new post
    result = post_new_release(reddit, title, body, config)
    if isinstance(result, Failure):
        msg = f"Failed to create post: {result.failure()}"
        raise BitBotError(msg)
    return (result.unwrap(), False)


@beartype
def _build_changelog_data(
    all_releases_data: dict[str, Any], state: AccountState
) -> dict[str, dict[str, Any]]:
    """Build changelog data by comparing current releases vs posted versions."""
    changelog_data: dict[str, dict[str, Any]] = {
        "added": {},
        "updated": {},
        "removed": {},
    }

    # Get current versions with full release info
    current_releases = {}
    for app_id, app_data in all_releases_data.items():
        latest = app_data.get("latest_release")
        if latest:
            current_releases[app_id] = {
                "display_name": app_data.get("display_name", app_id),
                "version": latest.get("version", "unknown"),
                "url": latest.get("download_url", ""),
            }

    # Check for new and updated apps
    for app_id, release_info in current_releases.items():
        if app_id not in state.online:
            # New app
            changelog_data["added"][app_id] = release_info
        elif state.online[app_id] != release_info["version"]:
            # Updated app - use OLD version from state
            changelog_data["updated"][app_id] = {
                "new": release_info,
                "old": state.online[app_id],
            }

    # Check for removed apps
    for app_id, old_version in state.online.items():
        if app_id not in current_releases:
            changelog_data["removed"][app_id] = {
                "display_name": app_id,
                "version": old_version,
            }

    return changelog_data


@beartype
def _has_new_releases(changelog_data: dict[str, dict[str, Any]], console: Console) -> bool:
    """Check if changelog has any changes."""
    has_changes = False

    for app_id, info in changelog_data["added"].items():
        console.print(f"[cyan]→[/cyan] New app detected: {app_id} v{info['version']}")
        has_changes = True

    for app_id, info in changelog_data["updated"].items():
        console.print(
            f"[cyan]→[/cyan] Version change: {app_id} {info['old']} → {info['new']['version']}"
        )
        has_changes = True

    for app_id in changelog_data["removed"]:
        console.print(f"[cyan]→[/cyan] App removed: {app_id}")
        has_changes = True

    return has_changes


@dataclass
class PostContext:
    """Context for posting to Reddit."""

    config: Config
    page_url: str


@beartype
def _build_and_post(
    reddit: "praw.Reddit",
    context: PostContext,
    changelog_data: dict[str, dict[str, Any]],
    all_releases_data: dict[str, Any],
    existing_post_id: str | None,
) -> tuple["praw.models.Submission", bool] | None:
    """Build post content and submit to Reddit."""
    # Generate title and body
    title = generate_dynamic_title(
        context.config, changelog_data["added"], changelog_data["updated"]
    )
    body = generate_post_body(context.config, changelog_data, all_releases_data, context.page_url)

    # Post or update
    return post_or_update(reddit, title, body, context.config, existing_post_id)


@beartype
@app.command()
def run(
    ctx: typer.Context,
    page_url: str = typer.Option(None, "--page-url", help="Landing page URL to post"),
    verify: bool = typer.Option(  # noqa: FBT001
        default=False, help="Verify state against actual Reddit post"
    ),
    force: bool = typer.Option(  # noqa: FBT001
        default=False, help="Force post even if no changes detected"
    ),
) -> None:
    """Post new releases to Reddit."""
    container: Container = ctx.obj["container"]
    console: Console = container.console()
    logger = container.logger()
    config: Config = container.config()

    with error_context(command="post", page_url=page_url):
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                progress.add_task(description="Checking for new releases...", total=None)

                # Load releases data
                all_releases_data = _load_releases_data(console, logger)

                # Load state to check for changes
                state_result = load_account_state()
                if isinstance(state_result, Failure):
                    console.print("[yellow]⚠[/yellow] No existing state, will create new post")
                    state = AccountState()
                else:
                    state = state_result.unwrap()

                # Build changelog data by comparing current vs posted
                changelog_data = _build_changelog_data(all_releases_data, state)

                # Check if there are actual changes
                if not force and not _has_new_releases(changelog_data, console):
                    console.print(
                        "[dim]No new releases detected. Skipping post update.[/dim]\n"
                        "[dim]Use --force to post anyway.[/dim]"
                    )
                    return

                # Get landing page URL
                if not page_url:
                    page_url = config.github.pages_url

                # Init Reddit
                reddit_result = init_reddit(config)
                if isinstance(reddit_result, Failure):
                    error = BitBotError(f"Reddit error: {reddit_result.failure()}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {reddit_result.failure()}")
                    raise typer.Exit(code=1) from None
                reddit = reddit_result.unwrap()

                # Optional verification against actual Reddit post
                if verify and state.active_post_id:
                    state = _verify_account_state(reddit, config, state, console)

                # Build and post
                existing_post_id = state.active_post_id if state else None
                context = PostContext(config=config, page_url=page_url)
                result = _build_and_post(
                    reddit, context, changelog_data, all_releases_data, existing_post_id
                )

                if result is None:
                    console.print(
                        "[yellow][i] No existing post to update in rolling_update mode[/yellow]"
                    )
                    return

                submission, was_updated = result

                if was_updated:
                    console.print(f"[green]✓[/green] Updated existing post: {submission.url}")
                else:
                    console.print(f"[green]✓[/green] Posted to Reddit: {submission.url}")

                # Update state with post ID tracking and posted versions
                state.active_post_id = submission.id
                # Track all post IDs for robust detection
                if submission.id not in state.all_post_ids:
                    state.all_post_ids.append(submission.id)

                # Update posted versions to match what we just posted
                for app_id, app_data in all_releases_data.items():
                    latest = app_data.get("latest_release")
                    if latest:
                        state.online[app_id] = latest.get("version", "unknown")

                save_result = save_account_state(state)
                if isinstance(save_result, Failure):
                    error = BitBotError(f"Failed to save state: {save_result.failure()}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[yellow]⚠[/yellow] {error.message}")
                    # Don't fail - post was successful, state update is secondary

        except Exception as e:
            error = BitBotError(f"Unexpected error: {e}")
            logger.log_error(error, LogLevel.CRITICAL)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
