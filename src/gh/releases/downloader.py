"""GitHub asset downloading."""

from pathlib import Path
from typing import Any, cast

import deal
from beartype import beartype

import paths
from core.credentials import Credentials
from core.errors import GitHubAPIError
from core.result import Err, Ok, Result
from gh.releases.fetcher import get_github_data, run_command

DOWNLOAD_DIR = paths.DIST_DIR


@deal.pre(
    lambda source_repo, release_id, asset_name: "/" in source_repo,
    message="Repository must be in owner/name format",
)
@deal.pre(
    lambda source_repo, release_id, asset_name: release_id > 0,
    message="Release ID must be positive - invalid release ID provided",
)
@deal.pre(
    lambda source_repo, release_id, asset_name: len(asset_name) > 0,
    message="Asset name cannot be empty - must specify which file to download",
)
@beartype
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
