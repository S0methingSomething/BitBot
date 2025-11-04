"""Error types for BitBot."""

from datetime import UTC, datetime
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
        self.timestamp = datetime.now(UTC)

    @beartype
    def to_dict(self) -> dict[str, Any]:
        """Convert error to dict for serialization."""
        return {
            "type": self.__class__.__name__,
            "message": self.message,
            "context": self.context,
            "timestamp": self.timestamp.isoformat(),
        }

    def __str__(self) -> str:
        """String representation."""
        ctx = f" (context: {self.context})" if self.context else ""
        return f"{self.__class__.__name__}: {self.message}{ctx}"

    def __repr__(self) -> str:
        """Detailed representation."""
        return (
            f"{self.__class__.__name__}(message={self.message!r}, "
            f"context={self.context!r}, timestamp={self.timestamp.isoformat()!r})"
        )


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


class ReleaseQueueError(BitBotError):
    """Release queue operation error."""


class PageGeneratorError(BitBotError):
    """Landing page generation error."""
