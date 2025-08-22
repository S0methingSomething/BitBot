import os
import sys
from typing import Any, cast

import requests

from helpers import load_config
from logging_config import get_logger

logging = get_logger(__name__)

MIN_RELEASES_TO_MARK_OUTDATED = 2


def _fetch_releases(repo: str, headers: dict[str, str]) -> list[dict[str, Any]]:
    """Fetches all releases from the specified repository."""
    releases_url = f"https://api.github.com/repos/{repo}/releases"
    try:
        response = requests.get(releases_url, headers=headers, timeout=10)
        response.raise_for_status()
        return cast(list[dict[str, Any]], response.json())
    except requests.RequestException as e:
        logging.error(f"Could not fetch releases: {e}")
        sys.exit(1)

def _update_release_title(release: dict[str, Any], repo: str, headers: dict[str, str]) -> bool:
    """Updates a single release title to mark it as outdated."""
    if release["name"].startswith("[OUTDATED] "):
        return False

    logging.info(f"Updating non-legacy release '{release['name']}'...")
    new_title = f"[OUTDATED] {release['name']}"
    update_url = f"https://api.github.com/repos/{repo}/releases/{release['id']}"
    payload = {"name": new_title}

    try:
        update_response = requests.patch(update_url, headers=headers, json=payload, timeout=10)
        update_response.raise_for_status()
        logging.info(f"-> Successfully updated to '{new_title}'.")
        return True
    except requests.RequestException:
        logging.warning(f"Failed to update release {release['id']}. Status: {update_response.status_code}, Body: {update_response.text}")
        return False

def main() -> None:
    """
    Marks old GitHub releases with an [OUTDATED] prefix.
    """
    config = load_config()
    bot_repo = config["github"]["botRepo"]
    token = os.environ["GITHUB_TOKEN"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    releases = _fetch_releases(bot_repo, headers)
    non_legacy_releases = [r for r in releases if "-v" not in r.get("tag_name", "")]

    if len(non_legacy_releases) < MIN_RELEASES_TO_MARK_OUTDATED:
        logging.info("Not enough non-legacy releases to mark any as outdated. Exiting.")
        sys.exit(0)

    latest_release = non_legacy_releases[0]
    older_releases = non_legacy_releases[1:]

    logging.info(f"Latest non-legacy release is {latest_release['tag_name']}. Checking {len(older_releases)} older non-legacy release(s).")

    updated_count = sum(1 for release in older_releases if _update_release_title(release, bot_repo, headers))
    logging.info(f"Maintenance complete. Updated {updated_count} release title(s).")

if __name__ == "__main__":
    main()
