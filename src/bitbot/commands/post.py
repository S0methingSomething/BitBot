"""Post command for BitBot CLI.

Architecture:
- releases.json = what versions exist (from gather)
- Local DB = what we've announced (our record)
- Reddit = output destination

We do NOT parse versions from Reddit. Local DB is our announcement record.
If state is wrong, use --reset to clear and re-announce.
"""

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, cast

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
from bitbot.reddit.posting.body_builder import generate_post_body
from bitbot.reddit.posting.poster import post_new_release, update_post
from bitbot.reddit.posting.title_generator import generate_dynamic_title
from bitbot.reddit.posting.validator import validate_post, validate_posted
from bitbot.reddit.state import (
    PostStatus,
    check_post_exists,
    compute_content_hash,
    verify_state,
)
from bitbot.types import Changelog, ReleaseInfo, ReleasesData, UpdatedReleaseInfo

if TYPE_CHECKING:
    from bitbot.core.container import Container

app = typer.Typer()


@beartype
def _load_releases_data(console: Console, logger: ErrorLogger) -> ReleasesData:
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

    return data  # type: ignore[return-value]


@beartype
def _should_create_new_post(
    reddit: praw.Reddit, existing_post_id: str | None, config: Config
) -> bool:
    """Check if enough time has passed to create a new post."""
    if not existing_post_id:
        return True

    try:
        submission = reddit.submission(id=existing_post_id)
        post_created_at = datetime.fromtimestamp(submission.created_utc, tz=UTC)
        time_elapsed = datetime.now(UTC) - post_created_at
        days_before_new = config.reddit.rolling.get("days_before_new_post", 7)
        return time_elapsed.total_seconds() >= days_before_new * 86400
    except Exception:
        # If we can't access the post, create a new one
        return True


@beartype
def _build_changelog(
    all_releases_data: ReleasesData, announced_versions: dict[str, str]
) -> Changelog:
    """Build changelog by comparing releases.json vs what we've announced."""
    changelog: Changelog = {"added": {}, "updated": {}, "removed": {}}

    # Current versions from releases.json
    current: dict[str, ReleaseInfo] = {}
    for app_id, app_data in all_releases_data.items():
        latest = app_data.get("latest_release")
        if latest:
            current[app_id] = cast(
                "ReleaseInfo",
                {
                    "display_name": app_data.get("display_name", app_id),
                    "version": latest.get("version", "unknown"),
                    "url": latest.get("download_url", ""),
                },
            )

    # Compare with announced
    for app_id, info in current.items():
        if app_id not in announced_versions:
            changelog["added"][app_id] = info
        elif announced_versions[app_id] != info["version"]:
            changelog["updated"][app_id] = cast(
                "UpdatedReleaseInfo", {"new": info, "old": announced_versions[app_id]}
            )

    for app_id, old_ver in announced_versions.items():
        if app_id not in current:
            changelog["removed"][app_id] = {"display_name": app_id, "version": old_ver}

    return changelog


@beartype
def _print_changelog(changelog: Changelog, console: Console) -> bool:
    """Print changelog and return True if there are changes."""
    has_changes = False
    for app_id, info in changelog["added"].items():
        console.print(f"[cyan]+ Added:[/cyan] {info['display_name']} v{info['version']}")
        has_changes = True
    for app_id, upd in changelog["updated"].items():
        console.print(
            f"[cyan]↑ Updated:[/cyan] {upd['new']['display_name']} "
            f"{upd['old']} → {upd['new']['version']}"
        )
        has_changes = True
    for app_id, info in changelog["removed"].items():
        console.print(f"[cyan]- Removed:[/cyan] {info['display_name']} v{info['version']}")
        has_changes = True
    return has_changes


@dataclass
class PostContext:
    """Context for posting."""

    config: Config
    page_url: str
    console: Console
    account_id: int


@beartype
def _do_post(
    reddit: praw.Reddit,
    ctx: PostContext,
    title: str,
    body: str,
    content_hash: str,
    active_post_id: str | None,
    force_update: bool = False,
) -> tuple[praw.models.Submission, bool, str] | None:
    """Execute the post/update operation. Returns (submission, was_update, content_hash)."""
    # Decide: new post or update?
    if ctx.config.reddit.post_mode == "rolling_update" and active_post_id:
        if force_update or not _should_create_new_post(reddit, active_post_id, ctx.config):
            # Update existing
            result = update_post(reddit, active_post_id, body, ctx.config)
            if isinstance(result, Failure):
                raise BitBotError(f"Failed to update post: {result.failure()}")
            return (result.unwrap(), True, content_hash)

    # Create new post
    result = post_new_release(reddit, title, body, ctx.config)
    if isinstance(result, Failure):
        raise BitBotError(f"Failed to create post: {result.failure()}")
    return (result.unwrap(), False, content_hash)


@beartype
def _verify_and_save(
    reddit: praw.Reddit,
    submission: praw.models.Submission,
    ctx: PostContext,
    releases_data: ReleasesData,
    content_hash: str,
) -> None:
    """Verify the post and save state."""
    # Validate after posting
    post_validation = validate_posted(submission)
    for issue in post_validation.issues:
        color = "red" if issue.severity == "error" else "yellow"
        ctx.console.print(f"[{color}]POST {issue.severity.upper()}:[/{color}] {issue.message}")

    # Verify post is accessible
    status = check_post_exists(reddit, submission.id)
    if not status.accessible:
        ctx.console.print(f"[yellow]⚠ Warning: Post may not be visible[/yellow]")
        if status.removal_reason:
            ctx.console.print(f"[yellow]  Reason: {status.removal_reason}[/yellow]")

    # Save state
    db.update_account(ctx.account_id, active_post_id=submission.id, content_hash=content_hash)
    db.add_post_id(ctx.account_id, submission.id)

    # Update announced versions
    for app_id, app_data in releases_data.items():
        latest = app_data.get("latest_release")
        if latest:
            db.set_posted_version(ctx.account_id, app_id, latest.get("version", "unknown"))


@beartype
@app.command()
def run(
    ctx: typer.Context,
    page_url: str = typer.Option(default=None, help="Landing page URL"),
    force: bool = typer.Option(  # noqa: FBT001
        default=False, help="Force post even if no version changes"
    ),
    refresh: bool = typer.Option(  # noqa: FBT001
        default=False, help="Refresh post content (update even if versions unchanged)"
    ),
    reset: bool = typer.Option(  # noqa: FBT001
        default=False, help="Reset state and announce all versions as new"
    ),
    verify: bool = typer.Option(  # noqa: FBT001
        default=False, help="Verify Reddit state before posting"
    ),
    preview: bool = typer.Option(  # noqa: FBT001
        default=False, help="Preview post content without posting (saves to dist/post_preview.md)"
    ),
) -> None:
    """Post releases to Reddit.

    Normal flow: Only posts if there are new/updated versions.
    --force: Post even if no version changes (uses existing changelog).
    --refresh: Update post content even if versions unchanged.
    --reset: Clear local state and announce everything as new.
    --verify: Check Reddit state and report issues before posting.
    """
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
                task = progress.add_task(description="Initializing...", total=None)

                # Initialize
                db.init()
                username = get_reddit_username()
                account_result = db.get_or_create_account(username, config.reddit.subreddit)
                if isinstance(account_result, Failure):
                    raise BitBotError(f"DB error: {account_result.failure()}")
                account_id = account_result.unwrap()

                # Handle reset
                if reset:
                    progress.update(task, description="Resetting state...")
                    db.reset_account_state(account_id)
                    console.print("[green]✓[/green] State reset - all versions will be announced as new")

                # Load data
                progress.update(task, description="Loading release data...")
                releases_data = _load_releases_data(console, logger)

                if not page_url:
                    page_url = config.github.pages_url

                # Get announced versions from local DB
                versions_result = db.get_posted_versions(account_id)
                announced = versions_result.unwrap() if isinstance(versions_result, Success) else {}

                # Build changelog
                changelog = _build_changelog(releases_data, announced)
                has_changes = _print_changelog(changelog, console)

                # Init Reddit
                progress.update(task, description="Connecting to Reddit...")
                reddit_result = init_reddit(config)
                if isinstance(reddit_result, Failure):
                    raise BitBotError(f"Reddit error: {reddit_result.failure()}")
                reddit = reddit_result.unwrap()

                # Get active post ID
                meta_result = db.get_account(account_id)
                active_post_id = None
                stored_hash = None
                if isinstance(meta_result, Success):
                    meta = meta_result.unwrap()
                    active_post_id = meta.get("active_post_id")
                    stored_hash = meta.get("content_hash")

                # Verify state if requested
                if verify and active_post_id:
                    progress.update(task, description="Verifying Reddit state...")
                    state_check = verify_state(reddit, account_id)

                    if state_check.issues:
                        for issue in state_check.issues:
                            console.print(f"[yellow]⚠ {issue}[/yellow]")

                    if not state_check.post_ok:
                        console.print("[yellow]Post is invalid - will create new post[/yellow]")
                        active_post_id = None

                # Check if we need to refresh content
                needs_refresh = False
                if refresh and active_post_id:
                    progress.update(task, description="Checking content...")
                    post_ctx = PostContext(config, page_url, console, account_id)
                    expected_body = generate_post_body(config, changelog, releases_data, page_url)
                    expected_hash = compute_content_hash(expected_body)

                    status = check_post_exists(reddit, active_post_id)
                    if status.current_hash and status.current_hash != expected_hash:
                        console.print("[cyan]→[/cyan] Content differs - will refresh")
                        needs_refresh = True

                # Decide if we should post
                should_post = has_changes or force or needs_refresh

                if not should_post and not preview:
                    console.print(
                        "[dim]No changes to post. Use --force to post anyway, "
                        "--refresh to update content, or --preview to see what would be posted.[/dim]"
                    )
                    return

                # Generate the post content
                progress.update(task, description="Generating post content...")
                title = generate_dynamic_title(config, changelog["added"], changelog["updated"])
                body = generate_post_body(config, changelog, releases_data, page_url)
                content_hash = compute_content_hash(body)

                # Validate content
                validation = validate_post(title, body, config)
                if validation.issues:
                    console.print("\n[bold]Validation Results:[/bold]")
                    for issue in validation.issues:
                        color = "red" if issue.severity == "error" else "yellow"
                        console.print(f"  [{color}]{issue.severity.upper()}:[/{color}] {issue.message}")

                    if validation.has_errors:
                        console.print("\n[red]✗ Post has validation errors - cannot post[/red]")
                        raise typer.Exit(code=1)

                # Save preview to file
                preview_file = Path(paths.DIST_DIR) / "post_preview.md"
                preview_file.parent.mkdir(parents=True, exist_ok=True)
                preview_content = f"""# Post Preview

**Title:** {title}

**Content Hash:** {content_hash}

**Would {'UPDATE' if active_post_id and not _should_create_new_post(reddit, active_post_id, config) else 'CREATE NEW'} post**

---

{body}
"""
                preview_file.write_text(preview_content)
                console.print(f"\n[green]✓[/green] Preview saved to: {preview_file}")

                # If preview mode, show content and exit
                if preview:
                    console.print("\n[bold]═══ POST PREVIEW ═══[/bold]")
                    console.print(f"\n[bold]Title:[/bold] {title}")
                    console.print(f"[bold]Length:[/bold] {len(body)} chars")
                    console.print(f"[bold]Hash:[/bold] {content_hash}")
                    console.print("\n[bold]Body:[/bold]")
                    console.print("─" * 60)
                    # Show first 2000 chars of body
                    if len(body) > 2000:
                        console.print(body[:2000])
                        console.print(f"\n... [dim]({len(body) - 2000} more chars, see {preview_file})[/dim]")
                    else:
                        console.print(body)
                    console.print("─" * 60)
                    console.print("\n[dim]This is a preview. Run without --preview to actually post.[/dim]")
                    return

                # Do the actual post
                progress.update(task, description="Posting to Reddit...")
                post_ctx = PostContext(config, page_url, console, account_id)

                result = _do_post(
                    reddit,
                    post_ctx,
                    title,
                    body,
                    content_hash,
                    active_post_id,
                    force_update=needs_refresh,
                )

                if result is None:
                    console.print("[yellow]No post created[/yellow]")
                    return

                submission, was_update, content_hash = result

                # Verify and save
                progress.update(task, description="Verifying and saving...")
                _verify_and_save(reddit, submission, post_ctx, releases_data, content_hash)

                # Report success
                if was_update:
                    if needs_refresh:
                        console.print(f"[green]✓[/green] Refreshed: {submission.url}")
                    else:
                        console.print(f"[green]✓[/green] Updated: {submission.url}")
                else:
                    console.print(f"[green]✓[/green] Posted: {submission.url}")

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
