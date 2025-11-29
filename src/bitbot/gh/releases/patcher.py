"""File patching for releases."""

from pathlib import Path

import icontract
from beartype import beartype
from returns.result import Failure, Result, Success

from bitbot import paths
from bitbot.core.errors import GitHubAPIError
from bitbot.patch_file import process_file

DOWNLOAD_DIR = paths.DIST_DIR


@icontract.require(
    lambda original_path: len(original_path) > 0,
    description="Original path cannot be empty - must specify source file to patch",
)
@icontract.require(
    lambda asset_name: len(asset_name) > 0,
    description="Asset name cannot be empty - must specify output filename",
)
@beartype
def patch_file(original_path: str, asset_name: str) -> Result[str, GitHubAPIError]:
    """Patch the downloaded file using crypto processing."""
    patched_path = Path(DOWNLOAD_DIR) / asset_name
    result = process_file(Path(original_path), patched_path)
    if isinstance(result, Failure):
        return Failure(GitHubAPIError(f"Failed to patch file: {result.failure()}"))
    return Success(str(patched_path))
