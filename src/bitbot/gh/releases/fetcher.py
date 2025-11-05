"""GitHub release fetching."""

import json
import logging
import subprocess
from typing import Any

import deal
from beartype import beartype
from tenacity import retry, retry_if_result, stop_after_attempt, wait_exponential

from bitbot.core.errors import GitHubAPIError
from bitbot.core.result import Err, Ok, Result

logger = logging.getLogger(__name__)


@deal.pre(
    lambda command, check=True: isinstance(command, list) and len(command) > 0,
    message="Command must be a non-empty list",
)
@beartype
def run_command(
    command: list[str], check: bool = True
) -> Result[subprocess.CompletedProcess[str], GitHubAPIError]:
    """Runs a shell command and returns its result."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=check)
        return Ok(result)
    except subprocess.CalledProcessError as e:
        return Err(GitHubAPIError(f"Command failed: {' '.join(command)}: {e.stderr}"))


@deal.pre(
    lambda url: len(url) > 0,
    message="URL cannot be empty",
)
@deal.pre(
    lambda url: url.startswith("/"),
    message="GitHub API URLs must start with / for relative paths",
)
@retry(
    retry=retry_if_result(lambda r: r.is_err()),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    before_sleep=lambda retry_state: logger.warning(
        "Retry %d/3 for get_github_data after error (wait %.1fs)",
        retry_state.attempt_number,
        retry_state.next_action.sleep if retry_state.next_action else 0,
    ),
)
@beartype
def get_github_data(url: str) -> Result[dict[str, Any] | list[Any], GitHubAPIError]:
    """Fetches data from the GitHub API using the gh cli."""
    command = ["gh", "api", url]
    result = run_command(command)

    if result.is_err():
        return Err(GitHubAPIError(f"Command failed: {result.error}"))

    try:
        data: dict[str, Any] | list[Any] = json.loads(result.unwrap().stdout)
        return Ok(data)
    except json.JSONDecodeError as e:
        return Err(GitHubAPIError(f"Failed to parse GitHub API response: {e}"))


@deal.pre(
    lambda repo: "/" in repo,
    message="Repository must be in owner/name format",
)
@retry(
    retry=retry_if_result(lambda r: r.is_err()),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    before_sleep=lambda retry_state: logger.warning(
        "Retry %d/3 for get_source_releases after error (wait %.1fs)",
        retry_state.attempt_number,
        retry_state.next_action.sleep if retry_state.next_action else 0,
    ),
)
@beartype
def get_source_releases(repo: str) -> Result[list[dict[str, Any]], GitHubAPIError]:
    """Gets the last 30 releases from the source repository."""
    result = get_github_data(f"/repos/{repo}/releases?per_page=30")

    if result.is_err():
        return Err(result.error)

    data = result.unwrap()
    if not isinstance(data, list):
        return Err(GitHubAPIError("Expected list of releases"))

    # Type narrowed by isinstance check above
    return Ok(data)  # type: ignore[return-value]


@deal.pre(
    lambda bot_repo, tag: "/" in bot_repo,
    message="Repository must be in owner/name format",
)
@deal.pre(
    lambda bot_repo, tag: len(tag) > 0,
    message="Tag cannot be empty - required to check release existence",
)
@beartype
def check_if_bot_release_exists(bot_repo: str, tag: str) -> Result[bool, GitHubAPIError]:
    """Checks if a release with the given tag exists in the bot repo."""
    result = run_command(["gh", "release", "view", tag, "--repo", bot_repo], check=False)

    if result.is_err():
        return Ok(False)

    return Ok(result.unwrap().returncode == 0)
