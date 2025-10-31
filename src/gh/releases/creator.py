"""GitHub release creation."""

import deal
from beartype import beartype

from gh.releases.fetcher import run_command


@deal.pre(lambda bot_repo, tag, title, notes, file_path: len(tag) > 0)  # type: ignore[misc]
@deal.pre(lambda bot_repo, tag, title, notes, file_path: len(file_path) > 0)  # type: ignore[misc]
@beartype  # type: ignore[misc]
def create_bot_release(bot_repo: str, tag: str, title: str, notes: str, file_path: str) -> None:
    """Creates a new release in the bot repository."""
    run_command(
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
