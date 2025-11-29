"""Reddit client initialization."""

import praw
from beartype import beartype

from bitbot.config_models import Config
from bitbot.core.credentials import (
    get_reddit_client_id,
    get_reddit_client_secret,
    get_reddit_password,
    get_reddit_user_agent,
    get_reddit_username,
)
from bitbot.core.errors import RedditAPIError
from bitbot.core.result import Err, Ok, Result
from bitbot.core.retry import retry_on_err


@retry_on_err()
@beartype
def init_reddit(_config: Config | None = None) -> Result[praw.Reddit, RedditAPIError]:
    """Initializes and returns a PRAW Reddit instance."""
    try:
        reddit = praw.Reddit(
            client_id=get_reddit_client_id(),
            client_secret=get_reddit_client_secret(),
            user_agent=get_reddit_user_agent(_config),
            username=get_reddit_username(),
            password=get_reddit_password(),
            validate_on_submit=True,
        )
        # Test connection
        reddit.user.me()
        return Ok(reddit)
    except (ValueError, praw.exceptions.PRAWException) as e:
        return Err(RedditAPIError(f"Failed to initialize Reddit client: {e}"))
