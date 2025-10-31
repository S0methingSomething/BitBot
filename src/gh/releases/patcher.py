"""File patching for releases."""

from pathlib import Path

import deal

import paths
from gh.releases.fetcher import run_command

DOWNLOAD_DIR = paths.DIST_DIR


@deal.pre(lambda original_path, _a: len(original_path) > 0)  # type: ignore[misc]
@deal.pre(lambda _o, asset_name: len(asset_name) > 0)  # type: ignore[misc]
@deal.post(lambda result: len(result) > 0)  # type: ignore[misc]
def patch_file(original_path: str, asset_name: str) -> str:
    """Patches the downloaded file using the Python script."""
    patched_path = Path(DOWNLOAD_DIR) / asset_name
    run_command(["python", "patch_file.py", original_path, str(patched_path)])
    return str(patched_path)
