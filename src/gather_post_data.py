import json
import os
import sys
from pathlib import Path
from typing import Any

from github import Github, GithubException
from packaging.version import parse as parse_version

import paths
from helpers import load_config, parse_release_notes
from logging_config import get_logger

logging = get_logger(__name__)


def _parse_and_add_release(release: Any, aggregated_data: dict[str, Any], config: dict[str, Any]) -> None:
    """Parses a single release and adds it to the aggregated data."""
    parsed_info = parse_release_notes(release.body, release.tag_name, release.title, config)
    if not parsed_info:
        logging.warning(f"Could not parse release tag {release.tag_name}. Skipping.")
        return

    app_id = parsed_info["app_id"]
    version = parsed_info["version"]
    asset_name = parsed_info.get("asset_name")

    app_data = aggregated_data.setdefault(app_id, {"display_name": parsed_info["display_name"], "releases_by_version": {}})
    version_releases = app_data["releases_by_version"].setdefault(version, [])

    download_url = next((asset.browser_download_url for asset in release.get_assets() if asset.name == asset_name), None)
    if not download_url:
        logging.warning(f"No matching asset found for release {release.tag_name}. Skipping.")
        return

    version_releases.append({
        "version": version, "download_url": download_url, "published_at": release.published_at.isoformat(),
        "release_notes": release.body, "release_url": release.html_url, "tag_name": release.tag_name
    })

def _process_releases(releases: Any, config: dict[str, Any]) -> dict[str, Any]:
    """Processes a list of releases and aggregates the data."""
    aggregated_data: dict[str, Any] = {}
    for release in releases:
        _parse_and_add_release(release, aggregated_data, config)
    return aggregated_data

def _find_best_release(release_group: list[dict[str, Any]], app_id: str) -> dict[str, Any]:
    """Finds the best release from a group of releases with the same version."""
    if len(release_group) == 1:
        return release_group[0]
    best = next((r for r in release_group if r["tag_name"].startswith(f"{app_id}-v")), None)
    return best or sorted(release_group, key=lambda x: x["published_at"], reverse=True)[0]

def _finalize_data(aggregated_data: dict[str, Any]) -> dict[str, Any]:
    """Finalizes the aggregated data by cleaning and sorting releases."""
    final_data: dict[str, Any] = {}
    for app_id, app_info in aggregated_data.items():
        clean_releases = [_find_best_release(group, app_id) for group in app_info["releases_by_version"].values()]
        clean_releases.sort(key=lambda r: parse_version(r["version"]), reverse=True)
        final_data[app_id] = {
            "display_name": app_info["display_name"],
            "latest_release": clean_releases[0] if clean_releases else None,
            "previous_releases": clean_releases[1:]
        }
    return final_data

def main() -> None:
    config = load_config()
    g = Github(os.getenv("GITHUB_TOKEN"))
    bot_repo_name = config["github"]["botRepo"]

    try:
        bot_repo = g.get_repo(bot_repo_name)
        logging.info(f"Fetching all releases from bot repository: {bot_repo_name}")
        bot_releases = bot_repo.get_releases()
    except GithubException as e:
        logging.error(f"Failed to get repositories: {e}")
        sys.exit(1)

    aggregated_data = _process_releases(bot_releases, config)
    final_data = _finalize_data(aggregated_data)

    dist_dir = Path(paths.DIST_DIR)
    dist_dir.mkdir(exist_ok=True)
    (dist_dir / "releases.json").write_text(json.dumps(final_data, indent=4))

    logging.info(f"Successfully generated clean, structured release data at {paths.RELEASES_JSON_FILE}")

if __name__ == "__main__":
    # This allows the script to be run directly for testing
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    main()
