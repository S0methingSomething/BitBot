"""GitHub asset downloading."""

from pathlib import Path
from typing import Any, cast

import deal

import paths
from core.credentials import Credentials
from gh.releases.fetcher import get_github_data, run_command

DOWNLOAD_DIR = paths.DIST_DIR


@deal.pre(lambda _s, _r, asset_name: len(asset_name) > 0)  # type: ignore[misc]
@deal.pre(lambda _s, release_id, _a: release_id > 0)  # type: ignore[misc]
@deal.post(lambda result: len(result) > 0)  # type: ignore[misc]
def download_asset(source_repo: str, release_id: int, asset_name: str) -> str:
    """Downloads a specific asset from a specific release."""
    Path(DOWNLOAD_DIR).mkdir(parents=True, exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    assets = cast("list[dict[str, Any]]", assets_data)
    asset_id = next((asset["id"] for asset in assets if asset["name"] == asset_name), None)

    if not asset_id:
        msg = f"Asset '{asset_name}' not found in release {release_id}"
        raise FileNotFoundError(msg)

    download_url = f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    output_path = Path(DOWNLOAD_DIR) / f"original_{asset_name}"

    run_command(
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
    return str(output_path)
