"""GitHub release fetching."""

import json
import subprocess
from typing import Any, cast

import deal
from beartype import beartype


@deal.pre(lambda command, check: isinstance(command, list) and len(command) > 0)  # type: ignore[misc]
@beartype  # type: ignore[misc]
def run_command(command: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:  # noqa: FBT001, FBT002
    """Runs a shell command and returns its result."""
    return subprocess.run(command, capture_output=True, text=True, check=check)  # noqa: S603


@deal.pre(lambda url: url.startswith("/"))  # type: ignore[misc]
@deal.post(lambda result: result is not None)  # type: ignore[misc]
def get_github_data(url: str) -> dict[str, Any] | list[Any]:
    """Fetches data from the GitHub API using the gh cli."""
    command = ["gh", "api", url]
    result = run_command(command)
    return cast("dict[str, Any] | list[Any]", json.loads(result.stdout))


@deal.pre(lambda repo: "/" in repo)  # type: ignore[misc]
@deal.post(lambda result: isinstance(result, list))  # type: ignore[misc]
@beartype  # type: ignore[misc]
def get_source_releases(repo: str) -> list[dict[str, Any]]:
    """Gets the last 30 releases from the source repository."""
    data = get_github_data(f"/repos/{repo}/releases?per_page=30")
    return cast("list[dict[str, Any]]", data)


@deal.pre(lambda bot_repo, tag: "/" in bot_repo)  # type: ignore[misc]
@deal.pre(lambda bot_repo, tag: len(tag) > 0)  # type: ignore[misc]
@beartype  # type: ignore[misc]
def check_if_bot_release_exists(bot_repo: str, tag: str) -> bool:
    """Checks if a release with the given tag exists in the bot repo."""
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
    except subprocess.CalledProcessError:
        return False
    else:
        return True
