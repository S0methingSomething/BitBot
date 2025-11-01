"""Reddit client initialization."""

from typing import Any

import deal
import praw
from beartype import beartype
from tenacity import retry, retry_if_result, stop_after_attempt, wait_exponential

from core.credentials import Credentials
from core.errors import RedditAPIError
from core.result import Err, Ok, Result
from core.tenacity_helpers import log_retry_attempt, should_retry_api_error


@deal.pre(lambda _config: _config is None or isinstance(_config, dict))  # type: ignore[misc]
@beartype  # type: ignore[misc]
@retry(
    retry=retry_if_result(should_retry_api_error),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    before_sleep=log_retry_attempt,
)
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
