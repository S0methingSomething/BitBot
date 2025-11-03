"""File patching for releases."""

from pathlib import Path

import deal
from beartype import beartype

from bitbot import paths
from bitbot.core.errors import GitHubAPIError
from bitbot.core.result import Result
from bitbot.patch_file import process_file

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
    """Patch the downloaded file using crypto processing."""
    patched_path = Path(DOWNLOAD_DIR) / asset_name
    result = process_file(Path(original_path), patched_path)
    if result.is_err():
        return result.map_err(lambda e: GitHubAPIError(f"Failed to patch file: {e}"))
    return result.map(lambda _: str(patched_path))
