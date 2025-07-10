import logging
from typing import Any, cast

import praw
import requests
from praw.models import Submission
from tenacity import RetryError, retry, stop_after_attempt, wait_exponential

from .config import Config, Credentials
from .messages import ExitMessages
from .utils import log_and_exit

# Use DEBUG for verbose, step-by-step logging during development/troubleshooting
# Change to logging.INFO for production to reduce noise
LOG_LEVEL = logging.DEBUG


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

    def test_connection(self) -> bool:
        """Tests the connection to the GitHub API."""
        url = f"{self.api_base}/user"
        try:
            response = self._request("GET", url)
            if response:
                logging.info("GitHub API connection successful.")
                return True
            logging.error("GitHub API connection failed.")
            return False
        except requests.HTTPError as e:
            logging.error(f"GitHub API connection failed: {e}")
            return False
        except RetryError as e:
            logging.error(f"GitHub API connection failed after multiple retries: {e}")
            return False

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
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

    def get_release_by_tag(self, tag_name: str) -> dict[str, Any] | None:
        """Fetches a specific release by its tag name."""
        url = f"{self.api_base}/repos/{self.config.bot_repo}/releases/tags/{tag_name}"
        try:
            response = self._request("GET", url)
            if response:
                return cast(dict[str, Any], response.json())
        except requests.HTTPError as e:
            if e.response and e.response.status_code == 404:
                logging.info(f"Release with tag '{tag_name}' not found.")
                return None
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

    def delete_asset(self, asset_id: int) -> None:
        """Deletes a release asset by its ID."""
        url = f"{self.api_base}/repos/{self.config.bot_repo}/releases/assets/{asset_id}"
        self._request("DELETE", url)
        logging.info(f"Deleted existing asset with ID: {asset_id}")

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

    def __init__(self, config: Config, creds: Credentials):
        self.reddit = praw.Reddit(
            client_id=creds.reddit_client_id,
            client_secret=creds.reddit_client_secret,
            user_agent=creds.reddit_user_agent,
            username=creds.reddit_username,
            password=creds.reddit_password,
        )
        self.subreddit_name = config.reddit.subreddit
        self.subreddit = self.reddit.subreddit(self.subreddit_name)
        self.bot_name = config.reddit.bot_name
        self.post_title_template = config.reddit.post_title
        self.asset_name = config.github.asset_file_name

    def test_connection(self) -> bool:
        """Tests the connection to the Reddit API."""
        try:
            user = self.reddit.user.me()
            if user:
                logging.info(
                    f"Reddit API connection successful. Logged in as u/{user.name}."
                )
                return True
            logging.error("Reddit API connection failed. User is None.")
            return False
        except Exception as e:
            logging.error(f"Reddit API connection failed: {e}")
            return False

    def get_bot_submissions(self, limit: int = 100) -> list[Submission]:
        """
        Gets the bot's recent submissions by searching the configured subreddit
        for posts made by the bot. This is more resilient to title changes.
        """
        try:
            bot_user = self.reddit.user.me()
            if not bot_user:
                logging.error("Failed to authenticate with Reddit. Bot user is None.")
                return []
            bot_username = bot_user.name
            logging.info(
                "Will search for posts by authenticated user: u/%s", bot_username
            )
        except Exception as e:
            logging.error(
                "Could not authenticate with Reddit to get bot user: %s",
                e,
                exc_info=True,
            )
            return []

        # Search for posts by the bot in the target subreddit.
        query = f"author:{bot_username}"
        # The title prefix, e.g., "[BitBot]", is a stable identifier.
        post_prefix = f"[{self.bot_name}]"

        logging.info(
            "Searching r/%s for posts with query: '%s' and title prefix: '%s'",
            self.subreddit_name,
            query,
            post_prefix,
        )

        matching_posts = []
        try:
            # Search the subreddit and sort by new to get the most recent posts first.
            for submission in self.subreddit.search(query, sort="new", limit=limit):
                # The search query handles the author,
                # Now we apply a stable title check.
                if submission.title.strip().startswith(post_prefix):
                    logging.info(
                        "    - ACCEPT: Found valid post %s ('%s')",
                        submission.id,
                        submission.title,
                    )
                    matching_posts.append(submission)
                else:
                    logging.log(
                        LOG_LEVEL,
                        "    - REJECT: Post %s from search results "
                        "did not match title prefix '%s'",
                        submission.id,
                        post_prefix,
                    )

            logging.info(
                "Search complete. Found %d matching post(s).", len(matching_posts)
            )
            return matching_posts

        except Exception as e:
            logging.error(
                "An unexpected error occurred while searching Reddit: %s",
                e,
                exc_info=True,
            )
            return []

    def submit_post(self, title: str, selftext: str) -> Submission:
        """Submits a new post to the configured subreddit."""
        return self.subreddit.submit(title, selftext=selftext)


def get_clients(
    config: Config, creds: Credentials
) -> tuple[GitHubClient, RedditClient] | None:
    """Initializes and returns all API clients if credentials are valid."""
    if not creds.github_token:
        log_and_exit(ExitMessages.GITHUB_TOKEN_MISSING)
        return None  # Unreachable

    gh_client = GitHubClient(config, creds.github_token)
    reddit_client = RedditClient(config, creds)
    return gh_client, reddit_client
