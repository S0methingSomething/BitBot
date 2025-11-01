"""GitHub asset downloading."""

from pathlib import Path
from typing import Any, cast

import deal
from beartype import beartype
from tenacity import retry, retry_if_result, stop_after_attempt, wait_exponential

import paths
from core.credentials import Credentials
from core.errors import GitHubAPIError
from core.result import Err, Ok, Result
from core.tenacity_helpers import log_retry_attempt, should_retry_api_error
from gh.releases.fetcher import get_github_data, run_command

DOWNLOAD_DIR = paths.DIST_DIR


@deal.pre(lambda _s, _r, asset_name: len(asset_name) > 0)  # type: ignore[misc]
@deal.pre(lambda _s, release_id, _a: release_id > 0)  # type: ignore[misc]
@beartype
@retry(
    retry=retry_if_result(should_retry_api_error),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    before_sleep=log_retry_attempt,
)
def download_asset(
    source_repo: str, release_id: int, asset_name: str
) -> Result[Path, GitHubAPIError]:
    """Downloads a specific asset from a specific release."""
    try:
        Path(DOWNLOAD_DIR).mkdir(parents=True, exist_ok=True)

        assets_result = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
        if assets_result.is_err():
            return assets_result

        assets = cast("list[dict[str, Any]]", assets_result.unwrap())
        asset_id = next((asset["id"] for asset in assets if asset["name"] == asset_name), None)

        if not asset_id:
            return Err(GitHubAPIError(f"Asset '{asset_name}' not found in release {release_id}"))

        download_url = f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
        output_path = Path(DOWNLOAD_DIR) / f"original_{asset_name}"

        result = run_command(
            [
                "curl",
                "-sL",
                "-J",
                "-H",
                "Accept: application/octet-stream",
                "-H",
                f"Authorization: token {Credentials.get_github_token()}",
                "-o",
                str(output_path),
                download_url,
            ]
        )

        if result.is_err():
            return result

        return Ok(output_path)
    except Exception as e:
        return Err(GitHubAPIError(f"Failed to download asset: {e}"))
