"""Release management for BitBot."""

import json
import os
import subprocess
from pathlib import Path
from typing import Any, cast

import paths
from config_loader import load_config
from dry_run import (
    is_dry_run,
)
from helpers import (
    get_github_data as helper_get_github_data,
)
from helpers import (
    load_release_state,
    save_release_state,
)
from helpers import (
    run_command as helper_run_command,
)
from logging_config import get_logger

logging = get_logger(__name__)

# --- Configuration ---
DOWNLOAD_DIR = Path(paths.DIST_DIR)


# --- Helper Functions ---
def run_command(
    command: list[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Runs a shell command and returns its result."""
    result = helper_run_command(command, check=check)
    return cast(subprocess.CompletedProcess[str], result)


def get_github_data(url: str) -> Any:
    """Fetches data from the GitHub API using the gh cli."""
    return helper_get_github_data(url)


# --- Core Logic ---
def get_source_releases(repo: str) -> list[dict[str, Any]]:
    """Gets the last 30 releases from the source repository."""
    if is_dry_run():
        logging.info(f"DRY_RUN: Returning mock releases for repo: {repo}")
        # Return mock data for testing
        return [
            {
                "id": 1001,
                "tag_name": "bitlife-v4.2.0",
                "created_at": "2025-08-20T10:00:00Z",
                "body": "app: BitLife\nversion: 4.2.0\nasset_name: MonetizationVars\n",
            },
            {
                "id": 1002,
                "tag_name": "bitlife-v4.1.0",
                "created_at": "2025-08-19T10:00:00Z",
                "body": "app: BitLife\nversion: 4.1.0\nasset_name: MonetizationVars\n",
            },
        ]
    logging.info(f"Fetching latest releases from source repo: {repo}")
    return cast(
        list[dict[str, Any]], get_github_data(f"/repos/{repo}/releases?per_page=30")
    )


def _parse_line(line: str, app_id_map: dict[str, str]) -> dict[str, Any] | None:
    """Parses a single line for release information."""
    try:
        key, value = line.split(":", 1)
        key, value = key.strip().lower(), value.strip()
        if key == "app":
            return {"app_id": app_id_map.get(value.lower()), "display_name": value}
        return {key: value}
    except ValueError:
        return None


def parse_release_description(
    description: str, apps_config: list[Any]
) -> list[dict[str, Any]]:
    """Parses a release description with a structured key-value format."""
    found_releases: list[dict[str, Any]] = []
    current_release: dict[str, Any] = {}
    # For Pydantic models, we need to access attributes, not dict keys
    app_id_map = {app.display_name.lower(): app.id for app in apps_config}

    for line in description.splitlines():
        stripped_line = line.strip()
        if not stripped_line:
            if current_release:
                found_releases.append(current_release)
            current_release = {}
            continue

        if parsed_line := _parse_line(stripped_line, app_id_map):
            if "app_id" in parsed_line:
                if current_release:
                    found_releases.append(current_release)
                current_release = parsed_line
            elif current_release:
                current_release.update(parsed_line)

    if current_release:
        found_releases.append(current_release)
    return found_releases


def check_if_bot_release_exists(bot_repo: str, tag: str) -> bool:
    """Checks if a release with the given tag exists in the bot repo."""
    if is_dry_run():
        # In dry-run mode, assume the release doesn't exist to allow processing
        logging.info(f"DRY_RUN: Assuming release '{tag}' does not exist in {bot_repo}")
        return False

    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo])
        logging.info(f"Release '{tag}' already exists. Skipping.")
        return True
    except subprocess.CalledProcessError:
        return False


def download_asset(source_repo: str, release_id: int, asset_name: str) -> Path:
    """Downloads a specific asset from a specific release."""
    logging.info(f"Downloading asset '{asset_name}' from release ID {release_id}")
    DOWNLOAD_DIR.mkdir(exist_ok=True)

    assets = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
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
    output_path = DOWNLOAD_DIR / f"original_{asset_name}"

    token = os.environ.get("GITHUB_TOKEN", "")
    if not token and not is_dry_run():
        raise ValueError("GitHub token is required but not available")

    run_command(
        [
            "curl",
            "-sL",
            "-J",
            "-H",
            "Accept: application/octet-stream",
            "-H",
            f"Authorization: token {token}",
            "-o",
            str(output_path),
            download_url,
        ]
    )
    return output_path


def patch_file(original_path: Path, asset_name: str) -> Path:
    """Patches the downloaded file using the Python script."""
    patched_path = DOWNLOAD_DIR / asset_name
    logging.info(f"Patching '{original_path}' to '{patched_path}' with Python script.")
    run_command(["python", "src/patch_file.py", str(original_path), str(patched_path)])
    return patched_path


def create_bot_release(
    bot_repo: str, tag: str, title: str, notes: str, file_path: Path
) -> None:
    """Creates a new release in the bot repository."""
    if is_dry_run():
        logging.info(f"DRY_RUN: Would create release '{tag}' in {bot_repo}")
        logging.info(f"  Title: {title}")
        logging.info(f"  Notes: {notes}")
        logging.info(f"  File: {file_path}")
        return

    logging.info(f"Creating new release '{tag}' in {bot_repo}")
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
            str(file_path),
        ]
    )


def process_app(
    app: dict[str, Any],
    bot_repo: str,
    source_repo: str,
    release_id: int,
    release_tag: str,
) -> dict[str, Any] | None:
    """Processes a single app from a release description."""
    if not all(app.get(k) for k in ["app_id", "version", "asset_name", "display_name"]):
        logging.warning(f"Skipping incomplete app info: {app}")
        return None

    tag = f"{app['app_id']}-v{app['version']}"
    if check_if_bot_release_exists(bot_repo, tag):
        return None

    try:
        original_file = download_asset(source_repo, release_id, app["asset_name"])
        patched_file = patch_file(original_file, app["asset_name"])
        title = f"{app['display_name']} {app['asset_name']} v{app['version']}"
        notes = f"app: {app['app_id']}\nversion: {app['version']}\nasset_name: {app['asset_name']}\n---\nAuto-patched from source release {release_tag}."
        create_bot_release(bot_repo, tag, title, notes, patched_file)

        return {
            "display_name": app["display_name"],
            "version": app["version"],
            "url": f"https://github.com/{bot_repo}/releases/download/{tag}/{app['asset_name']}",
        }
    except Exception as e:
        logging.error(
            f"Failed to process app {app['display_name']} from release {release_tag}. Reason: {e}"
        )
        return None


def process_release(
    release: dict[str, Any], config: Any, processed_ids: list[int]
) -> dict[str, Any]:
    """Processes a single source release and all the apps within it."""
    logging.info(
        f"--- Processing source release: {release['tag_name']} ({release['id']}) ---"
    )
    processed_data: dict[str, Any] = {}
    if not (description := release.get("body", "")):
        logging.warning("Release has no description. Skipping.")
        return processed_data

    apps_in_release = parse_release_description(description, config.apps)
    if not apps_in_release:
        logging.warning("No recognized app updates found in description.")
        return processed_data

    processed_count = 0
    for app in apps_in_release:
        if result := process_app(
            app,
            config.github.bot_repo,
            config.github.source_repo,
            release["id"],
            release["tag_name"],
        ):
            processed_data[app["app_id"]] = result
            processed_count += 1

    if processed_count > 0:
        processed_ids.append(release["id"])
        save_release_state(processed_ids)
        logging.info(
            f"Successfully processed {processed_count} app(s) from source release {release['tag_name']}. State updated."
        )
    return processed_data


def main() -> None:
    config = load_config()
    processed_ids = load_release_state()
    new_releases = [
        r
        for r in get_source_releases(config.github.source_repo)
        if r["id"] not in processed_ids
    ]

    if not new_releases:
        logging.info("No new source releases found to process.")
        if github_output := os.environ.get("GITHUB_OUTPUT"):
            with Path(github_output).open("a") as f:
                f.write("new_releases_found=false\n")
        return

    logging.info(f"Found {len(new_releases)} new source release(s) to process.")
    new_releases.sort(key=lambda r: r["created_at"])
    all_processed_data: dict[str, Any] = {}

    for release in new_releases:
        all_processed_data.update(process_release(release, config, processed_ids))

    if all_processed_data:
        logging.info("New releases were created. Saving data for downstream jobs.")
        DOWNLOAD_DIR.mkdir(exist_ok=True)
        (DOWNLOAD_DIR / "releases.json").write_text(
            json.dumps(all_processed_data, indent=2)
        )

    if github_output := os.environ.get("GITHUB_OUTPUT"):
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\n")


if __name__ == "__main__":
    main()
