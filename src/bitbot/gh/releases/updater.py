"""GitHub release updating."""

import deal
from beartype import beartype

from bitbot.core.errors import GitHubAPIError
from bitbot.core.result import Err, Ok, Result
from bitbot.gh.releases.fetcher import run_command


@deal.pre(
    lambda repo, tag, title: "/" in repo,
    message="Repository must be in owner/name format",
)
@deal.pre(
    lambda repo, tag, title: len(tag) > 0,
    message="Tag cannot be empty - GitHub API requires a version tag",
)
@deal.pre(
    lambda repo, tag, title: len(title) > 0,
    message="Title cannot be empty - release must have a title",
)
@beartype
def update_release_title(repo: str, tag: str, title: str) -> Result[None, GitHubAPIError]:
    """Update a release title."""
    result = run_command(["gh", "release", "edit", tag, "--repo", repo, "--title", title])
    if result.is_err():
        return Err(GitHubAPIError(f"Failed to update release title: {result.error}"))
    return Ok(None)
