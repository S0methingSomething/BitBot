"""File patching for releases."""

from pathlib import Path

import deal
from beartype import beartype

import paths
from core.errors import GitHubAPIError
from core.result import Result
from gh.releases.fetcher import run_command

DOWNLOAD_DIR = paths.DIST_DIR


@deal.pre(
    lambda original_path, asset_name: len(original_path) > 0,
    message="Original path cannot be empty - must specify source file to patch",
)
@deal.pre(
    lambda original_path, asset_name: len(asset_name) > 0,
    message="Asset name cannot be empty - must specify output filename",
)
@beartype
def patch_file(original_path: str, asset_name: str) -> Result[str, GitHubAPIError]:
    """Patches the downloaded file using the Python script."""
    patched_path = Path(DOWNLOAD_DIR) / asset_name
    result = run_command(["python", "patch_file.py", original_path, str(patched_path)])
    return result.map(lambda _: str(patched_path))
