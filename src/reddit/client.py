"""Reddit client initialization."""

import deal
import praw
from beartype import beartype

from src.config_models import Config
from src.core.credentials import Credentials
from src.core.errors import RedditAPIError
from src.core.result import Err, Ok, Result


@deal.pre(lambda _config: _config is None or isinstance(_config, Config))
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
    except Exception as e:
        return Err(RedditAPIError(f"Failed to initialize Reddit client: {e}"))
