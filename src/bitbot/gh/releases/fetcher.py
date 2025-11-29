"""GitHub release fetching."""

import json
import subprocess
from typing import Any

import icontract
from beartype import beartype
from returns.result import Failure, Result, Success

from bitbot.core.errors import GitHubAPIError
from bitbot.core.retry import retry_on_err


@icontract.require(
    lambda command: isinstance(command, list) and len(command) > 0,
    description="Command must be a non-empty list",
)
@beartype
def run_command(
    command: list[str], check: bool = True
) -> Result[subprocess.CompletedProcess[str], GitHubAPIError]:
    """Runs a shell command and returns its result."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=check)
        return Success(result)
    except subprocess.CalledProcessError as e:
        return Failure(GitHubAPIError(f"Command failed: {' '.join(command)}: {e.stderr}"))


@icontract.require(
    lambda url: len(url) > 0,
    description="URL cannot be empty",
)
@icontract.require(
    lambda url: url.startswith("/"),
    description="GitHub API URLs must start with / for relative paths",
)
@retry_on_err()
@beartype
def get_github_data(url: str) -> Result[dict[str, Any] | list[Any], GitHubAPIError]:
    """Fetches data from the GitHub API using the gh cli."""
    command = ["gh", "api", url]
    result = run_command(command)

    if isinstance(result, Failure):
        return Failure(GitHubAPIError(f"Command failed: {result.failure()}"))

    try:
        data: dict[str, Any] | list[Any] = json.loads(result.unwrap().stdout)
        return Success(data)
    except json.JSONDecodeError as e:
        return Failure(GitHubAPIError(f"Failed to parse GitHub API response: {e}"))


@icontract.require(
    lambda repo: "/" in repo,
    description="Repository must be in owner/name format",
)
@beartype
def get_source_releases(repo: str) -> Result[list[dict[str, Any]], GitHubAPIError]:
    """Gets the last 30 releases from the source repository."""
    result = get_github_data(f"/repos/{repo}/releases?per_page=30")

    if isinstance(result, Failure):
        return Failure(result.failure())

    data = result.unwrap()
    if not isinstance(data, list):
        return Failure(GitHubAPIError("Expected list of releases"))

    # Type narrowed by isinstance check above
    return Success(data)  # type: ignore[return-value]


@icontract.require(
    lambda bot_repo: "/" in bot_repo,
    description="Repository must be in owner/name format",
)
@icontract.require(
    lambda tag: len(tag) > 0,
    description="Tag cannot be empty - required to check release existence",
)
@beartype
def check_if_bot_release_exists(bot_repo: str, tag: str) -> Result[bool, GitHubAPIError]:
    """Checks if a release with the given tag exists in the bot repo."""
    result = run_command(["gh", "release", "view", tag, "--repo", bot_repo], check=False)

    if isinstance(result, Failure):
        return Success(False)

    return Success(result.unwrap().returncode == 0)
