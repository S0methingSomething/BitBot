"""Reddit client initialization."""

import praw
from beartype import beartype
from tenacity import retry, retry_if_result, stop_after_attempt, wait_exponential

from bitbot.config_models import Config
from bitbot.core.credentials import Credentials
from bitbot.core.errors import RedditAPIError
from bitbot.core.result import Err, Ok, Result


@retry(
    retry=retry_if_result(lambda r: r.is_err()),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
)
@beartype
def init_reddit(_config: Config | None = None) -> Result[praw.Reddit, RedditAPIError]:
    """Initializes and returns a PRAW Reddit instance."""
    try:
        reddit = praw.Reddit(
            client_id=Credentials.get_reddit_client_id(),
            client_secret=Credentials.get_reddit_client_secret(),
            user_agent=Credentials.get_reddit_user_agent(_config),
            username=Credentials.get_reddit_username(),
            password=Credentials.get_reddit_password(),
            validate_on_submit=True,
        )
        # Test connection
        reddit.user.me()
        return Ok(reddit)
    except (ValueError, praw.exceptions.PRAWException) as e:
        return Err(RedditAPIError(f"Failed to initialize Reddit client: {e}"))
