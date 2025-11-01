"""Reddit posting functionality for BitBot."""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import deal
from beartype import beartype
from packaging.version import parse as parse_version

import paths
from core.config import load_config
from core.state import load_bot_state, save_bot_state
from reddit.client import init_reddit
from reddit.posting.body_builder import generate_post_body
from reddit.posting.poster import post_new_release
from reddit.posting.title_generator import generate_dynamic_title
from reddit.posts import get_bot_posts, update_older_posts


@deal.post(lambda result: result is None)  # type: ignore[misc]
@beartype  # type: ignore[misc]
def main() -> None:  # noqa: PLR0915, C901
    """Post a new release to Reddit if it's out of date."""
    parser = argparse.ArgumentParser(description="Post a new release to Reddit.")
    parser.add_argument("--page-url", required=False, default="", help="URL to GitHub Pages.")
    parser.add_argument("--generate-only", action="store_true", help="Generate without posting.")
    args = parser.parse_args()

    config = load_config()
    bot_state = load_bot_state()

    if not Path(paths.RELEASES_JSON_FILE).exists():
        sys.exit(0)

    with Path(paths.RELEASES_JSON_FILE).open(encoding="utf-8") as f:
        all_available_versions: dict[str, Any] = json.load(f)

    is_manual_mode = config["reddit"].get("post_manually", False) or args.generate_only
    versions_to_check = (
        bot_state["offline"]["last_generated_versions"]
        if is_manual_mode
        else bot_state["online"]["last_posted_versions"]
    )

    added_apps: dict[str, Any] = {}
    updated_apps: dict[str, Any] = {}
    removed_apps: dict[str, Any] = {}
    new_versions_state = versions_to_check.copy()

    for app_id, app_data in all_available_versions.items():
        if not app_data.get("latest_release"):
            continue

        latest_version_str: str = app_data["latest_release"]["version"]
        current_version_str: str = versions_to_check.get(app_id, "0.0.0")

        if parse_version(latest_version_str) > parse_version(current_version_str):
            new_versions_state[app_id] = latest_version_str
            if current_version_str == "0.0.0":
                added_apps[app_id] = {
                    "display_name": app_data["display_name"],
                    "version": latest_version_str,
                    "url": app_data["latest_release"]["download_url"],
                }
            else:
                updated_apps[app_id] = {
                    "new": {
                        "display_name": app_data["display_name"],
                        "version": latest_version_str,
                        "url": app_data["latest_release"]["download_url"],
                    },
                    "old": current_version_str,
                }

    changelog_data = {"added": added_apps, "updated": updated_apps, "removed": removed_apps}
    if not any(changelog_data.values()):
        sys.exit(0)

    post_mode = config["reddit"].get("postMode", "landing_page")
    github_pages_url: str = config.get("github", {}).get("pages_url", "https://example.com")

    # Rolling update mode
    if post_mode == "rolling_update" and not is_manual_mode:
        reddit = init_reddit(config)
        existing_posts = get_bot_posts(reddit, config)

        if existing_posts:
            latest_post = existing_posts[0]
            post_age_days = (
                datetime.now(timezone.utc)
                - datetime.fromtimestamp(latest_post.created_utc, tz=timezone.utc)
            ).days

            days_limit = config["reddit"].get("rolling", {}).get("daysBeforeNewPost", 7)

            if post_age_days < days_limit:
                title = generate_dynamic_title(config, added_apps, updated_apps)
                body = generate_post_body(
                    config, changelog_data, all_available_versions, args.page_url or github_pages_url
                )

                latest_post.edit(body=body)
                bot_state["online"]["last_posted_versions"] = new_versions_state
                bot_state["online"]["activePostId"] = latest_post.id
                save_bot_state(bot_state)
                sys.exit(0)

    title = generate_dynamic_title(config, added_apps, updated_apps)
    body = generate_post_body(
        config, changelog_data, all_available_versions, args.page_url or github_pages_url
    )

    if is_manual_mode:
        Path(paths.DIST_DIR).mkdir(parents=True, exist_ok=True)
        Path(paths.DIST_DIR, "post_title.txt").write_text(title, encoding="utf-8")
        Path(paths.DIST_DIR, "post_body.md").write_text(body, encoding="utf-8")
        bot_state["offline"]["last_generated_versions"] = new_versions_state
        save_bot_state(bot_state)
        sys.exit(0)

    reddit = init_reddit(config)
    existing_posts = get_bot_posts(reddit, config)
    new_submission = post_new_release(reddit, title, body, config)

    if existing_posts:
        update_older_posts(
            existing_posts,
            {"title": new_submission.title, "url": new_submission.shortlink, "version": "latest"},
            config,
        )

    bot_state["online"]["last_posted_versions"] = new_versions_state
    bot_state["online"]["activePostId"] = new_submission.id
    save_bot_state(bot_state)


if __name__ == "__main__":
    main()
