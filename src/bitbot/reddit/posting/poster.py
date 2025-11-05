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
MAX_OUTBOUND_LINKS_ERROR = 8


@deal.post(lambda result: result >= 0)
@beartype
def count_outbound_links(text: str) -> int:
    """Count outbound links in text."""
    url_pattern = re.compile(r"https?://[^\s/$.?#].[^\s]*|www\.[^\s/$.?#].[^\s]*")
    return len(set(url_pattern.findall(text)))


@deal.pre(
    lambda _r, title, _p, _c: len(title) > 0,
    message="Title cannot be empty",
)
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
    link_count = count_outbound_links(post_body)
    warn_threshold: int = config.safety.get("max_outbound_links_warn", 5)

    if link_count > MAX_OUTBOUND_LINKS_ERROR:
        msg = (
            f"Post contains {link_count} outbound links, "
            f"exceeds limit of {MAX_OUTBOUND_LINKS_ERROR}"
        )
        return Err(RedditAPIError(msg))
    if link_count > warn_threshold:
        logger.warning(
            "Post contains %d outbound links (threshold: %d)", link_count, warn_threshold
        )

    try:
        submission = reddit.subreddit(config.reddit.subreddit).submit(title, selftext=post_body)
        return Ok(submission)
    except RedditAPIException as e:
        return Err(RedditAPIError(f"Reddit API error: {e}"))
    except Exception as e:
        return Err(RedditAPIError(f"Failed to post to Reddit: {e}"))
