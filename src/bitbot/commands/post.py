"""Post command for BitBot CLI."""

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

import praw
import typer
from beartype import beartype
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from bitbot import paths
from bitbot.config_models import Config
from bitbot.core.error_context import error_context
from bitbot.core.error_logger import ErrorLogger, LogLevel
from bitbot.core.errors import BitBotError
from bitbot.core.state import load_account_state, save_account_state
from bitbot.models import AccountState, PendingRelease
from bitbot.reddit.client import init_reddit
from bitbot.reddit.parser import parse_versions_from_post
from bitbot.reddit.posting.body_builder import generate_post_body
from bitbot.reddit.posting.poster import post_new_release
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
        if posts_result.is_ok():
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
def _build_changelog_data(
    pending: list[PendingRelease], all_releases_data: dict[str, Any]
) -> dict[str, dict[str, Any]]:
    """Build changelog data from pending releases."""
    changelog_data: dict[str, dict[str, Any]] = {
        "added": {},
        "updated": {},
        "removed": {},
    }

    for release in pending:
        app_id = release.app_id
        app_data = all_releases_data.get(app_id, {})
        latest_release = app_data.get("latest_release", {})

        if not latest_release:
            continue

        # Determine if this is a new app or an update
        if app_id not in all_releases_data or not app_data.get("releases"):
            changelog_data["added"][app_id] = {
                "display_name": release.display_name,
                "version": release.version,
            }
        else:
            changelog_data["updated"][app_id] = {
                "display_name": release.display_name,
                "old_version": app_data.get("releases", [{}])[-2].get("version", "unknown")
                if len(app_data.get("releases", [])) > 1
                else "unknown",
                "new_version": release.version,
            }

    return changelog_data


@beartype
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
        submission = reddit.submission(id=existing_post_id)
        try:
            submission.edit(body)
        except Exception as e:
            msg = f"Failed to update post {existing_post_id}, creating new post: {e}"
            raise BitBotError(msg) from e
        else:
            return (submission, True)

    # Create new post
    result = post_new_release(reddit, title, body, config)
    if result.is_err():
        msg = f"Failed to create post: {result.error}"
        raise BitBotError(msg)
    return (result.unwrap(), False)


@beartype
@app.command()
def run(
    ctx: typer.Context,
    page_url: str = typer.Option(None, "--page-url", help="Landing page URL to post"),
    verify: bool = typer.Option(  # noqa: FBT001
        default=False, flag_value=True, help="Verify state against actual Reddit post"
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
                progress.add_task(description="Posting to Reddit...", total=None)

                # Load releases data
                all_releases_data = _load_releases_data(console, logger)

                # Build changelog from all current releases
                changelog_data: dict[str, dict[str, Any]] = {
                    "added": {},
                    "updated": {},
                    "removed": {},
                }
                for app_id, app_data in all_releases_data.items():
                    latest = app_data.get("latest_release")
                    if latest:
                        changelog_data["updated"][app_id] = {
                            "new": {
                                "display_name": app_data.get("display_name", app_id),
                                "version": latest.get("version", "unknown"),
                                "url": latest.get("download_url", ""),
                            },
                            "old": latest.get("version", "unknown"),
                        }

                # Get landing page URL
                if not page_url:
                    bot_repo = config.github.bot_repo
                    owner, repo = bot_repo.split("/")
                    page_url = f"https://{owner}.github.io/{repo}/"

                # Generate title
                title = generate_dynamic_title(
                    config, changelog_data["added"], changelog_data["updated"]
                )

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
                state_result = load_account_state()
                existing_post_id = None
                if post_mode == "rolling_update" and state_result.is_ok():
                    state = state_result.unwrap()
                    existing_post_id = state.active_post_id

                    # Optional verification against actual Reddit post
                    if verify and existing_post_id:
                        state = _verify_account_state(reddit, config, state, console)

                # Post or update
                submission, was_updated = post_or_update(
                    reddit, title, body, config, existing_post_id
                )

                if was_updated:
                    console.print(f"[green]✓[/green] Updated existing post: {submission.url}")
                else:
                    console.print(f"[green]✓[/green] Posted to Reddit: {submission.url}")

                # Update state with post ID tracking
                state_result = load_account_state()
                if state_result.is_ok():
                    state = state_result.unwrap()
                    state.active_post_id = submission.id
                    # Track all post IDs for robust detection
                    if submission.id not in state.all_post_ids:
                        state.all_post_ids.append(submission.id)
                    save_result = save_account_state(state)
                    if save_result.is_err():
                        error = BitBotError(f"Failed to save state: {save_result.error}")
                        logger.log_error(error, LogLevel.ERROR)
                        console.print(f"[yellow]⚠[/yellow] {error.message}")
                        # Don't fail - post was successful, state update is secondary
                else:
                    console.print("[yellow]⚠[/yellow] Could not load state for update")

        except Exception as e:
            error = BitBotError(f"Unexpected error: {e}")
            logger.log_error(error, LogLevel.CRITICAL)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
