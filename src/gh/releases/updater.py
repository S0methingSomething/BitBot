"""GitHub release updating."""

import deal
from beartype import beartype
from tenacity import retry, retry_if_result, stop_after_attempt, wait_exponential

from core.errors import GitHubAPIError
from core.result import Result
from core.tenacity_helpers import log_retry_attempt, should_retry_api_error
from gh.releases.fetcher import run_command


@deal.pre(lambda _r, tag, _t: len(tag) > 0, message="Tag cannot be empty")
@deal.pre(lambda _r, _t, title: len(title) > 0, message="Title cannot be empty")
@beartype
@retry(
    retry=retry_if_result(should_retry_api_error),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    before_sleep=log_retry_attempt,
)
def update_release_title(repo: str, tag: str, title: str) -> Result[None, GitHubAPIError]:
    """Update a release title."""
    result = run_command(["gh", "release", "edit", tag, "--repo", repo, "--title", title])
    return result.map(lambda _: None)
