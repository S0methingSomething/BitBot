"""This module checks for comments on the active Reddit post."""

import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .interfaces.config_protocol import ConfigManagerProtocol
from .interfaces.reddit_protocol import RedditManagerProtocol
from .interfaces.state_protocol import StateManagerProtocol
from .logging import get_logger

logger = get_logger(__name__)


async def check_comments(
    config_manager: ConfigManagerProtocol,
    state_manager: StateManagerProtocol,
    reddit_manager: RedditManagerProtocol,
) -> bool:
    """Check for comments on the active Reddit post.

    This function analyzes feedback, and updates the post status with an
    adaptive timer.

    Returns:
        True if a check was performed, False otherwise.
    """
    config = await config_manager.load_config()
    state = await state_manager.load_state()
    state_was_meaningfully_updated = False

    if not state.activePostId:
        logger.info("No active post ID in state file. Exiting pulse.")
        return False

    if not state.lastCheckTimestamp:
        logger.info("No lastCheckTimestamp in state file. Exiting pulse.")
        return False

    now = datetime.now(timezone.utc)
    last_check = datetime.fromisoformat(state.lastCheckTimestamp.replace("Z", "+00:00"))

    if now < (last_check + timedelta(seconds=state.currentIntervalSeconds)):
        logger.info(
            "Not time yet. Next check in %s.",
            int(
                (
                    (last_check + timedelta(seconds=state.currentIntervalSeconds)) - now
                ).total_seconds()
            ),
        )
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("state_changed=false")
        return False

    logger.info("Time for a real check on post: %s", state.activePostId)
    try:
        submission = await reddit_manager.get_post_by_id(state.activePostId)
        if not submission:
            logger.warning("Could not find submission with ID: %s", state.activePostId)
            return False

        comments = await reddit_manager.get_comments(submission)

        working_kw = re.compile("|".join(config.feedback.workingKeywords), re.I)
        not_working_kw = re.compile("|".join(config.feedback.notWorkingKeywords), re.I)
        positive_score = sum(1 for c in comments if working_kw.search(c.body))
        negative_score = sum(1 for c in comments if not_working_kw.search(c.body))
        net_score = positive_score - negative_score
        logger.info(
            "Comment analysis: Positive=%s, Negative=%s, Net Score=%s",
            positive_score,
            negative_score,
            net_score,
        )

        threshold = config.feedback.minFeedbackCount
        if net_score <= -threshold:
            new_status_text = config.feedback.labels.broken
        elif net_score >= threshold:
            new_status_text = config.feedback.labels.working
        else:
            new_status_text = config.feedback.labels.unknown

        new_status_line = config.feedback.statusLineFormat.replace(
            "{{status}}", new_status_text
        )

        status_regex = re.compile(
            config.feedback.statusLineRegex, re.MULTILINE | re.DOTALL
        )
        if not status_regex.search(submission.body):
            logger.warning(
                "Could not find status line in post. "
                "It may have been edited or is an outdated post."
            )
        elif new_status_line != submission.body:
            updated_body = status_regex.sub(new_status_line, submission.body)
            await reddit_manager.update_post_body(submission.id, updated_body)
            logger.info("Status updated to: %s", new_status_text)
        else:
            logger.info("Status is already correct.")

        if len(comments) > state.lastCommentCount:
            state.currentIntervalSeconds = config.timing.firstCheck
            state_was_meaningfully_updated = True
        else:
            if state.currentIntervalSeconds < config.timing.maxWait:
                state.currentIntervalSeconds = min(
                    config.timing.maxWait,
                    state.currentIntervalSeconds + config.timing.increaseBy,
                )
                state_was_meaningfully_updated = True

        if state.lastCommentCount != len(comments):
            state.lastCommentCount = len(comments)
            state_was_meaningfully_updated = True

    except Exception as e:
        logger.error("An exception occurred during check: %s", e, exc_info=True)
    finally:
        state.lastCheckTimestamp = now.isoformat().replace("+00:00", "Z")
        if state_was_meaningfully_updated:
            logger.info("Meaningful state change detected. Saving state file.")
            await state_manager.save_state(state)
        else:
            logger.info("No meaningful state change detected. Skipping file write.")

        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write(f"state_changed={str(state_was_meaningfully_updated).lower()}")
        logger.info(
            "Pulse check complete. Next interval: %ss",
            state.currentIntervalSeconds,
        )
    return True
