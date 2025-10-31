"""Gather and aggregate release data from GitHub."""

import json
import sys
from pathlib import Path

import deal
from beartype import beartype
from github import Auth, Github, GithubException
from packaging.version import parse as parse_version

from core.config import load_config
from core.credentials import Credentials
from gh.parser import parse_release_notes


@deal.post(lambda result: result is None)  # type: ignore[misc]
@beartype  # type: ignore[misc]
def main() -> None:  # noqa: C901, PLR0912
    """Gather and aggregate release data from GitHub."""
    config = load_config()
    auth = Auth.Token(Credentials.get_github_token())
    g = Github(auth=auth)
    bot_repo_name = config["github"]["botRepo"]

    try:
        bot_repo = g.get_repo(bot_repo_name)
        bot_releases = bot_repo.get_releases()
    except GithubException:
        sys.exit(1)

    # --- Data Aggregation and Cleaning Pipeline ---
    aggregated_data = {}
    for release in bot_releases:
        parsed_info = parse_release_notes(release.body, release.tag_name, release.title, config)
        if not parsed_info:
            continue

        app_id = parsed_info["app_id"]
        version = parsed_info["version"]

        if app_id not in aggregated_data:
            aggregated_data[app_id] = {
                "display_name": parsed_info["display_name"],
                "releases_by_version": {},
            }

        if version not in aggregated_data[app_id]["releases_by_version"]:
            aggregated_data[app_id]["releases_by_version"][version] = []

        download_url = next(
            (
                asset.browser_download_url
                for asset in release.get_assets()
                if asset.name == parsed_info.get("asset_name")
            ),
            None,
        )
        if not download_url:
            continue

        aggregated_data[app_id]["releases_by_version"][version].append(
            {
                "version": version,
                "download_url": download_url,
                "published_at": release.published_at.isoformat(),
                "release_notes": release.body,
                "release_url": release.html_url,
                "tag_name": release.tag_name,
            }
        )

    final_data = {}
    for app_id, app_info in aggregated_data.items():
        clean_releases = []
        for release_group in app_info["releases_by_version"].values():
            if len(release_group) == 1:
                clean_releases.append(release_group[0])
            else:
                best_release = next(
                    (r for r in release_group if r["tag_name"].startswith(f"{app_id}-v")), None
                )
                if not best_release:
                    best_release = sorted(
                        release_group, key=lambda x: x["published_at"], reverse=True
                    )[0]
                clean_releases.append(best_release)

        clean_releases.sort(key=lambda r: parse_version(r["version"]), reverse=True)

        if clean_releases:
            final_data[app_id] = {
                "display_name": app_info["display_name"],
                "latest_release": clean_releases[0],
                "previous_releases": clean_releases[1:],
            }
        else:
            final_data[app_id] = {
                "display_name": app_info["display_name"],
                "latest_release": None,
                "previous_releases": [],
            }

    Path(paths.DIST_DIR).mkdir(parents=True, exist_ok=True)
    with Path(paths.RELEASES_JSON_FILE).open("w") as f:
        json.dump(final_data, f, indent=4)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))
    import paths

    main()
