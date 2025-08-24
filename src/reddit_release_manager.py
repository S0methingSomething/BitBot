"""Release management for BitBot using Reddit posts as the source of truth."""

import json
import os
import subprocess
from pathlib import Path
from typing import Any, cast

import paths
from config_loader import load_config
from credentials import setup_credentials
from digest_aggregator import add_release_to_digest
from dry_run import is_dry_run
from helpers import get_github_data as helper_get_github_data
from helpers import run_command as helper_run_command
from logging_config import get_logger
from reddit_parser import extract_app_versions_from_posts

logging = get_logger(__name__)

# --- Configuration ---
DOWNLOAD_DIR = Path(paths.DIST_DIR)


def run_command(
    command: list[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Runs a shell command and returns its result."""
    result = helper_run_command(command, check=check)
    return cast(subprocess.CompletedProcess[str], result)


def get_github_data(url: str) -> Any:
    """Fetches data from the GitHub API using the gh cli."""
    return helper_get_github_data(url)


# Auto-setup credentials
try:
    config = load_config()
    auto_save = getattr(config.auth, "auto_save", False)
    auto_load = getattr(config.auth, "auto_load", False)
    setup_credentials(auto_save=auto_save, auto_load=auto_load)
except Exception:
    logging.warning("Failed to auto-setup credentials")


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
                "body": "app: BitLife\\nversion: 4.2.0\\nasset_name: MonetizationVars\\n",
            },
            {
                "id": 1002,
                "tag_name": "bitlife-v4.1.0",
                "created_at": "2025-08-19T10:00:00Z",
                "body": "app: BitLife\\nversion: 4.1.0\\nasset_name: MonetizationVars\\n",
            },
        ]
    logging.info(f"Fetching latest releases from source repo: {repo}")
    return cast(
        list[dict[str, Any]], get_github_data(f"/repos/{repo}/releases?per_page=30")
    )


def get_current_versions_from_reddit() -> dict[str, str]:
    """Get current app versions from Reddit posts."""
    try:
        versions: dict[str, str] = extract_app_versions_from_posts()
        logging.info(f"Found {len(versions)} app versions from Reddit posts")
        return versions
    except Exception as e:
        logging.error(f"Failed to extract versions from Reddit posts: {e}")
        return {}


def _parse_line(line: str, app_id_map: dict[str, str]) -> dict[str, str] | None:
    """Parses a single line for release information."""
    try:
        key, value = line.split(":", 1)
        key, value = key.strip().lower(), value.strip()
        if key == "app":
            app_id = app_id_map.get(value.lower())
            if app_id:
                return {"app_id": app_id, "display_name": value}
            return None
        return {key: value}
    except ValueError:
        return None


def _process_release_line(
    line: str,
    current_release: dict[str, Any],
    found_releases: list[dict[str, Any]],
    app_id_map: dict[str, str],
) -> dict[str, Any]:
    """Process a single line and update releases."""
    stripped_line = line.strip()
    if not stripped_line:
        if current_release:
            found_releases.append(current_release)
        return {}

    if parsed_line := _parse_line(stripped_line, app_id_map):
        if "app_id" in parsed_line:
            if current_release:
                found_releases.append(current_release)
            return parsed_line
        if current_release:
            current_release.update(parsed_line)

    return current_release


def parse_release_description(
    description: str, apps_config: list[Any]
) -> list[dict[str, Any]]:
    """Parses a release description with a structured key-value format."""
    found_releases: list[dict[str, Any]] = []
    current_release: dict[str, Any] = {}
    # For Pydantic models, we need to access attributes, not dict keys
    app_id_map = {app.display_name.lower(): app.id for app in apps_config}

    for line in description.splitlines():
        current_release = _process_release_line(
            line, current_release, found_releases, app_id_map
        )

    if current_release:
        found_releases.append(current_release)
    return found_releases


def check_if_bot_release_exists(bot_repo: str, tag: str) -> bool:
    """Check if a release already exists in the bot repository."""
    if is_dry_run():
        logging.info(f"DRY_RUN: Checking if release '{tag}' exists in {bot_repo}")
        # For testing, let's pretend some releases exist and others don't
        return tag.endswith("v4.2.0")  # Pretend v4.2.0 already exists

    try:
        run_command(["gh", "release", "view", tag, "--repo", bot_repo], check=True)
        logging.info(f"Release '{tag}' already exists in {bot_repo}")
        return True
    except subprocess.CalledProcessError:
        logging.info(f"Release '{tag}' does not exist in {bot_repo}")
        return False


def download_asset(source_repo: str, release_id: int, asset_name: str) -> Path:
    """Downloads an asset from a source release."""
    if is_dry_run():
        logging.info(
            f"DRY_RUN: Would download asset '{asset_name}' from release {release_id}"
        )
        # Return a mock file path
        mock_path = DOWNLOAD_DIR / f"mock-{asset_name}"
        mock_path.parent.mkdir(exist_ok=True)
        mock_path.write_text("mock asset content")
        return mock_path

    logging.info(f"Downloading asset '{asset_name}' from release {release_id}")
    asset_path = DOWNLOAD_DIR / asset_name
    run_command(
        [
            "gh",
            "release",
            "download",
            str(release_id),
            "--pattern",
            asset_name,
            "--repo",
            source_repo,
            "--dir",
            str(DOWNLOAD_DIR),
        ]
    )
    return asset_path


def patch_file(original_path: Path, asset_name: str) -> Path:
    """Patches a file by setting all boolean values to true."""
    if is_dry_run():
        logging.info(f"DRY_RUN: Would patch file {original_path}")
        # Return the same path for dry-run
        return original_path

    patched_path = original_path.with_name(f"patched-{asset_name}")
    logging.info(f"Patching {original_path} -> {patched_path}")
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


def process_release(release: dict[str, Any], config: Any) -> dict[str, Any]:
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

    logging.info(
        f"Successfully processed {processed_count} app(s) from source release {release['tag_name']}."
    )
    return processed_data


def identify_new_releases(current_versions: dict[str, str]) -> list[dict[str, Any]]:
    """
    Identify which apps need new releases based on current versions.
    This function checks the source repository for new releases and compares
    them with the versions currently posted on Reddit.
    """
    config = load_config()
    source_releases = get_source_releases(config.github.source_repo)

    # Create a mapping of app names to their current versions from Reddit
    reddit_versions = current_versions

    # For each source release, check if we need to process it
    new_releases = []
    for release in source_releases:
        if not (description := release.get("body", "")):
            continue

        apps_in_release = parse_release_description(description, config.apps)
        for app in apps_in_release:
            if not all(app.get(k) for k in ["app_id", "version", "display_name"]):
                continue

            app_id = app["app_id"]
            app_version = app["version"]

            # Check if this app version is already posted on Reddit
            if app_id in reddit_versions:
                current_version = reddit_versions[app_id]
                # Compare versions (simplified comparison)
                if app_version != current_version:
                    # New version available
                    new_releases.append(
                        {
                            "app_id": app_id,
                            "display_name": app["display_name"],
                            "current_version": current_version,
                            "new_version": app_version,
                            "release": release,
                        }
                    )
            else:
                # App not found on Reddit, so it's new
                new_releases.append(
                    {
                        "app_id": app_id,
                        "display_name": app["display_name"],
                        "current_version": None,
                        "new_version": app_version,
                        "release": release,
                    }
                )

    logging.info(f"Identified {len(new_releases)} apps with new releases available")
    return new_releases


def process_new_releases(
    new_releases: list[dict[str, Any]], config: Any
) -> dict[str, Any]:
    """
    Process new releases that need to be created.
    This function processes the source releases to create new bot releases.
    """
    all_processed_data: dict[str, Any] = {}

    # Group releases by source release to avoid processing the same release multiple times
    release_groups = {}
    for item in new_releases:
        release_id = item["release"]["id"]
        if release_id not in release_groups:
            release_groups[release_id] = item["release"]

    # Process each unique source release
    for release in release_groups.values():
        processed_data = process_release(release, config)
        all_processed_data.update(processed_data)

    logging.info(f"Processed {len(all_processed_data)} new releases")
    return all_processed_data


def _collect_apps_from_releases(
    source_releases: list[dict[str, Any]], config: Any
) -> dict[str, Any]:
    """Collect all apps from source releases."""
    all_apps_data: dict[str, Any] = {}  # app_id -> app_data

    for release in source_releases:
        if description := release.get("body", ""):
            apps_in_release = parse_release_description(description, config.apps)
            for app in apps_in_release:
                if all(
                    app.get(k)
                    for k in ["app_id", "version", "display_name", "asset_name"]
                ):
                    app_id = app["app_id"]
                    # Store the app data (we'll use the first occurrence for simplicity)
                    if app_id not in all_apps_data:
                        all_apps_data[app_id] = {
                            "display_name": app["display_name"],
                            "version": app["version"],
                            "asset_name": app["asset_name"],
                            "release_id": release["id"],
                            "created_at": release.get(
                                "created_at", "2025-01-01T00:00:00Z"
                            ),
                        }
    return all_apps_data


def _create_release_data_for_apps(
    all_apps_data: dict[str, Any], config: Any
) -> dict[str, Any]:
    """Create release data for all apps."""
    processed_data: dict[str, Any] = {}
    for app_id, app_info in all_apps_data.items():
        processed_data[app_id] = {
            "display_name": app_info["display_name"],
            "version": app_info["version"],
            "latest_release": {
                "version": app_info["version"],
                "download_url": f"https://github.com/{config.github.bot_repo}/releases/download/{app_id}-v{app_info['version']}/{app_info['asset_name']}",
                "published_at": app_info["created_at"],
            },
        }
    return processed_data


def _save_fresh_start_data(processed_data: dict[str, Any]) -> None:
    """Save fresh start data to files."""
    logging.info(f"Created initial release data for {len(processed_data)} apps")
    DOWNLOAD_DIR.mkdir(exist_ok=True)
    (DOWNLOAD_DIR / "releases.json").write_text(json.dumps(processed_data, indent=2))

    # Also write a flag indicating this is a fresh start
    (DOWNLOAD_DIR / "fresh_start.flag").write_text("true")

    if github_output := os.environ.get("GITHUB_OUTPUT"):
        with Path(github_output).open("a") as f:
            f.write("new_releases_found=true\\n")


def _handle_fresh_start(config: Any, source_releases: list[dict[str, Any]]) -> bool:
    """Handle fresh start scenario."""
    if not source_releases:
        return False

    logging.info(f"Processing {len(source_releases)} source releases for fresh start")
    # Collect ALL apps from ALL releases to get complete picture
    all_apps_data = _collect_apps_from_releases(source_releases, config)

    if not all_apps_data:
        return False

    # Create release data for ALL apps that are available
    processed_data = _create_release_data_for_apps(all_apps_data, config)
    _save_fresh_start_data(processed_data)
    return True


def _process_releases(config: Any, new_releases: list[dict[str, Any]]) -> None:
    """Process new releases."""
    if not new_releases:
        logging.info("No new releases needed based on current state")
        if github_output := os.environ.get("GITHUB_OUTPUT"):
            with Path(github_output).open("a") as f:
                f.write("new_releases_found=false\n")
        return

    logging.info(f"Found {len(new_releases)} apps that need new releases")

    # Process new releases
    processed_data = process_new_releases(new_releases, config)

    if processed_data:
        logging.info("New releases were processed. Saving data for downstream jobs.")
        DOWNLOAD_DIR.mkdir(exist_ok=True)
        (DOWNLOAD_DIR / "releases.json").write_text(
            json.dumps(processed_data, indent=2)
        )

        # If digest mode is enabled, add releases to digest
        if getattr(config.digest, "enabled", False):
            add_release_to_digest(processed_data)

        if github_output := os.environ.get("GITHUB_OUTPUT"):
            with Path(github_output).open("a") as f:
                f.write("new_releases_found=true\n")
    else:
        logging.info("No new releases were processed")
        if github_output := os.environ.get("GITHUB_OUTPUT"):
            with Path(github_output).open("a") as f:
                f.write("new_releases_found=false\n")


def main() -> None:
    """Main function to manage releases based on Reddit posts as source of truth."""
    config = load_config()

    # Get current versions from Reddit posts
    logging.info("Fetching current app versions from Reddit posts")
    current_versions = get_current_versions_from_reddit()

    # If no posts found, this might be a fresh start
    if not current_versions:
        logging.info("No Reddit posts found. This might be a fresh start.")
        # For a fresh start, create release data for ALL available apps from ALL source releases
        # to generate comprehensive initial Reddit posts
        source_releases = get_source_releases(config.github.source_repo)
        if source_releases and _handle_fresh_start(config, source_releases):
            return

        logging.info("No action taken for fresh start scenario")
        return

    # Log current versions
    for app, version in current_versions.items():
        logging.info(f"Current version for {app}: {version}")

    # Identify what needs new releases
    new_releases = identify_new_releases(current_versions)
    _process_releases(config, new_releases)


if __name__ == "__main__":
    main()
