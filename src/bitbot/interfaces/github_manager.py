"""Protocol for interacting with the GitHub API."""

from typing import Optional, Protocol

from bitbot.data.models import GitHubRelease


class GitHubManagerProtocol(Protocol):
    """Defines the interface for a GitHub API manager."""

    async def get_latest_release(self, repo: str) -> Optional[GitHubRelease]:
        """
        Gets the latest release for a given repository.

        Args:
            repo: The name of the repository (e.g., "user/repo").

        Returns:
            Optional[GitHubRelease]: The latest release, or None if not found.
        """
        ...

    async def validate_credentials(self) -> None:
        """
        Validates the GitHub credentials.

        Raises:
            InvalidCredentialsError: If the credentials are invalid.
        """
        ...
