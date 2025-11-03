"""One-time migration script for legacy releases."""

import sys
from pathlib import Path

import deal
from beartype import beartype
from github import Auth, Github, GithubException

from bitbot.core.config import load_config
from bitbot.core.credentials import Credentials
from bitbot.gh.parser import parse_release_notes  # Still in helpers.py


@deal.post(lambda result: result is None)  # type: ignore[misc]
@beartype  # type: ignore[misc]
def migrate_releases() -> None:
    """Performs a one-time migration of all legacy releases to a new structured format.

    Leverages the centralized parser to update release bodies.
    """
    config = load_config()
    auth = Auth.Token(Credentials.get_github_token())
    g = Github(auth=auth)
    bot_repo_name = config["github"]["botRepo"]

    try:
        repo = g.get_repo(bot_repo_name)
        releases = repo.get_releases()
    except GithubException:
        sys.exit(1)

    updated_count = 0
    failed_count = 0

    for release in releases:
        # 1. Check if the release is already in the new, fully structured format
        if "app:" in release.body and "version:" in release.body and "asset_name:" in release.body:
            continue

        # 2. Use the one true parser to derive the release info
        parsed_info = parse_release_notes(release.body, release.tag_name, release.title, config)

        if not parsed_info:
            failed_count += 1
            continue

        app_id = parsed_info["app_id"]
        version = parsed_info["version"]
        asset_name = parsed_info["asset_name"]

        # 3. Construct the new structured body
        new_body = f"""app: {app_id}
version: {version}
asset_name: {asset_name}
"""

        # 4. Update the release on GitHub
        try:
            release.update_release(name=release.title, message=new_body)
            updated_count += 1
        except GithubException:
            failed_count += 1

    if failed_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))
    migrate_releases()
