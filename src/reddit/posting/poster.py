"""Reddit post submission."""

import re
import sys
from typing import TYPE_CHECKING, Any

from praw.exceptions import RedditAPIException

if TYPE_CHECKING:
    import praw

MAX_OUTBOUND_LINKS_ERROR = 8


def count_outbound_links(text: str) -> int:
    """Count outbound links in text."""
    url_pattern = re.compile(r"https?://[^\s/$.?#].[^\s]*|www\.[^\s/$.?#].[^\s]*")
    return len(set(url_pattern.findall(text)))


def post_new_release(
    reddit: "praw.Reddit", title: str, post_body: str, config: dict[str, Any]
) -> "praw.models.Submission":
    """Post new release to Reddit."""
    link_count = count_outbound_links(post_body)
    warn_threshold: int = config.get("safety", {}).get("max_outbound_links_warn", 5)

    if link_count > MAX_OUTBOUND_LINKS_ERROR:
        sys.exit(1)
    if link_count > warn_threshold:
        pass

    try:
        return reddit.subreddit(config["reddit"]["subreddit"]).submit(title, selftext=post_body)
    except RedditAPIException:
        sys.exit(1)
    except Exception:  # noqa: BLE001
        sys.exit(1)
