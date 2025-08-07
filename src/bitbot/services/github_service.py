"""Service for interacting with the GitHub API."""

import json
import subprocess
from typing import cast

from ..models.config import GitHubConfig


class GitHubService:
    """Service for interacting with the GitHub API."""

    def __init__(self, config: GitHubConfig):
        """Initialize the GitHubService.

        Args:
            config: The GitHub configuration.

        """
        self._config = config
        token = self._config.token
        if not token:
            raise ValueError("GITHUB_TOKEN is not set in the configuration.")
        self._token = token

    def _run_gh_command(self, command: list[str]) -> dict | list:
        """Run a 'gh api' command and returns the JSON output."""
        full_command = ["gh", "api"] + command
        result = subprocess.run(
            full_command,
            capture_output=True,
            text=True,
            check=False,
            env={"GITHUB_TOKEN": self._token},
        )
        if result.returncode != 0:
            raise Exception(f"GitHub API command failed: {result.stderr}")
        return cast(dict | list, json.loads(result.stdout))

    def get_source_releases(self) -> list[dict]:
        """Get the last 30 releases from the source repository."""
        return cast(
            list[dict],
            self._run_gh_command([f"/repos/{self._config.source_repo}/releases?per_page=30"]),
        )

    def check_release_exists(self, tag: str) -> bool:
        """Check if a release with a given tag exists in the bot repo."""
        try:
            subprocess.run(
                ["gh", "release", "view", tag, "--repo", self._config.bot_repo],
                capture_output=True,
                text=True,
                check=True,
                env={"GITHUB_TOKEN": self._token},
            )
            return True
        except subprocess.CalledProcessError:
            return False
