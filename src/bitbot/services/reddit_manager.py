"""Service for interacting with the Reddit API using asyncpraw."""

import asyncpraw
from asyncprawcore.exceptions import OAuthException, ResponseException
from bitbot.data.models import RedditPost, Settings
from bitbot.errors import InvalidCredentialsError
from bitbot.interfaces.reddit_manager import RedditManagerProtocol


class PrawRedditManager(RedditManagerProtocol):
    """Manages Reddit API interactions using asyncpraw."""

    def __init__(self, settings: Settings) -> None:
        """
        Initializes the PrawRedditManager.

        Args:
            settings: The application settings.
        """
        self._reddit = asyncpraw.Reddit(
            client_id=settings.reddit_client_id,
            client_secret=settings.reddit_client_secret,
            user_agent=settings.reddit_user_agent,
            username=settings.reddit_username,
            password=settings.reddit_password,
        )

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
        sub = await self._reddit.subreddit(subreddit)
        submission = await sub.submit(title, selftext=body)
        return RedditPost(
            id=submission.id,
            url=submission.url,
            title=submission.title,
            body=submission.selftext,
        )

    async def validate_credentials(self) -> None:
        """
        Validates the Reddit credentials.

        Raises:
            InvalidCredentialsError: If the credentials are invalid.
        """
        try:
            await self._reddit.user.me()
        except (OAuthException, ResponseException) as e:
            raise InvalidCredentialsError("Reddit", str(e)) from e
