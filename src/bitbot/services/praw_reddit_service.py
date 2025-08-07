"""A Reddit service implementation using the PRAW library."""

import os

import praw

from ..models.config import RedditConfig
from .abstract.reddit_service_abc import BotPost, RedditServiceABC
from .logging_service import LoggingService


class PrawRedditService(RedditServiceABC):
    """A service for interacting with the Reddit API using PRAW."""

    def __init__(self, config: RedditConfig, logger: LoggingService):
        """Initialize the PrawRedditService."""
        self._config = config
        self._logger = logger
        self._reddit = self._init_reddit()

    def _init_reddit(self) -> praw.Reddit:
        """Initialize and return a PRAW Reddit instance."""
        return praw.Reddit(
            client_id=os.environ["REDDIT_CLIENT_ID"],
            client_secret=os.environ["REDDIT_CLIENT_SECRET"],
            user_agent=os.environ["REDDIT_USER_AGENT"],
            username=os.environ["REDDIT_USERNAME"],
            password=os.environ["REDDIT_PASSWORD"],
            validate_on_submit=True,
        )

    def get_bot_posts(self) -> list[BotPost]:
        """Fetch all of the bot's release posts from the configured subreddit."""
        bot_user = self._reddit.user.me()
        if not bot_user:
            self._logger.warning("Could not authenticate with Reddit. Returning no posts.")
            return []

        target_subreddit = self._config.subreddit.lower()
        post_identifier = "[BitBot]"  # A common, unique prefix for all posts.

        bot_posts: list[BotPost] = []
        for submission in bot_user.submissions.new(limit=100):
            try:
                if submission.subreddit.display_name.lower() == target_subreddit and submission.title.startswith(
                    post_identifier
                ):
                    # Translate the raw PRAW object to our clean, immutable BotPost
                    bot_posts.append(BotPost(id=submission.id, title=submission.title))
            except AttributeError as e:
                self._logger.warning(
                    f"Skipping a Reddit post due to unexpected data structure: {e}. Post ID: {getattr(submission, 'id', 'N/A')}"
                )
                continue
        return bot_posts
