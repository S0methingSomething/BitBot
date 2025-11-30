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
from bitbot.core import db
from bitbot.core.credentials import get_reddit_username
from bitbot.core.error_context import error_context
from bitbot.core.error_logger import ErrorLogger, LogLevel
from bitbot.core.errors import BitBotError
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
    reddit: praw.Reddit, config: Config, account_id: int, console: Console
) -> None:
    """Verify account state against actual Reddit post."""
    console.print("[dim]Verifying state against Reddit...[/dim]")
    try:
        posts_result = get_bot_posts(reddit, config)
        if isinstance(posts_result, Success) and posts_result.unwrap():
            latest_post = posts_result.unwrap()[0]
            reddit_versions = parse_versions_from_post(latest_post, config)

            local_result = db.get_posted_versions(account_id)
            local_versions = local_result.unwrap() if isinstance(local_result, Success) else {}

            if reddit_versions != local_versions:
                console.print(
                    f"[yellow]⚠ State mismatch![/yellow]\n"
                    f"  Local: {local_versions}\n"
                    f"  Reddit: {reddit_versions}\n"
                    f"  Using Reddit as source of truth"
                )
                for app_id, version in reddit_versions.items():
                    db.set_posted_version(account_id, app_id, version)
            else:
                console.print("[green]✓[/green] State verified")
    except Exception as e:
        console.print(f"[yellow]⚠ Verification failed: {e}[/yellow]")


@beartype
def _load_releases_data(console: Console, logger: ErrorLogger) -> dict[str, Any]:
    """Load releases.json file."""
    releases_file = Path(paths.DIST_DIR) / "releases.json"
    if not releases_file.exists():
        error = BitBotError("releases.json not found. Run 'bitbot gather' first.")
        logger.log_error(error, LogLevel.ERROR)
        console.print(f"[red]✗ Error:[/red] {error.message}")
        raise typer.Exit(code=1) from None

    with releases_file.open() as f:
        data = json.load(f)

    if not isinstance(data, dict):
        error = BitBotError("releases.json has invalid format")
        logger.log_error(error, LogLevel.ERROR)
        console.print(f"[red]✗ Error:[/red] {error.message}")
        raise typer.Exit(code=1) from None

    return data


@beartype
def should_create_new_post(
    reddit: praw.Reddit, existing_post_id: str | None, config: Config
) -> bool:
    """Check if enough time has passed to create a new post."""
    if not existing_post_id:
        return True

    try:
        submission = reddit.submission(id=existing_post_id)
        post_created_at = datetime.fromtimestamp(submission.created_utc, tz=UTC)
        days_elapsed = (datetime.now(UTC) - post_created_at).days
        days_before_new = config.reddit.rolling.get("days_before_new_post", 7)
    except Exception:
        return False
    else:
        return days_elapsed >= days_before_new


@beartype
def post_or_update(
    reddit: praw.Reddit, title: str, body: str, config: Config, existing_post_id: str | None
) -> tuple[praw.models.Submission, bool] | None:
    """Post new or update existing Reddit post."""
    if config.reddit.post_mode == "rolling_update":
        if should_create_new_post(reddit, existing_post_id, config):
            result = post_new_release(reddit, title, body, config)
            if isinstance(result, Failure):
                msg = f"Failed to create post: {result.failure()}"
                raise BitBotError(msg)
            return (result.unwrap(), False)

        if not existing_post_id:
            return None

        result = update_post(reddit, existing_post_id, body, config)
        if isinstance(result, Failure):
            msg = f"Failed to update post: {result.failure()}"
            raise BitBotError(msg)
        return (result.unwrap(), True)

    result = post_new_release(reddit, title, body, config)
    if isinstance(result, Failure):
        msg = f"Failed to create post: {result.failure()}"
        raise BitBotError(msg)
    return (result.unwrap(), False)


@beartype
def _build_changelog_data(
    all_releases_data: dict[str, Any], online_versions: dict[str, str]
) -> dict[str, dict[str, Any]]:
    """Build changelog data by comparing current releases vs posted versions."""
    changelog: dict[str, dict[str, Any]] = {"added": {}, "updated": {}, "removed": {}}

    current = {}
    for app_id, app_data in all_releases_data.items():
        latest = app_data.get("latest_release")
        if latest:
            current[app_id] = {
                "display_name": app_data.get("display_name", app_id),
                "version": latest.get("version", "unknown"),
                "url": latest.get("download_url", ""),
            }

    for app_id, info in current.items():
        if app_id not in online_versions:
            changelog["added"][app_id] = info
        elif online_versions[app_id] != info["version"]:
            changelog["updated"][app_id] = {"new": info, "old": online_versions[app_id]}

    for app_id, old_ver in online_versions.items():
        if app_id not in current:
            changelog["removed"][app_id] = {"display_name": app_id, "version": old_ver}

    return changelog


@beartype
def _has_new_releases(changelog: dict[str, dict[str, Any]], console: Console) -> bool:
    """Check if changelog has any changes."""
    has_changes = False
    for app_id, info in changelog["added"].items():
        console.print(f"[cyan]→[/cyan] New app: {app_id} v{info['version']}")
        has_changes = True
    for app_id, info in changelog["updated"].items():
        console.print(f"[cyan]→[/cyan] Update: {app_id} {info['old']} → {info['new']['version']}")
        has_changes = True
    for app_id in changelog["removed"]:
        console.print(f"[cyan]→[/cyan] Removed: {app_id}")
        has_changes = True
    return has_changes


@dataclass
class PostContext:
    """Context for posting to Reddit."""

    config: Config
    page_url: str


@beartype
def _build_and_post(
    reddit: praw.Reddit,
    context: PostContext,
    changelog: dict[str, dict[str, Any]],
    all_releases_data: dict[str, Any],
    existing_post_id: str | None,
) -> tuple[praw.models.Submission, bool] | None:
    """Build post content and submit to Reddit."""
    title = generate_dynamic_title(context.config, changelog["added"], changelog["updated"])
    body = generate_post_body(context.config, changelog, all_releases_data, context.page_url)
    return post_or_update(reddit, title, body, context.config, existing_post_id)


@beartype
@app.command()
def run(
    ctx: typer.Context,
    page_url: str = typer.Option(default=None, help="Landing page URL to post"),
    verify: bool = typer.Option(  # noqa: FBT001 - Typer CLI flag
        default=False, help="Verify state against actual Reddit post"
    ),
    force: bool = typer.Option(  # noqa: FBT001 - Typer CLI flag
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

                # Initialize database
                db.init()

                # Get account
                username = get_reddit_username()
                account_result = db.get_or_create_account(username, config.reddit.subreddit)
                if isinstance(account_result, Failure):
                    error = BitBotError(f"DB error: {account_result.failure()}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {error.message}")
                    raise typer.Exit(code=1) from None
                account_id = account_result.unwrap()

                # Load releases data
                all_releases_data = _load_releases_data(console, logger)

                # Get posted versions
                versions_result = db.get_posted_versions(account_id)
                if isinstance(versions_result, Success):
                    online_versions = versions_result.unwrap()
                else:
                    online_versions = {}

                # Build changelog
                changelog = _build_changelog_data(all_releases_data, online_versions)

                if not force and not _has_new_releases(changelog, console):
                    console.print("[dim]No new releases. Use --force to post anyway.[/dim]")
                    return

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

                # Get current active post
                meta_result = db.get_account(account_id)
                active_post_id = None
                if isinstance(meta_result, Success):
                    active_post_id = meta_result.unwrap().get("active_post_id")

                # Optional verification
                if verify and active_post_id:
                    _verify_account_state(reddit, config, account_id, console)

                # Build and post
                context = PostContext(config=config, page_url=page_url)
                result = _build_and_post(
                    reddit, context, changelog, all_releases_data, active_post_id
                )

                if result is None:
                    console.print("[yellow][i] No existing post to update[/yellow]")
                    return

                submission, was_updated = result

                if was_updated:
                    console.print(f"[green]✓[/green] Updated post: {submission.url}")
                else:
                    console.print(f"[green]✓[/green] Posted: {submission.url}")

                # Update database
                db.update_account(account_id, active_post_id=submission.id)
                db.add_post_id(account_id, submission.id)

                for app_id, app_data in all_releases_data.items():
                    latest = app_data.get("latest_release")
                    if latest:
                        db.set_posted_version(account_id, app_id, latest.get("version", "unknown"))

        except Exception as e:
            error = BitBotError(f"Unexpected error: {e}")
            logger.log_error(error, LogLevel.CRITICAL)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
