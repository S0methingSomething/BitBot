"""GitHub release creation."""

import deal
from beartype import beartype

from src.core.errors import GitHubAPIError
from src.core.result import Err, Ok, Result
from src.gh.releases.fetcher import run_command


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

    if result.is_err():
        return Err(GitHubAPIError(f"Failed to create release: {result.error}"))
    return Ok(None)
