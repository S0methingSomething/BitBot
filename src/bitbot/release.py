"""This module handles the creation of GitHub releases."""

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from . import crypto
from .logging import get_logger

logger = get_logger(__name__)

# --- Configuration ---
CONFIG_FILE = "config.json"
DOWNLOAD_DIR = "./dist"


# --- Helper Functions ---


def run_command(
    command: List[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a shell command and return its result.

    Args:
        command: The command to run.
        check: Whether to check the return code of the command.

    Returns:
        The result of the command.
    """
    logger.info("Executing: %s", " ".join(command))
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=check,
    )


def load_config() -> Dict[str, Any]:
    """Load the configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path(CONFIG_FILE)
    with config_path.open("r") as f:
        return cast(Dict[str, Any], json.load(f))


def get_github_data(url: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Fetch data from the GitHub API using the gh cli.

    Args:
        url: The API endpoint to fetch data from.

    Returns:
        The JSON response from the API.
    """
    command = ["gh", "api", url]
    result = run_command(command)
    return cast(Union[Dict[str, Any], List[Dict[str, Any]]], json.loads(result.stdout))


# --- Core Logic ---


def get_source_releases(repo: str) -> List[Dict[str, Any]]:
    """Get the last 30 releases from the source repository.

    Args:
        repo: The repository to fetch releases from.

    Returns:
        A list of releases.
    """
    logger.info("Fetching latest releases from source repo: %s", repo)
    data = get_github_data(f"/repos/{repo}/releases?per_page=30")
    if isinstance(data, list):
        return data
    return []


def parse_release_description(
    description: str, apps_config: List[Dict[str, Any]]
) -> Optional[Tuple[str, str]]:
    """Parse a release description to find the app name and version.

    Example: "MonetizationVars for BitLife v3.19.4"

    Args:
        description: The release description.
        apps_config: The configuration for the apps.

    Returns:
        A tuple containing the app ID and version, or None if not found.
    """
    for app in apps_config:
        display_name = app["displayName"]
        # Regex to find "for <AppName> v<version>"
        match = re.search(
            f"for {re.escape(display_name)} v([\\d\\.]+)", description, re.IGNORECASE
        )
        if match:
            version = match.group(1)
            logger.info(
                "Found app '%s' with version '%s' in description.",
                display_name,
                version,
            )
            return (app["id"], version)
    return None


def check_if_bot_release_exists(bot_repo: str, tag: str) -> bool:
    """Check if a release with the given tag exists in the bot repo.

    Args:
        bot_repo: The repository to check.
        tag: The tag to check for.

    Returns:
        True if the release exists, False otherwise.
    """
    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logger.info("Release '%s' already exists in %s. Skipping.", tag, bot_repo)
        return True
    except subprocess.CalledProcessError:
        logger.info("Release '%s' does not exist in %s. Proceeding.", tag, bot_repo)
        return False


def download_asset(source_repo: str, release_id: int, asset_name: str) -> str:
    """Download a specific asset from a specific release.

    Args:
        source_repo: The repository to download the asset from.
        release_id: The ID of the release to download the asset from.
        asset_name: The name of the asset to download.

    Returns:
        The path to the downloaded asset.
    """
    logger.info("Downloading asset '%s' from release ID %s", asset_name, release_id)
    download_dir = Path(DOWNLOAD_DIR)
    download_dir.mkdir(exist_ok=True)

    assets_data = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    if isinstance(assets_data, list):
        assets: List[Dict[str, Any]] = assets_data
    else:
        assets = []
    asset_id = next(
        (asset["id"] for asset in assets if asset["name"] == asset_name), None
    )

    if not asset_id:
        raise FileNotFoundError(
            f"Asset '{asset_name}' not found in release {release_id}"
        )

    download_url = (
        f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    )
    output_path = download_dir / f"original_{asset_name}"

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return str(output_path)


def patch_file(original_path: str, asset_name: str) -> str:
    """Patch the downloaded file using the crypto module.

    Args:
        original_path: The path to the original file.
        asset_name: The name of the asset.

    Returns:
        The path to the patched file.
    """
    download_dir = Path(DOWNLOAD_DIR)
    patched_path = download_dir / asset_name
    logger.info("Patching '%s' to '%s'", original_path, patched_path)
    crypto.patch_file(original_path, str(patched_path))
    return str(patched_path)


def create_bot_release(
    bot_repo: str, tag: str, title: str, notes: str, file_path: str
) -> None:
    """Create a new release in the bot repository.

    Args:
        bot_repo: The repository to create the release in.
        tag: The tag for the release.
        title: The title of the release.
        notes: The release notes.
        file_path: The path to the file to attach to the release.
    """
    logger.info("Creating new release '%s' in %s", tag, bot_repo)
    run_command(
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


# --- Main Execution ---


def main() -> None:
    """The main function for the release module."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    asset_name = config["github"]["assetFileName"]
    apps_config = config["apps"]

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit: Dict[str, str] = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get("body", "")
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app["id"] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release["id"], asset_name)

                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = (
                    f"Auto-patched {asset_name} for {app_config['displayName']} "
                    f"from source release {release['tag_name']}."
                )
                create_bot_release(
                    bot_repo,
                    bot_release_tag,
                    release_title,
                    release_notes,
                    patched_file,
                )

                # 4. Store info for Reddit post
                download_url = (
                    f"https://github.com/{bot_repo}/releases/download/"
                    f"{bot_release_tag}/{asset_name}"
                )
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == "bitlife":
                    primary_version_for_title = version

            except Exception:
                logger.error(
                    "Failed to process release %s for app %s.",
                    release["tag_name"],
                    app_id,
                    exc_info=True,
                )

    # If no primary version was found but other apps were updated, use the
    # latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        primary_version_for_title = version
        logger.warning(
            "BitLife version not found. Using fallback version '%s' for Reddit title.",
            version,
        )

    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        logger.info("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")
            f.write(f"version={primary_version_for_title}\n")
            f.write(f"urls={urls_json}\n")
    else:
        logger.info("No new releases to post to Reddit.")
        github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=false\n")


if __name__ == "__main__":
    main()
