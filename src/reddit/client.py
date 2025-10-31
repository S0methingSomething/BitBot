"""Reddit client initialization."""

from typing import Any

import deal
import praw
from beartype import beartype

from core.credentials import Credentials


@deal.post(lambda result: result is not None)  # type: ignore[misc]
@beartype  # type: ignore[misc]
def init_reddit(_config: dict[str, Any] | None = None) -> praw.Reddit:
    """Initializes and returns a PRAW Reddit instance."""
    return praw.Reddit(
        client_id=Credentials.get_reddit_client_id(),
        client_secret=Credentials.get_reddit_client_secret(),
        user_agent=Credentials.get_reddit_user_agent(),
        username=Credentials.get_reddit_username(),
        password=Credentials.get_reddit_password(),
        validate_on_submit=True,
    )
