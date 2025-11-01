"""Reddit post submission."""

import re
import sys
from typing import TYPE_CHECKING, Any

import deal
from beartype import beartype
from praw.exceptions import RedditAPIException

if TYPE_CHECKING:
    import praw

MAX_OUTBOUND_LINKS_ERROR = 8


@deal.pre(lambda text: len(text) >= 0)  # type: ignore[misc]
@deal.post(lambda result: result >= 0)  # type: ignore[misc]
@beartype
def count_outbound_links(text: str) -> int:
    """Count outbound links in text."""
    url_pattern = re.compile(r"https?://[^\s/$.?#].[^\s]*|www\.[^\s/$.?#].[^\s]*")
    return len(set(url_pattern.findall(text)))


@deal.pre(lambda _r, title, _p, _c: len(title) > 0)  # type: ignore[misc]
@deal.pre(lambda _r, _t, post_body, _c: len(post_body) > 0)  # type: ignore[misc]
@deal.pre(lambda _r, _t, _p, config: isinstance(config, dict))  # type: ignore[misc]
@deal.post(lambda result: result is not None)  # type: ignore[misc]
@beartype
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
    except Exception:
        sys.exit(1)
