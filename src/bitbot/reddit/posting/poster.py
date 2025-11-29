"""Reddit post submission."""

import re
from typing import TYPE_CHECKING

import deal
from beartype import beartype
from praw.exceptions import RedditAPIException

from bitbot.config_models import Config
from bitbot.core.error_logger import get_logger
from bitbot.core.errors import RedditAPIError
from bitbot.core.result import Err, Ok, Result
from bitbot.core.retry import retry_on_err

if TYPE_CHECKING:
    import praw

logger = get_logger()


@deal.post(lambda result: result >= 0)
@beartype
def count_outbound_links(text: str) -> int:
    """Count outbound links in text."""
    url_pattern = re.compile(r"https?://[^\s/$.?#].[^\s]*|www\.[^\s/$.?#].[^\s]*")
    return len(set(url_pattern.findall(text)))


@beartype
def _check_link_safety(post_body: str, config: Config) -> Result[None, RedditAPIError]:
    """Check if post has too many outbound links."""
    link_count = count_outbound_links(post_body)
    warn_threshold = config.safety.get("max_outbound_links_warn", 5)
    error_threshold = config.safety.get("max_outbound_links_error", 8)

    if link_count > error_threshold:
        return Err(
            RedditAPIError(
                f"Post contains {link_count} outbound links, exceeds limit of {error_threshold}"
            )
        )
    if link_count > warn_threshold:
        logger.warning(
            "Post contains %d outbound links (threshold: %d)", link_count, warn_threshold
        )
    return Ok(None)


@deal.pre(
    lambda _r, _p, post_body, _c: len(post_body) > 0,
    message="Post body cannot be empty",
)
@retry_on_err()
@beartype
def update_post(
    reddit: "praw.Reddit", post_id: str, post_body: str, config: Config
) -> Result["praw.models.Submission", RedditAPIError]:
    """Update existing Reddit post."""
    safety_check = _check_link_safety(post_body, config)
    if safety_check.is_err():
        return Err(safety_check.unwrap_err())

    try:
        submission = reddit.submission(id=post_id)
        submission.edit(post_body)
        return Ok(submission)
    except RedditAPIException as e:
        return Err(RedditAPIError(f"Reddit API error: {e}"))
    except Exception as e:
        return Err(RedditAPIError(f"Failed to update Reddit post: {e}"))


@deal.pre(
    lambda _r, _t, post_body, _c: len(post_body) > 0,
    message="Post body cannot be empty",
)
@retry_on_err()
@beartype
def post_new_release(
    reddit: "praw.Reddit", title: str, post_body: str, config: Config
) -> Result["praw.models.Submission", RedditAPIError]:
    """Post new release to Reddit."""
    safety_check = _check_link_safety(post_body, config)
    if safety_check.is_err():
        return Err(safety_check.unwrap_err())

    try:
        submission = reddit.subreddit(config.reddit.subreddit).submit(title, selftext=post_body)
        return Ok(submission)
    except RedditAPIException as e:
        return Err(RedditAPIError(f"Reddit API error: {e}"))
    except Exception as e:
        return Err(RedditAPIError(f"Failed to post to Reddit: {e}"))
