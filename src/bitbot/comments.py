"""This module checks for comments on the active Reddit post."""

import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, cast

import praw  # type: ignore

from . import utils
from .logging import get_logger

logger = get_logger(__name__)


def check_comments() -> None:
    """Check for comments on the active Reddit post.

    This function analyzes feedback, and updates the post status with an
    adaptive timer.
    """
    config = utils.load_config()
    state = utils.load_state()
    state_was_meaningfully_updated = False

    if not state.get("activePostId"):
        logger.info("No active post ID in state file. Exiting pulse.")
        sys.exit(0)

    if not state.get("lastCheckTimestamp"):
        logger.info("No lastCheckTimestamp in state file. Exiting pulse.")
        sys.exit(0)

    now = datetime.now(timezone.utc)
    last_check = datetime.fromisoformat(
        state["lastCheckTimestamp"].replace("Z", "+00:00")
    )

    if now < (last_check + timedelta(seconds=state["currentIntervalSeconds"])):
        logger.info(
            "Not time yet. Next check in %s.",
            int(
                (
                    (last_check + timedelta(seconds=state["currentIntervalSeconds"]))
                    - now
                ).total_seconds()
            ),
        )
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("state_changed=false")
        sys.exit(0)

    logger.info("Time for a real check on post: %s", state["activePostId"])
    try:
        reddit = praw.Reddit(
            client_id=os.environ["REDDIT_CLIENT_ID"],
            client_secret=os.environ["REDDIT_CLIENT_SECRET"],
            user_agent=os.environ["REDDIT_USER_AGENT"],
            username=os.environ["REDDIT_USERNAME"],
            password=os.environ["REDDIT_PASSWORD"],
        )
        submission = reddit.submission(id=state["activePostId"])
        submission.comments.replace_more(limit=0)
        comments = submission.comments.list()

        working_kw = re.compile("|".join(config["feedback"]["workingKeywords"]), re.I)
        not_working_kw = re.compile(
            "|".join(config["feedback"]["notWorkingKeywords"]), re.I
        )
        positive_score = sum(1 for c in comments if working_kw.search(c.body))
        negative_score = sum(1 for c in comments if not_working_kw.search(c.body))
        net_score = positive_score - negative_score
        logger.info(
            "Comment analysis: Positive=%s, Negative=%s, Net Score=%s",
            positive_score,
            negative_score,
            net_score,
        )

        threshold = config["feedback"]["minFeedbackCount"]
        if net_score <= -threshold:
            new_status_text = config["feedback"]["labels"]["broken"]
        elif net_score >= threshold:
            new_status_text = config["feedback"]["labels"]["working"]
        else:
            new_status_text = config["feedback"]["labels"]["unknown"]

        new_status_line = config["feedback"]["statusLineFormat"].replace(
            "{{status}}", new_status_text
        )

        status_regex = re.compile(
            config["feedback"]["statusLineRegex"], re.MULTILINE | re.DOTALL
        )
        logger.info("Searching for status line with regex: %s", status_regex.pattern)
        logger.info("New status line: %s", new_status_line)
        logger.info("New status line: %s", new_status_line)
        logger.info("Post selftext: %s", submission.selftext)
        logger.info("New status line: %s", new_status_line)
        logger.info("Post selftext: %s", submission.selftext)
        if not submission or not status_regex.search(submission.selftext):
            logger.warning(
                "Could not find status line in post. "
                "It may have been edited or is an outdated post."
            )
        elif new_status_line != submission.selftext:
            updated_body = status_regex.sub(new_status_line, submission.selftext)
            submission.edit(body=updated_body)
            logger.info("Status updated to: %s", new_status_text)
        else:
            logger.info("Status is already correct.")

        if len(comments) > state["lastCommentCount"]:
            state["currentIntervalSeconds"] = config["timing"]["firstCheck"]
            state_was_meaningfully_updated = True
        else:
            if state["currentIntervalSeconds"] < config["timing"]["maxWait"]:
                state["currentIntervalSeconds"] = min(
                    config["timing"]["maxWait"],
                    state["currentIntervalSeconds"] + config["timing"]["increaseBy"],
                )
                state_was_meaningfully_updated = True

        if state["lastCommentCount"] != len(comments):
            state["lastCommentCount"] = len(comments)
            state_was_meaningfully_updated = True

    except praw.exceptions.PRAWException as e:
        logger.error("An exception occurred during check: %s", e, exc_info=True)
    finally:
        state["lastCheckTimestamp"] = now.isoformat().replace("+00:00", "Z")
        if state_was_meaningfully_updated:
            logger.info("Meaningful state change detected. Saving state file.")
            save_state(state)
        else:
            logger.info("No meaningful state change detected. Skipping file write.")

        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write(f"state_changed={str(state_was_meaningfully_updated).lower()}")
        logger.info(
            "Pulse check complete. Next interval: %ss",
            state["currentIntervalSeconds"],
        )
