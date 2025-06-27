import json
import logging
import os
import re
import sys
from typing import Any

import praw
import requests
from praw.models import Submission
from tenacity import RetryError, retry, stop_after_attempt, wait_exponential

from .config import BotState, Config


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
        self.state_issue_url = (
            f"{self.api_base}/repos/{self.config.bot_repo}/issues/"
            f"{config.reddit.state_issue_number}"
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
    def _request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        """Makes a request with unified headers, timeout, and retry logic."""
        response = requests.request(
            method, url, headers=self.headers, timeout=30, **kwargs
        )
        response.raise_for_status()
        return response

    def get_latest_release(self, repo_slug: str) -> dict[str, Any] | None:
        """Fetches the latest release from a given repository."""
        url = f"{self.api_base}/repos/{repo_slug}/releases/latest"
        try:
            return self._request("GET", url).json()
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

    def download_asset(self, url: str) -> bytes:
        """Downloads a release asset."""
        try:
            # Asset downloads need a different Accept header
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
        return self._request("POST", url, json=payload).json()

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
        releases = self._request("GET", url).json()
        if not releases or len(releases) < 2:
            logging.info("Not enough releases to mark any as outdated.")
            return

        for release in releases[1:]:  # Skip the latest one at index 0
            if not release["name"].startswith("[OUTDATED] "):
                logging.info(f"Marking release '{release['name']}' as outdated.")
                update_url = release["url"]
                payload = {"name": f"[OUTDATED] {release['name']}"}
                self._request("PATCH", update_url, json=payload)

    def load_state(self) -> BotState | None:
        """Loads the bot's state from the dedicated GitHub issue."""
        try:
            issue_data = self._request("GET", self.state_issue_url).json()
            issue_body = issue_data.get("body", "")

            # Find the JSON code block
            match = re.search(r"```json\s*(\{.*?\})\s*```", issue_body, re.DOTALL)
            if not match:
                logging.error(
                    "Could not find a JSON code block in state issue %s",
                    self.state_issue_url,
                )
                return None

            state_json = json.loads(match.group(1))
            return BotState.model_validate(state_json)
        except Exception as e:
            logging.error(
                f"Failed to load or parse state from GitHub issue: {e}", exc_info=True
            )
            return None

    def save_state(self, state: BotState) -> None:
        """Saves the bot's state to the dedicated GitHub issue."""
        try:
            # Fetch the current issue body to preserve other content
            issue_data = self._request("GET", self.state_issue_url).json()
            issue_body = issue_data.get("body", "")

            # Create the new state block
            state_json_str = state.model_dump_json(by_alias=True, indent=2)
            new_state_block = f"```json\n{state_json_str}\n```"

            # Replace the old state block or append if not found
            json_block_pattern = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)
            if json_block_pattern.search(issue_body):
                new_body = json_block_pattern.sub(new_state_block, issue_body)
            else:
                new_body = f"{issue_body}\n\n{new_state_block}"

            self._request("PATCH", self.state_issue_url, json={"body": new_body})
            logging.info(
                "Successfully saved state to issue %s#%s",
                self.config.bot_repo,
                self.state_issue_url.split("/")[-1],
            )
        except Exception as e:
            logging.error(f"Failed to save state to GitHub issue: {e}", exc_info=True)


class RedditClient:
    """A client for all PRAW/Reddit interactions."""

    def __init__(self, config: Config):
        # Validate that all required environment variables are set
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
        """Gets the bot's recent submissions that match the release post format."""
        post_identifier = (
            self.post_title_template.split("{{version}}")[0]
            .replace("{{asset_name}}", self.asset_name)
            .strip()
        )
        bot_posts = []
        for submission in self.reddit.user.me().submissions.new(limit=limit):
            if (
                submission.subreddit.display_name.lower()
                == self.subreddit.display_name.lower()
                and submission.title.startswith(post_identifier)
            ):
                bot_posts.append(submission)
        return bot_posts

    def submit_post(self, title: str, selftext: str) -> Submission:
        """Submits a new post to the configured subreddit."""
        return self.subreddit.submit(title, selftext=selftext)
