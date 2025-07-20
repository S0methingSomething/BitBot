"""Protocol for the Reddit management service."""

from typing import Any, List, Optional, Protocol

from ..data.models import RedditPost


class RedditManagerProtocol(Protocol):
    """A protocol for managing Reddit interactions."""

    async def get_post_by_id(self, post_id: str) -> Optional[RedditPost]:
        """Gets a Reddit post by its ID."""
        ...

    async def get_comments(self, post: RedditPost) -> List[Any]:
        """Gets the comments from a Reddit post."""
        ...

    async def get_recent_bot_posts(self, limit: int) -> List[RedditPost]:
        """Gets a list of recent posts made by the bot."""
        ...

    async def update_post_body(self, post_id: str, new_body: str) -> None:
        """Updates the body of a Reddit post."""
        ...

    async def submit_post(self, title: str, body: str) -> RedditPost:
        """Submits a new post to Reddit."""
        ...

    async def close(self) -> None:
        """Closes the Reddit session."""
        ...
