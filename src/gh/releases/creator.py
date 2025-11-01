"""GitHub release creation."""

import deal
from beartype import beartype
from tenacity import retry, retry_if_result, stop_after_attempt, wait_exponential

from core.errors import GitHubAPIError
from core.result import Result
from core.tenacity_helpers import log_retry_attempt, should_retry_api_error
from gh.releases.fetcher import run_command


@deal.pre(lambda bot_repo, tag, title, notes, file_path: len(tag) > 0)  # type: ignore[misc]
@deal.pre(lambda bot_repo, tag, title, notes, file_path: len(file_path) > 0)  # type: ignore[misc]
@beartype  # type: ignore[misc]
@retry(
    retry=retry_if_result(should_retry_api_error),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    before_sleep=log_retry_attempt,
)
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

    return result.map(lambda _: None)
