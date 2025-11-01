"""GitHub release fetching."""

import json
import subprocess
from typing import Any, cast

import deal
from beartype import beartype

from core.errors import GitHubAPIError
from core.result import Err, Ok, Result
from core.retry import retry


@deal.pre(lambda command, check: isinstance(command, list) and len(command) > 0)  # type: ignore[misc]
@beartype  # type: ignore[misc]
def run_command(command: list[str], check: bool = True) -> Result[subprocess.CompletedProcess[str], GitHubAPIError]:  # noqa: FBT001, FBT002
    """Runs a shell command and returns its result."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=check)  # noqa: S603
        return Ok(result)
    except subprocess.CalledProcessError as e:
        return Err(GitHubAPIError(f"Command failed: {' '.join(command)}: {e.stderr}"))


@deal.pre(lambda url: url.startswith("/"))  # type: ignore[misc]
@beartype
@retry(max_attempts=3, on=[GitHubAPIError])
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


@deal.pre(lambda repo: "/" in repo)  # type: ignore[misc]
@beartype  # type: ignore[misc]
@retry(max_attempts=3, on=[GitHubAPIError])
def get_source_releases(repo: str) -> Result[list[dict[str, Any]], GitHubAPIError]:
    """Gets the last 30 releases from the source repository."""
    result = get_github_data(f"/repos/{repo}/releases?per_page=30")
    
    if result.is_err():
        return result
    
    data = result.unwrap()
    if not isinstance(data, list):
        return Err(GitHubAPIError("Expected list of releases"))
    
    return Ok(cast("list[dict[str, Any]]", data))


@deal.pre(lambda bot_repo, tag: "/" in bot_repo)  # type: ignore[misc]
@deal.pre(lambda bot_repo, tag: len(tag) > 0)  # type: ignore[misc]
@beartype  # type: ignore[misc]
def check_if_bot_release_exists(bot_repo: str, tag: str) -> Result[bool, GitHubAPIError]:
    """Checks if a release with the given tag exists in the bot repo."""
    result = run_command(["gh", "release", "view", tag, "--repo", bot_repo], check=False)
    
    if result.is_err():
        return Ok(False)
    
    return Ok(result.unwrap().returncode == 0)
