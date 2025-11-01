"""Error types for BitBot."""

from datetime import datetime
from typing import Any

from beartype import beartype


class BitBotError(Exception):
    """Base error for all BitBot errors."""

    @beartype
    def __init__(self, message: str, context: dict[str, Any] | None = None) -> None:
        """Initialize error with message and optional context."""
        super().__init__(message)
        self.message = message
        self.context = context or {}
        self.timestamp = datetime.now()

    @beartype
    def to_dict(self) -> dict[str, Any]:
        """Convert error to dict for serialization."""
        return {
            "type": self.__class__.__name__,
            "message": self.message,
            "context": self.context,
            "timestamp": self.timestamp.isoformat(),
        }


class TransientError(BitBotError):
    """Retry-able error (network, rate limits)."""


class PermanentError(BitBotError):
    """Not retry-able (404, validation)."""


class ConfigurationError(BitBotError):
    """Configuration or setup error."""


class StateError(BitBotError):
    """State corruption or inconsistency."""


class ExternalAPIError(BitBotError):
    """Base for external API errors."""


class RedditAPIError(ExternalAPIError):
    """Reddit API error."""


class GitHubAPIError(ExternalAPIError):
    """GitHub API error."""
