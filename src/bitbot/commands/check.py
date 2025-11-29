"""Check command for BitBot CLI."""

import re
from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import TYPE_CHECKING

import deal
import typer
from beartype import beartype
from praw.models import Submission
from rich.progress import Progress, SpinnerColumn, TextColumn

from bitbot.config_models import Config
from bitbot.core.error_context import error_context
from bitbot.core.error_logger import LogLevel
from bitbot.core.errors import BitBotError, RedditAPIError
from bitbot.core.result import Err, Ok, Result
from bitbot.core.state import load_bot_state, save_bot_state
from bitbot.models import BotState
from bitbot.reddit.client import init_reddit

if TYPE_CHECKING:
    from rich.console import Console

    from bitbot.core.container import Container

app = typer.Typer()


class CheckResult(Enum):
    """Result of comment check operation."""

    STATE_CHANGED = "changed"
    STATE_UNCHANGED = "unchanged"


@deal.post(lambda result: len(result) > 0)
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


@deal.pre(
    lambda _submission, status, _config: len(status) > 0,
    message="Status cannot be empty",
)
@beartype
def _update_post_status(submission: Submission, status: str, config: Config) -> None:
    """Update post status line if needed."""
    status_line = config.feedback["statusLineFormat"].replace("{{status}}", status)
    status_regex = re.compile(config.feedback["statusLineRegex"], re.MULTILINE)

    if status_regex.search(submission.selftext) and status_line not in submission.selftext:
        updated_body = status_regex.sub(status_line, submission.selftext)
        submission.edit(body=updated_body)


@deal.pre(
    lambda _state, comment_count, _config: comment_count >= 0,
    message="Comment count must be non-negative",
)
@beartype
def _update_check_interval(state: BotState, comment_count: int, config: Config) -> CheckResult:
    """Update check interval based on activity."""
    last_count = int(state.online.get("lastCommentCount", "0"))
    current_interval = state.current_interval_seconds or config.timing["firstCheck"]
    changed = False

    if comment_count > last_count:
        state.current_interval_seconds = config.timing["firstCheck"]
        changed = True
    elif current_interval < config.timing["maxWait"]:
        state.current_interval_seconds = min(
            config.timing["maxWait"], current_interval + config.timing["increaseBy"]
        )
        changed = True

    if last_count != comment_count:
        state.online["lastCommentCount"] = str(comment_count)
        changed = True

    return CheckResult.STATE_CHANGED if changed else CheckResult.STATE_UNCHANGED


@beartype
def check_comments(config: Config) -> Result[CheckResult, BitBotError]:
    """Check comments and update post status."""
    state_result = load_bot_state()
    if state_result.is_err():
        return Err(state_result.unwrap_err())

    state = state_result.unwrap()
    now = datetime.now(UTC)
    last_check_str = state.last_check_timestamp or "2000-01-01T00:00:00Z"
    last_check = datetime.fromisoformat(last_check_str)
    current_interval = state.current_interval_seconds or config.timing["firstCheck"]

    # Skip check if no active post or not time yet
    if not state.active_post_id or now < (last_check + timedelta(seconds=current_interval)):
        return Ok(CheckResult.STATE_UNCHANGED)

    # Initialize reddit client
    reddit_result = init_reddit(config)
    if reddit_result.is_err():
        return Err(reddit_result.unwrap_err())

    reddit = reddit_result.unwrap()

    try:
        submission = reddit.submission(id=state.active_post_id)
        submission.comments.replace_more(limit=0)
        comments = submission.comments.list()

        status = _analyze_sentiment(comments, config)
        _update_post_status(submission, status, config)
        state_changed = _update_check_interval(state, len(comments), config)

    except Exception as e:
        return Err(RedditAPIError(f"Failed to check comments: {e}"))

    # Update timestamp and save state
    state.last_check_timestamp = now.isoformat().replace("+00:00", "Z")
    if state_changed == CheckResult.STATE_CHANGED:
        save_result = save_bot_state(state)
        if save_result.is_err():
            return Err(save_result.unwrap_err())

    return Ok(state_changed)


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
                result = check_comments(config)

                if result.is_err():
                    error = result.unwrap_err()
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
