"""Abstract interfaces for Reddit services."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


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
