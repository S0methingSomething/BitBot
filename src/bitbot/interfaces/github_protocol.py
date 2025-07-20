"""Protocol for the GitHub management service."""

from typing import Optional, Protocol

from ..data.models import GitHubRelease


class GitHubManagerProtocol(Protocol):
    """A protocol for managing GitHub interactions."""

    async def get_latest_release(self, repo_slug: str) -> Optional[GitHubRelease]:
        """Gets the latest release from a GitHub repository."""
        ...

    async def close(self) -> None:
        """Closes the GitHub session."""
        ...
