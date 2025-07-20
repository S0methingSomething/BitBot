"""A service for managing GitHub interactions."""

from typing import Optional

import aiohttp

from ..data.models import GitHubRelease
from ..interfaces.github_protocol import GitHubManagerProtocol


class GitHubManager(GitHubManagerProtocol):
    """Manages GitHub interactions."""

    def __init__(self, session: aiohttp.ClientSession, token: str) -> None:
        """Initializes the GitHubManager."""
        self.session = session
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
        }

    async def get_latest_release(self, repo_slug: str) -> Optional[GitHubRelease]:
        """Gets the latest release from a GitHub repository."""
        api_url = f"https://api.github.com/repos/{repo_slug}/releases/latest"
        async with self.session.get(api_url, headers=self.headers) as response:
            response.raise_for_status()
            release_data = await response.json()
            return GitHubRelease(**release_data)

    async def close(self) -> None:
        """Closes the GitHub session."""
        await self.session.close()
