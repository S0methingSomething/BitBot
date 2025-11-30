"""Check command for BitBot CLI."""

import re
from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import TYPE_CHECKING

import typer
from beartype import beartype
from praw.models import Submission
from returns.result import Failure, Result, Success
from rich.progress import Progress, SpinnerColumn, TextColumn

from bitbot.config_models import Config
from bitbot.core import db
from bitbot.core.credentials import get_reddit_username
from bitbot.core.error_context import error_context
from bitbot.core.error_logger import LogLevel
from bitbot.core.errors import BitBotError, RedditAPIError
from bitbot.reddit.client import init_reddit

if TYPE_CHECKING:
    from rich.console import Console

    from bitbot.core.container import Container

app = typer.Typer()


class CheckResult(Enum):
    """Result of comment check operation."""

    STATE_CHANGED = "changed"
    STATE_UNCHANGED = "unchanged"


@beartype
def _analyze_sentiment(comments: list, config: Config) -> str:
    """Analyze comment sentiment and return status."""
    working_kw = re.compile("|".join(config.feedback["workingKeywords"]), re.IGNORECASE)
    not_working_kw = re.compile("|".join(config.feedback["notWorkingKeywords"]), re.IGNORECASE)
    positive = sum(1 for c in comments if working_kw.search(c.body))
    negative = sum(1 for c in comments if not_working_kw.search(c.body))
    net_score = positive - negative

    threshold = config.feedback["minFeedbackCount"]
    if net_score <= -threshold:
        return config.feedback["labels"]["broken"]
    if net_score >= threshold:
        return config.feedback["labels"]["working"]
    return config.feedback["labels"]["unknown"]


@beartype
def _update_post_status(submission: Submission, status: str, config: Config) -> None:
    """Update post status line if needed."""
    status_line = config.feedback["statusLineFormat"].replace("{{status}}", status)
    status_regex = re.compile(config.feedback["statusLineRegex"], re.MULTILINE)

    if status_regex.search(submission.selftext) and status_line not in submission.selftext:
        updated_body = status_regex.sub(status_line, submission.selftext)
        submission.edit(body=updated_body)


@beartype
def check_comments(config: Config, account_id: int) -> Result[CheckResult, BitBotError]:
    """Check comments and update post status."""
    # Get account metadata
    meta_result = db.get_account(account_id)
    if isinstance(meta_result, Failure):
        return Failure(meta_result.failure())

    meta = meta_result.unwrap()
    active_post_id = meta.get("active_post_id")
    last_check_str = meta.get("last_check_timestamp") or "2000-01-01T00:00:00Z"
    current_interval = meta.get("check_interval_seconds") or config.timing["firstCheck"]

    # Skip if no active post
    if not active_post_id:
        return Success(CheckResult.STATE_UNCHANGED)

    # Skip if not time yet
    now = datetime.now(UTC)
    last_check = datetime.fromisoformat(last_check_str)
    if now < (last_check + timedelta(seconds=current_interval)):
        return Success(CheckResult.STATE_UNCHANGED)

    # Initialize reddit client
    reddit_result = init_reddit(config)
    if isinstance(reddit_result, Failure):
        return Failure(reddit_result.failure())

    reddit = reddit_result.unwrap()

    try:
        submission = reddit.submission(id=active_post_id)
        submission.comments.replace_more(limit=0)
        comments = submission.comments.list()

        status = _analyze_sentiment(comments, config)
        _update_post_status(submission, status, config)

        # Update interval based on activity
        last_count = meta.get("last_comment_count") or 0
        comment_count = len(comments)
        new_interval = current_interval

        if comment_count > last_count:
            new_interval = config.timing["firstCheck"]
        elif current_interval < config.timing["maxWait"]:
            increase = config.timing["increaseBy"]
            new_interval = min(config.timing["maxWait"], current_interval + increase)

        # Update timestamp and comment count
        new_timestamp = now.isoformat().replace("+00:00", "Z")
        db.update_account(
            account_id,
            last_check_timestamp=new_timestamp,
            check_interval_seconds=new_interval,
            last_comment_count=comment_count,
        )

        changed = new_interval != current_interval
        return Success(CheckResult.STATE_CHANGED if changed else CheckResult.STATE_UNCHANGED)

    except Exception as e:
        return Failure(RedditAPIError(f"Failed to check comments: {e}"))


@beartype
@app.command()
def run(ctx: typer.Context) -> None:
    """Check Reddit comments for feedback."""
    container: Container = ctx.obj["container"]
    console: Console = container.console()
    logger = container.logger()
    config: Config = container.config()

    with error_context(operation="check_comments"):
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                progress.add_task(description="Checking comments...", total=None)

                # Initialize database
                db.init()

                # Get account
                username = get_reddit_username()
                account_result = db.get_or_create_account(username, config.reddit.subreddit)
                if isinstance(account_result, Failure):
                    error = BitBotError(f"DB error: {account_result.failure()}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {error.message}")
                    raise typer.Exit(code=1)
                account_id = account_result.unwrap()

                result = check_comments(config, account_id)

                if isinstance(result, Failure):
                    error = result.failure()
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {error.message}")
                    raise typer.Exit(code=1)

                check_result = result.unwrap()
                if check_result == CheckResult.STATE_CHANGED:
                    console.print("[green]✓[/green] Comments checked, state updated")
                else:
                    console.print("[green]✓[/green] No updates needed")

        except Exception as e:
            error = BitBotError(f"Unexpected error: {e}")
            logger.log_error(error, LogLevel.CRITICAL)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
