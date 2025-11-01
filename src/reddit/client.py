"""Reddit client initialization."""

from typing import Any

import deal
import praw
from beartype import beartype

from core.credentials import Credentials
from core.errors import RedditAPIError
from core.result import Err, Ok, Result
from core.retry import retry


@deal.pre(lambda _config: _config is None or isinstance(_config, dict))  # type: ignore[misc]
@beartype  # type: ignore[misc]
@retry(max_attempts=3, on=[RedditAPIError])
def init_reddit(_config: dict[str, Any] | None = None) -> Result[praw.Reddit, RedditAPIError]:
    """Initializes and returns a PRAW Reddit instance."""
    try:
        reddit = praw.Reddit(
            client_id=Credentials.get_reddit_client_id(),
            client_secret=Credentials.get_reddit_client_secret(),
            user_agent=Credentials.get_reddit_user_agent(),
            username=Credentials.get_reddit_username(),
            password=Credentials.get_reddit_password(),
            validate_on_submit=True,
        )
        # Test connection
        reddit.user.me()
        return Ok(reddit)
    except Exception as e:
        return Err(RedditAPIError(f"Failed to initialize Reddit client: {e}"))
