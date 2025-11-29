"""GitHub release updating."""

import icontract
from beartype import beartype
from returns.result import Failure, Result, Success

from bitbot.core.errors import GitHubAPIError
from bitbot.gh.releases.fetcher import run_command


@icontract.require(
    lambda repo: "/" in repo,
    description="Repository must be in owner/name format",
)
@icontract.require(
    lambda tag: len(tag) > 0,
    description="Tag cannot be empty - GitHub API requires a version tag",
)
@icontract.require(
    lambda title: len(title) > 0,
    description="Title cannot be empty - release must have a title",
)
@beartype
def update_release_title(repo: str, tag: str, title: str) -> Result[None, GitHubAPIError]:
    """Update a release title."""
    result = run_command(["gh", "release", "edit", tag, "--repo", repo, "--title", title])
    if isinstance(result, Failure):
        return Failure(GitHubAPIError(f"Failed to update release title: {result.failure()}"))
    return Success(None)
