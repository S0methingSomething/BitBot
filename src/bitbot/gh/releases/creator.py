"""GitHub release creation."""

from pathlib import Path

import deal
from beartype import beartype
from returns.result import Failure, Result, Success

from bitbot.core.errors import GitHubAPIError
from bitbot.gh.releases.fetcher import run_command


@deal.pre(
    lambda bot_repo, tag, title, notes, file_path: "/" in bot_repo,
    message="Repository must be in owner/name format",
)
@deal.pre(
    lambda bot_repo, tag, title, notes, file_path: len(tag) > 0,
    message="Tag cannot be empty - GitHub requires a version tag for releases",
)
@deal.pre(
    lambda bot_repo, tag, title, notes, file_path: len(title) > 0,
    message="Title cannot be empty - release must have a title",
)
@deal.pre(
    lambda bot_repo, tag, title, notes, file_path: len(file_path) > 0,
    message="File path cannot be empty - release must include an asset file",
)
@beartype
def create_bot_release(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> Result[None, GitHubAPIError]:
    """Creates a new release in the bot repository."""
    if not Path(file_path).exists():
        return Failure(GitHubAPIError(f"Asset file not found: {file_path}"))

    result = run_command(
        [
            "gh",
            "release",
            "create",
            tag,
            "--repo",
            bot_repo,
            "--title",
            title,
            "--notes",
            notes,
            file_path,
        ]
    )

    if isinstance(result, Failure):
        return Failure(GitHubAPIError(f"Failed to create release: {result.failure()}"))
    return Success(None)
