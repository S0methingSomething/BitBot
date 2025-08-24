"""Reddit posting utilities for BitBot."""

import re
import sys
from typing import Any
from unittest.mock import MagicMock

import praw

from dry_run import (
    DryRunLevel,
    get_dry_run_level,
    is_dry_run,
)
from logging_config import get_logger

logging = get_logger(__name__)

# --- Constants ---
MAX_OUTBOUND_LINKS_ERROR = 8


def count_outbound_links(text: str) -> int:
    """Count the number of unique outbound links in a text.

    Args:
        text: Text to analyze

    Returns:
        Number of unique outbound links
    """
    url_pattern = re.compile(r"https?://[^\s/$.?#].[^\s]*|www\.[^\s/$.?#].[^\s]*")
    return len(set(url_pattern.findall(text)))


def post_new_release(
    reddit: praw.Reddit, title: str, body: str, config: Any
) -> praw.models.Submission:
    """Post a new release to Reddit.

    Args:
        reddit: Reddit instance
        title: Post title
        body: Post body
        config: Configuration object

    Returns:
        Reddit submission object
    """
    link_count = count_outbound_links(body)
    warn_threshold = config.safety.max_outbound_links_warn
    logging.info(f"Post analysis: Found {link_count} unique outbound link(s).")
    if link_count > MAX_OUTBOUND_LINKS_ERROR:
        logging.error(
            f"Post contains {link_count} links, exceeding safety limit of {MAX_OUTBOUND_LINKS_ERROR}. Aborting."
        )
        sys.exit(1)
    if link_count > warn_threshold:
        logging.warning(
            f"Post contains {link_count} links, which is above the warning threshold of {warn_threshold}."
        )

    # Check dry-run level for different behaviors
    dry_run_level = get_dry_run_level()

    if dry_run_level == 0:  # Full dry-run
        logging.info(f"DRY_RUN: Would submit new post to r/{config.reddit.subreddit}")
        logging.info(f"  Title: {title}")
        logging.info(f"  Body: {body[:200]}...")  # Log first 200 chars of body
        # Return a mock submission object
        mock_submission = MagicMock()
        mock_submission.id = "mock-post-id-dry-run"
        mock_submission.title = title
        mock_submission.shortlink = "https://dry-run.reddit.post/mock-post-id"
        return mock_submission
    if dry_run_level in [1, 2]:  # Read-only or safe writes
        logging.info(
            f"DRY_RUN_LEVEL_{dry_run_level}: Would submit new post to r/{config.reddit.subreddit}"
        )
        logging.info(f"  Title: {title}")
        logging.info(f"  Body: {body[:200]}...")  # Log first 200 chars of body
        # Return a mock submission object
        mock_submission = MagicMock()
        mock_submission.id = "mock-post-id-read-only"
        mock_submission.title = title
        mock_submission.shortlink = "https://dry-run.reddit.post/mock-post-id"
        return mock_submission
    if dry_run_level == DryRunLevel.PUBLIC_PREVIEW:  # Public preview - create draft
        if is_dry_run():
            logging.info(
                f"PUBLIC_PREVIEW: Would submit draft post to r/{config.reddit.subreddit}"
            )
            logging.info(f"  Title: {title}")
            logging.info(f"  Body: {body[:200]}...")
            mock_submission = MagicMock()
            mock_submission.id = "mock-post-id-preview"
            mock_submission.title = f"[DRAFT] {title}"
            mock_submission.shortlink = "https://preview.reddit.post/mock-post-id"
            return mock_submission
        logging.info(f"Submitting draft post to r/{config.reddit.subreddit}: {title}")
        submission = reddit.subreddit(config.reddit.subreddit)
        # Submit as selftext but mark as draft (if Reddit API supports it)
        submission = submission.submit(f"[DRAFT] {title}", selftext=body)
        logging.info(f"Draft post successful: {submission.shortlink}")
        return submission
    # Production mode
    logging.info(f"Submitting new post to r/{config.reddit.subreddit}: {title}")
    submission = reddit.subreddit(config.reddit.subreddit)
    submission = submission.submit(title, selftext=body)
    logging.info(f"Post successful: {submission.shortlink}")
    return submission
