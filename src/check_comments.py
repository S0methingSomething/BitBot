import os
import re
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, cast

from config_loader import load_config
from dry_run import is_dry_run
from helpers import init_reddit, load_bot_state, save_bot_state
from logging_config import get_logger

logging = get_logger(__name__)


def _analyze_comments(comments: list[Any], config: Any) -> str:
    """Analyzes comments and returns the new status."""
    working_kw = re.compile("|".join(config.feedback.working_keywords), re.I)
    not_working_kw = re.compile("|".join(config.feedback.not_working_keywords), re.I)
    positive = sum(1 for c in comments if working_kw.search(c.body))
    negative = sum(1 for c in comments if not_working_kw.search(c.body))
    net_score = positive - negative
    logging.info(
        f"Comment analysis: Positive={positive}, Negative={negative}, Net={net_score}"
    )

    threshold = config.feedback.min_feedback_count
    if net_score <= -threshold:
        return cast(str, config.feedback.labels.broken)
    if net_score >= threshold:
        return cast(str, config.feedback.labels.working)
    return cast(str, config.feedback.labels.unknown)


def _update_post_status(submission: Any, new_status: str, config: Any) -> None:
    """Updates the post with the new status if it has changed."""
    new_line = config.feedback.status_line_format.replace("{{status}}", new_status)
    regex = re.compile(config.feedback.status_line_regex, re.MULTILINE)
    if not regex.search(submission.selftext):
        logging.warning("Could not find status line in post.")
    elif new_line not in submission.selftext:
        submission.edit(body=regex.sub(new_line, submission.selftext))
        logging.info(f"Status updated to: {new_status}")
    else:
        logging.info("Status is already correct.")


def _update_timing_interval(
    state: dict[str, Any], num_comments: int, config: Any
) -> None:
    """Updates the timing interval based on comment activity."""
    last_count = state.get("lastCommentCount", 0)
    if num_comments > last_count:
        state["currentIntervalSeconds"] = config.timing.first_check
    elif (
        state.get("currentIntervalSeconds", config.timing.first_check)
        < config.timing.max_wait
    ):
        state["currentIntervalSeconds"] = (
            state.get("currentIntervalSeconds", config.timing.first_check)
            + config.timing.increase_by
        )
    if last_count != num_comments:
        state["lastCommentCount"] = num_comments


def check_post_status(config: Any, state: dict[str, Any]) -> bool:
    """Analyzes feedback and updates the post status."""
    active_post_id = state.get("activePostId")
    if not active_post_id:
        logging.info("No active post ID in state file.")
        return False

    if is_dry_run():
        logging.info("DRY_RUN: Would check post status")
        logging.info(f"  Active Post ID: {active_post_id}")
        # Simulate a status update
        new_status = "Working (Dry Run Simulation)"
        logging.info(f"  Simulated new status: {new_status}")
        _update_timing_interval(state, 5, config)  # Simulate 5 comments
        return True

    try:
        reddit = init_reddit(config)
        submission = reddit.submission(id=active_post_id)
        submission.comments.replace_more(limit=0)
        comments = submission.comments.list()

        new_status = _analyze_comments(comments, config)
        _update_post_status(submission, new_status, config)
        _update_timing_interval(state, len(comments), config)
        return True

    except Exception as e:
        logging.error(f"An exception occurred during check: {e}")
        return False


def main() -> None:
    config = load_config()
    state = load_bot_state()

    now = datetime.now(UTC)
    last_check = datetime.fromisoformat(
        state.get("lastCheckTimestamp", "2000-01-01T00:00:00Z").replace("Z", "+00:00")
    )
    interval = state.get("currentIntervalSeconds", config.timing.first_check)

    if now < (last_check + timedelta(seconds=interval)):
        logging.info(
            f"Not time yet. Next check in {int(((last_check + timedelta(seconds=interval)) - now).total_seconds())}s."
        )
        if github_output := os.environ.get("GITHUB_OUTPUT"):
            with Path(github_output).open("a") as f:
                f.write(
                    "state_changed=false\
"
                )
        sys.exit(0)

    updated = check_post_status(config, state)
    state["lastCheckTimestamp"] = now.isoformat().replace("+00:00", "Z")
    save_bot_state(state)

    if github_output := os.environ.get("GITHUB_OUTPUT"):
        with Path(github_output).open("a") as f:
            f.write(
                f"state_changed={str(updated).lower()}\
"
            )
    logging.info(
        f"Pulse check complete. Next interval: {state.get('currentIntervalSeconds', config.timing.first_check)}s"
    )


if __name__ == "__main__":
    main()
