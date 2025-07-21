"""Service for interacting with the GitHub API using aiohttp."""

from typing import Optional

import aiohttp
from tenacity import retry, stop_after_attempt, wait_fixed

from bitbot.data.models import GitHubRelease
from bitbot.errors import InvalidCredentialsError
from bitbot.interfaces.github_manager import GitHubManagerProtocol


class AiohttpGitHubManager(GitHubManagerProtocol):
    """Manages GitHub API interactions using aiohttp."""

    def __init__(self, token: str) -> None:
        """
        Initializes the AiohttpGitHubManager.

        Args:
            token: The GitHub API token.
        """
        self._headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def get_latest_release(self, repo: str) -> Optional[GitHubRelease]:
        """
        Gets the latest release for a given repository.

        Args:
            repo: The name of the repository (e.g., "user/repo").

        Returns:
            Optional[GitHubRelease]: The latest release, or None if not found.
        """
        url = f"https://api.github.com/repos/{repo}/releases/latest"
        async with (
            aiohttp.ClientSession(headers=self._headers) as session,
            session.get(url) as response,
        ):
            if response.status == 404:
                return None
            response.raise_for_status()
            data = await response.json()
            return GitHubRelease(
                version=data["tag_name"],
                url=data["html_url"],
                body=data.get("body"),
            )

    async def validate_credentials(self) -> None:
        """
        Validates the GitHub credentials.

        Raises:
            InvalidCredentialsError: If the credentials are invalid.
        """
        url = "https://api.github.com/user"
        async with (
            aiohttp.ClientSession(headers=self._headers) as session,
            session.get(url) as response,
        ):
            if response.status == 401:
                raise InvalidCredentialsError("GitHub", "Token is invalid.")
            response.raise_for_status()
