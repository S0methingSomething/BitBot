import logging
import os
import sys
from typing import Any, cast

import praw
import requests
from praw.models import Submission
from tenacity import RetryError, retry, stop_after_attempt, wait_exponential

from .config import Config


class GitHubClient:
    """A resilient client for all GitHub API interactions."""

    def __init__(self, config: Config, token: str):
        if not token:
            raise ValueError("GitHub token cannot be empty.")
        self.config = config.github
        self.api_base = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))  # type: ignore[misc]
    def _request(
        self, method: str, url: str, **kwargs: Any
    ) -> requests.Response | None:
        """Makes a request with unified headers, timeout, and retry logic."""
        try:
            response = requests.request(
                method, url, headers=self.headers, timeout=30, **kwargs
            )
            response.raise_for_status()
        except requests.HTTPError as e:
            if 400 <= e.response.status_code < 500:
                logging.error(f"Client error: {e.response.status_code} for URL {url}")
                return None  # Don't retry on client errors
            raise
        return response

    def get_latest_release(self, repo_slug: str) -> dict[str, Any] | None:
        """Fetches the latest release from a given repository."""
        url = f"{self.api_base}/repos/{repo_slug}/releases/latest"
        try:
            response = self._request("GET", url)
            if response:
                return cast(dict[str, Any], response.json())
            return None
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                logging.warning(f"No releases found for {repo_slug}. Returning None.")
                return None
            raise
        except RetryError as e:
            logging.error(
                "Failed to fetch latest release from %s after multiple retries: %s",
                repo_slug,
                e,
            )
            raise
        return None

    def download_asset(self, url: str) -> bytes:
        """Downloads a release asset."""
        try:
            headers = self.headers.copy()
            headers["Accept"] = "application/octet-stream"
            response = requests.get(url, headers=headers, timeout=60, stream=True)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            logging.error(f"Failed to download asset from {url}: {e}")
            raise

    def create_release(
        self, tag_name: str, release_name: str, body: str
    ) -> dict[str, Any]:
        """Creates a new GitHub release."""
        url = f"{self.api_base}/repos/{self.config.bot_repo}/releases"
        payload = {"tag_name": tag_name, "name": release_name, "body": body}
        response = self._request("POST", url, json=payload)
        return cast(dict[str, Any], response.json())

    def upload_asset(self, upload_url: str, asset_name: str, data: bytes) -> None:
        """Uploads an asset to a release."""
        url = upload_url.split("{")[0] + f"?name={asset_name}"
        headers = self.headers.copy()
        headers["Content-Type"] = "application/octet-stream"
        self._request("POST", url, data=data)

    def mark_old_releases_outdated(self) -> None:
        """
        Finds all releases except the latest and prepends '[OUTDATED]' to their titles.
        """
        url = f"{self.api_base}/repos/{self.config.bot_repo}/releases"
        response = self._request("GET", url)
        if not response:
            return
        releases = cast(list[dict[str, Any]], response.json())
        if not releases or len(releases) < 2:
            logging.info("Not enough releases to mark any as outdated.")
            return

        for release in releases[1:]:
            if not release["name"].startswith("[OUTDATED] "):
                logging.info(f"Marking release '{release['name']}' as outdated.")
                update_url = release["url"]
                payload = {"name": f"[OUTDATED] {release['name']}"}
                self._request("PATCH", update_url, json=payload)


class RedditClient:
    """A client for all PRAW/Reddit interactions."""

    def __init__(self, config: Config):
        required_vars = [
            "REDDIT_CLIENT_ID",
            "REDDIT_CLIENT_SECRET",
            "REDDIT_USER_AGENT",
            "REDDIT_USERNAME",
            "REDDIT_PASSWORD",
        ]
        for var in required_vars:
            if not os.environ.get(var):
                logging.critical(f"Missing required environment variable: {var}")
                sys.exit(1)

        self.reddit = praw.Reddit(
            client_id=os.environ["REDDIT_CLIENT_ID"],
            client_secret=os.environ["REDDIT_CLIENT_SECRET"],
            user_agent=os.environ["REDDIT_USER_AGENT"],
            username=os.environ["REDDIT_USERNAME"],
            password=os.environ["REDDIT_PASSWORD"],
        )
        self.subreddit = self.reddit.subreddit(config.reddit.subreddit)
        self.post_title_template = config.messages["postTitle"]
        self.asset_name = config.github.asset_file_name

    def get_bot_submissions(self, limit: int = 100) -> list[Submission]:
        """
        Gets the bot's recent submissions that match the release post format
        using a robust subreddit search query.
        """
        # Ensure we can get the bot's username for the search query
        try:
            bot_username = self.reddit.user.me().name
        except Exception:
            logging.error("Could not authenticate with Reddit to get bot username.")
            return []

        # Construct a search query that is more reliable than iterating.
        # This searches for posts by the bot with a title matching the format.
        post_identifier = (
            self.post_title_template.split("{{version}}")[0]
            .replace("{{asset_name}}", self.asset_name)
            .strip()
        )

        # We need to escape special characters for Reddit's search syntax.
        # For this title, double quotes are the most likely issue.
        search_title = post_identifier.replace('"', '\\"')

        query = f'author:"{bot_username}" title:"{search_title}"'

        logging.info(
            f"Searching subreddit '{self.subreddit.display_name}' with query: {query}"
        )

        try:
            # Use list() to execute the search generator and get results
            search_results = list(self.subreddit.search(query, sort="new", limit=limit))
            logging.info(f"Found {len(search_results)} post(s) matching the query.")
            return search_results
        except Exception as e:
            logging.error(
                f"An exception occurred during Reddit search: {e}", exc_info=True
            )
            return []

    def submit_post(self, title: str, selftext: str) -> Submission:
        """Submits a new post to the configured subreddit."""
        return self.subreddit.submit(title, selftext=selftext)
