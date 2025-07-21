"""Protocol for interacting with the Reddit API."""

from typing import Protocol

from bitbot.data.models import RedditPost


class RedditManagerProtocol(Protocol):
    """Defines the interface for a Reddit API manager."""

    async def submit_post(self, subreddit: str, title: str, body: str) -> RedditPost:
        """
        Submits a new post to a subreddit.

        Args:
            subreddit: The name of the subreddit.
            title: The title of the post.
            body: The content of the post (in Markdown).

        Returns:
            RedditPost: The created Reddit post.
        """
        ...

    async def validate_credentials(self) -> None:
        """
        Validates the Reddit credentials.

        Raises:
            InvalidCredentialsError: If the credentials are invalid.
        """
        ...
