"""Maintain releases by marking older ones as pre-release."""

import sys

import deal
import requests
from beartype import beartype

from bitbot.core.config import load_config
from bitbot.core.credentials import Credentials


@deal.post(lambda result: result is None)  # type: ignore[misc]
@beartype  # type: ignore[misc]
def main() -> None:
    """Marks old GitHub releases with an [OUTDATED] prefix."""
    config = load_config()
    bot_repo = config["github"]["botRepo"]
    token = Credentials.get_github_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    releases_url = f"https://api.github.com/repos/{bot_repo}/releases"
    try:
        response = requests.get(releases_url, headers=headers, timeout=30)
        response.raise_for_status()
        releases = response.json()
    except requests.RequestException:
        sys.exit(1)

    # A legacy release is defined by having a version in the tag like '-v1.2.3'
    # The new generic releases do not have this pattern.
    non_legacy_releases = [r for r in releases if "-v" not in r.get("tag_name", "")]

    if not non_legacy_releases or len(non_legacy_releases) < 2:  # noqa: PLR2004
        sys.exit(0)

    non_legacy_releases[0]
    older_releases = non_legacy_releases[1:]

    updated_count = 0
    for release in older_releases:
        release_id = release["id"]
        current_title = release["name"]

        if current_title.startswith("[OUTDATED] "):
            continue

        new_title = f"[OUTDATED] {current_title}"
        update_url = f"https://api.github.com/repos/{bot_repo}/releases/{release_id}"
        payload = {"name": new_title}

        try:
            update_response = requests.patch(update_url, headers=headers, json=payload, timeout=30)
            update_response.raise_for_status()
            updated_count += 1
        except requests.RequestException:
            pass


if __name__ == "__main__":
    main()
