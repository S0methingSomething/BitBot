# src/bitbot/services/api_clients.py
"""
Clients for interacting with external APIs like GitHub and Reddit.
"""

import httpx

from ..core import ApplicationCore
from ..domain.models import GitHubRelease, RedditPost


class GitHubClient:
    """A client for interacting with the GitHub API."""

    BASE_URL = "https://api.github.com"

    def __init__(self, core: ApplicationCore):
        self._core = core

    @property
    def _broker(self):
        return self._core.broker

    async def get_latest_releases(self) -> list[GitHubRelease]:
        """Fetches the latest releases from the source repository."""
        source_repo = self._core.settings.github.source_repo
        url = f"{self.BASE_URL}/repos/{source_repo}/releases?per_page=30"

        response_data = await self._broker.request_network_call(
            requester=self,
            method="GET",
            url=url,
            # In a real app, we'd handle headers and auth here
        )
        if response_data is None:
            return []
        return [GitHubRelease.model_validate(release) for release in response_data]

    async def create_release(self, release: GitHubRelease) -> GitHubRelease:
        """Creates a new release in the bot's repository."""
        bot_repo = self._core.settings.github.bot_repo
        url = f"{self.BASE_URL}/repos/{bot_repo}/releases"

        response_data = await self._broker.request_network_call(
            requester=self,
            method="POST",
            url=url,
            json=release.model_dump(include={"tag_name", "body"}),
            # In a real app, we'd handle headers and auth here
        )
        if response_data is None:
            # This would ideally be a more specific exception
            raise Exception("Failed to create release")
        return GitHubRelease.model_validate(response_data)


class RedditClient:
    """
    A client for interacting with the Reddit API.

    This class acts as an Adapter to translate untyped asyncpraw objects
    into our trusted Pydantic domain models.
    """

    def __init__(self, core: ApplicationCore):
        self._core = core

    @property
    def _broker(self):
        return self._core.broker

    async def submit_post(self, post: RedditPost) -> RedditPost:
        """Submits a new post to the configured subreddit."""
        subreddit_name = self._core.settings.reddit.subreddit
        # In a real implementation, we would use asyncpraw here.
        # For now, we'll just simulate the call through the broker.
        response_data = await self._broker.request_network_call(
            requester=self,
            method="POST",
            url=f"https://oauth.reddit.com/r/{subreddit_name}/submit",
            json=post.model_dump(include={"title", "selftext", "url"}),
        )
        if response_data is None:
            raise Exception("Failed to submit post")
        # Assuming the response contains the ID of the new post
        return post.model_copy(update=response_data)


class ApiClientService:
    """A service that provides access to all API clients."""

    def __init__(self, core: ApplicationCore):
        self.github = GitHubClient(core)
        self.reddit = RedditClient(core)
