"""GitHub release fetching."""

import json
import subprocess
from typing import Any, cast

import deal
from beartype import beartype
from tenacity import retry, retry_if_result, stop_after_attempt, wait_exponential

from core.errors import GitHubAPIError
from core.result import Err, Ok, Result
from core.tenacity_helpers import log_retry_attempt, should_retry_api_error


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
@beartype
@retry(
    retry=retry_if_result(should_retry_api_error),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    before_sleep=log_retry_attempt,
)
def get_github_data(url: str) -> Result[dict[str, Any] | list[Any], GitHubAPIError]:
    """Fetches data from the GitHub API using the gh cli."""
    command = ["gh", "api", url]
    result = run_command(command)

    if result.is_err():
        return result

    try:
        data = json.loads(result.unwrap().stdout)
        return Ok(cast("dict[str, Any] | list[Any]", data))
    except json.JSONDecodeError as e:
        return Err(GitHubAPIError(f"Failed to parse GitHub API response: {e}"))


@deal.pre(
    lambda repo: "/" in repo,
    message="Repository must be in owner/name format",
)
@beartype
@retry(
    retry=retry_if_result(should_retry_api_error),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    before_sleep=log_retry_attempt,
)
def get_source_releases(repo: str) -> Result[list[dict[str, Any]], GitHubAPIError]:
    """Gets the last 30 releases from the source repository."""
    result = get_github_data(f"/repos/{repo}/releases?per_page=30")

    if result.is_err():
        return result

    data = result.unwrap()
    if not isinstance(data, list):
        return Err(GitHubAPIError("Expected list of releases"))

    return Ok(cast("list[dict[str, Any]]", data))


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
