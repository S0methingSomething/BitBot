"""GitHub asset downloading."""

from pathlib import Path
from typing import Any, cast

import deal
from beartype import beartype

import paths
from core.credentials import Credentials
from core.errors import GitHubAPIError
from core.result import Err, Ok, Result
from core.retry import retry
from gh.releases.fetcher import get_github_data, run_command

DOWNLOAD_DIR = paths.DIST_DIR


@deal.pre(lambda _s, _r, asset_name: len(asset_name) > 0)  # type: ignore[misc]
@deal.pre(lambda _s, release_id, _a: release_id > 0)  # type: ignore[misc]
@beartype
@retry(max_attempts=3, on=[GitHubAPIError])
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
