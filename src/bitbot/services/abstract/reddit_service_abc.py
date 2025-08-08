"""Abstract interfaces for Reddit services."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from ...models.reddit_post import RedditPost


@dataclass(frozen=True)
class BotPost:
    """A simple, immutable data structure for a Reddit post."""

    id: str
    title: str


class RedditServiceABC(ABC):
    """An abstract base class defining the interface for a Reddit service."""

    @abstractmethod
    def get_bot_posts(self) -> list[BotPost]:
        """Fetch all of the bot's release posts."""
        raise NotImplementedError

    @abstractmethod
    def create_post(self, post: RedditPost) -> str:
        """Create a new post on Reddit.

        Args:
            post: The post to create.

        Returns:
            The ID of the newly created post.
        """
        raise NotImplementedError

    @abstractmethod
    def update_post(self, post_id: str, post: RedditPost) -> None:
        """Update an existing post on Reddit.

        Args:
            post_id: The ID of the post to update.
            post: The new content for the post.
        """
        raise NotImplementedError
