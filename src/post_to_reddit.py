import argparse
import json
import sys
from pathlib import Path
from typing import Any

import praw
from packaging.version import parse as parse_version

import paths
from config_loader import load_config
from credentials import setup_credentials
from digest_aggregator import (
    format_digest_changelog,
    should_create_new_digest_cycle,
    start_new_digest_cycle,
)
from dry_run import is_dry_run
from helpers import (
    get_bot_posts,
    init_reddit,
    load_bot_state,
    update_older_posts,
)
from io_handler import IOHandler
from logging_config import get_logger
from placeholder_parser import generate_post_placeholders, process_placeholders
from reddit.available_list_generator import generate_available_list
from reddit.changelog_generator import generate_changelog
from reddit.post_body_generator import generate_post_body
from reddit.poster import post_new_release
from reddit.title_generator import generate_dynamic_title
from reddit.version_detector import get_version_changes

logging = get_logger(__name__)

# Auto-setup credentials
try:
    config = load_config()
    auto_save = getattr(config.auth, "auto_save", False)
    auto_load = getattr(config.auth, "auto_load", False)
    setup_credentials(auto_save=auto_save, auto_load=auto_load)
except Exception:
    logging.warning("Failed to auto-setup credentials")


def _generate_dynamic_title(
    config: Any,
    added: dict[str, Any],
    updated: dict[str, Any],
    fresh_start: bool = False,
) -> str:
    """Generate a dynamic title for a Reddit post."""
    return str(generate_dynamic_title(config, added, updated, fresh_start))


def _format_added_changelog_line(
    line_format: str, info: dict[str, Any], asset_name: str
) -> str:
    """Format a single added line in the changelog."""
    return line_format.format(
        display_name=info["display_name"],
        asset_name=asset_name,
        version=info["version"],
        download_url=info["url"],
    )


def _format_updated_changelog_line(
    line_format: str, info: dict[str, Any], asset_name: str
) -> str:
    """Format a single updated line in the changelog."""
    return line_format.format(
        display_name=info["new"]["display_name"],
        asset_name=asset_name,
        new_version=info["new"]["version"],
        old_version=info["old"],
        download_url=info["new"]["url"],
    )


def _format_removed_changelog_line(
    line_format: str, info: dict[str, Any], asset_name: str
) -> str:
    """Format a single removed line in the changelog."""
    return line_format.format(
        display_name=info["display_name"],
        asset_name=asset_name,
        old_version=info["version"],
    )


def _format_changelog_line(
    line_format: str, info: dict[str, Any], asset_name: str, change_type: str
) -> str:
    """Formats a single line in the changelog."""
    if change_type == "Added":
        return _format_added_changelog_line(line_format, info, asset_name)
    if change_type == "Updated":
        return _format_updated_changelog_line(line_format, info, asset_name)
    if change_type == "Removed":
        return _format_removed_changelog_line(line_format, info, asset_name)
    return ""


def _format_changelog_section(
    title: str, data: dict[str, Any], formats: Any, asset_name: str, key_suffix: str
) -> str:
    """Format a single changelog section."""
    if not data:
        return ""

    lines = [f"### {title}"]
    key_format = f"{title.lower()}_{key_suffix}"
    if hasattr(formats, key_format):
        line_format = getattr(formats, key_format)
        lines.extend(
            _format_changelog_line(line_format, info, asset_name, title)
            for info in data.values()
        )
    if len(lines) > 1:
        return "\n".join(lines)
    return ""


def _generate_changelog(
    config: Any, added: dict[str, Any], updated: dict[str, Any], removed: dict[str, Any]
) -> str:
    """Generate a changelog for a Reddit post."""
    return str(generate_changelog(config, added, updated, removed))


def _generate_available_list(config: Any, all_releases: dict[str, Any]) -> str:
    """Generate an available list for a Reddit post."""
    return str(generate_available_list(config, all_releases))


def _generate_post_body(
    config: Any,
    changelog_data: dict[str, Any],
    all_releases: dict[str, Any],
    page_url: str,
) -> str:
    """Generate the body of a Reddit post."""
    return str(generate_post_body(config, changelog_data, all_releases, page_url))


def _post_new_release(
    reddit: praw.Reddit, title: str, body: str, config: Any
) -> praw.models.Submission:
    """Post a new release to Reddit."""
    return post_new_release(reddit, title, body, config)


def _check_added_or_updated_apps(
    all_versions: dict[str, Any],
    versions_to_check: dict[str, str],
    added: dict[str, Any],
    updated: dict[str, Any],
    new_versions: dict[str, str],
) -> None:
    """Check for added or updated apps."""
    for app_id, data in all_versions.items():
        if not (latest := data.get("latest_release")):
            continue
        current_v = versions_to_check.get(app_id, "0.0.0")
        if parse_version(latest["version"]) > parse_version(current_v):
            new_versions[app_id] = latest["version"]
            if current_v == "0.0.0":
                added[app_id] = {
                    "display_name": data["display_name"],
                    "version": latest["version"],
                    "url": latest["download_url"],
                }
            else:
                updated[app_id] = {
                    "new": {
                        "display_name": data["display_name"],
                        "version": latest["version"],
                        "url": latest["download_url"],
                    },
                    "old": current_v,
                }
        elif parse_version(latest["version"]) < parse_version(current_v):
            # Handle version rollback
            updated[app_id] = {
                "new": {
                    "display_name": data["display_name"],
                    "version": latest["version"],
                    "url": latest["download_url"],
                },
                "old": current_v,
            }


def _check_removed_apps(
    versions_to_check: dict[str, str],
    all_versions: dict[str, Any],
    removed: dict[str, Any],
    config: Any,
) -> None:
    """Check for removed apps."""
    for app_id, current_v in versions_to_check.items():
        if app_id not in all_versions and current_v != "0.0.0":
            # Find the app display name from config
            display_name = app_id  # Default to app_id
            for app in config.apps:
                if app.id == app_id:
                    display_name = app.display_name
                    break
            removed[app_id] = {"display_name": display_name, "version": current_v}


def _process_added_or_updated_apps(
    all_versions: dict[str, Any],
    versions_to_check: dict[str, str],
    added: dict[str, Any],
    updated: dict[str, Any],
    new_versions: dict[str, str],
) -> None:
    """Process added or updated apps.

    DEPRECATED: This function has been moved to reddit.version_detector module.
    """
    # This function is now in the version_detector module


def _process_removed_apps(
    versions_to_check: dict[str, str],
    all_versions: dict[str, Any],
    removed: dict[str, Any],
    config: Any,
) -> None:
    """Process removed apps.

    DEPRECATED: This function has been moved to reddit.version_detector module.
    """
    # This function is now in the version_detector module


def _get_version_changes(
    all_versions: dict[str, Any], versions_to_check: dict[str, str]
) -> dict[str, Any]:
    """Compares current versions with the latest versions and returns the changes."""
    return dict(get_version_changes(all_versions, versions_to_check))


def _handle_manual_post(
    title: str, body: str, new_versions: dict[str, str], bot_state: dict[str, Any]
) -> None:
    """Handles the generation of post files for manual posting."""
    dist_dir = Path(paths.DIST_DIR)
    dist_dir.mkdir(exist_ok=True)
    (dist_dir / "post_title.txt").write_text(title)
    (dist_dir / "post_body.md").write_text(body)
    bot_state["offline"]["last_generated_versions"] = new_versions
    IOHandler.save_bot_state(bot_state)
    logging.info(
        f"Successfully generated post files in {dist_dir} and updated offline state."
    )


def _initialize_state() -> dict[str, Any]:
    """Parses arguments and initializes the state."""
    parser = argparse.ArgumentParser(
        description="Post a new release to Reddit if it's out of date."
    )
    parser.add_argument(
        "--page-url", default="", help="URL to the GitHub Pages landing page."
    )
    parser.add_argument(
        "--generate-only",
        action="store_true",
        help="Generate post content without posting.",
    )
    args, _ = parser.parse_known_args()
    config = load_config()
    bot_state = load_bot_state()
    return {"args": args, "config": config, "bot_state": bot_state}


def _create_and_submit_post(
    config: Any,
    bot_state: dict[str, Any],
    version_changes: dict[str, Any],
    all_versions: dict[str, Any],
    page_url: str,
) -> None:
    """Creates the post content and submits it to Reddit."""
    # Check if digest mode is enabled
    if getattr(config.digest, "enabled", False):
        _create_and_submit_digest_post(
            config, bot_state, version_changes, all_versions, page_url
        )
    else:
        _create_and_submit_regular_post(
            config, bot_state, version_changes, all_versions, page_url
        )


def _create_and_submit_regular_post(
    config: Any,
    bot_state: dict[str, Any],
    version_changes: dict[str, Any],
    all_versions: dict[str, Any],
    page_url: str,
) -> None:
    """Creates and submits a regular post."""
    changelog_data = {
        k: v for k, v in version_changes.items() if k in ["added", "updated", "removed"]
    }

    # Check if this is a fresh start by looking for the flag file
    fresh_start = (Path(paths.DIST_DIR) / "fresh_start.flag").exists()

    title = _generate_dynamic_title(
        config,
        added=changelog_data["added"],
        updated=changelog_data["updated"],
        fresh_start=fresh_start,
    )
    body = _generate_post_body(config, changelog_data, all_versions, page_url)

    is_manual = config.reddit.post_manually
    if is_manual:
        _handle_manual_post(title, body, version_changes["new_versions"], bot_state)
        sys.exit(0)

    reddit = init_reddit(config)
    new_submission = _post_new_release(reddit, title, body, config)
    if not is_dry_run() and (existing_posts := get_bot_posts(reddit, config)):
        update_older_posts(
            existing_posts,
            {
                "title": new_submission.title,
                "url": new_submission.shortlink,
                "version": "latest",
            },
            config,
        )

    bot_state["online"].update(
        {
            "last_posted_versions": version_changes["new_versions"],
            "activePostId": new_submission.id,
        }
    )
    IOHandler.save_bot_state(bot_state)
    logging.info("Post and update process complete. Online state updated.")


def _create_digest_post(args: dict[str, Any]) -> None:
    """Create and submit a digest post with all changes from the previous cycle."""
    config = args["config"]
    releases = args["releases"]
    version_changes = args["version_changes"]
    all_versions = args["all_versions"]
    page_url = args["page_url"]
    bot_state = args["bot_state"]

    # Create digest post with all changes from the previous cycle
    changelog = format_digest_changelog(releases, config)

    # Create title for digest post
    title = f"[BitBot] Weekly Digest - {len(releases)} Updates"

    # For body, we'll need to customize this for digest format
    body = _generate_digest_post_body(config, changelog, all_versions, page_url)

    # Handle manual posting
    is_manual = config.reddit.post_manually
    if is_manual:
        _handle_manual_post(title, body, version_changes["new_versions"], bot_state)
        return

    # Post to Reddit
    reddit = init_reddit(config)
    new_submission = _post_new_release(reddit, title, body, config)

    # Mark previous posts as outdated
    if not is_dry_run() and (existing_posts := get_bot_posts(reddit, config)):
        update_older_posts(
            existing_posts,
            {
                "title": new_submission.title,
                "url": new_submission.shortlink,
                "version": "latest",
            },
            config,
        )

    # Update bot state
    bot_state["online"].update(
        {
            "last_posted_versions": version_changes["new_versions"],
            "activePostId": new_submission.id,
        }
    )
    IOHandler.save_bot_state(bot_state)
    logging.info("Digest post created and previous posts marked as outdated.")


def _create_regular_update_post(args: dict[str, Any]) -> None:
    """Create and submit a regular update post for the digest cycle."""
    config = args["config"]
    version_changes = args["version_changes"]
    all_versions = args["all_versions"]
    page_url = args["page_url"]
    bot_state = args["bot_state"]

    changelog_data = {
        k: v for k, v in version_changes.items() if k in ["added", "updated", "removed"]
    }

    # Check if this is a fresh start by looking for the flag file
    fresh_start = (Path(paths.DIST_DIR) / "fresh_start.flag").exists()

    title = _generate_dynamic_title(
        config,
        added=changelog_data["added"],
        updated=changelog_data["updated"],
        fresh_start=fresh_start,
    )
    body = _generate_post_body(config, changelog_data, all_versions, page_url)

    is_manual = config.reddit.post_manually
    if is_manual:
        _handle_manual_post(title, body, version_changes["new_versions"], bot_state)
        sys.exit(0)

    reddit = init_reddit(config)
    new_submission = _post_new_release(reddit, title, body, config)
    if not is_dry_run() and (existing_posts := get_bot_posts(reddit, config)):
        update_older_posts(
            existing_posts,
            {
                "title": new_submission.title,
                "url": new_submission.shortlink,
                "version": "latest",
            },
            config,
        )

    bot_state["online"].update(
        {
            "last_posted_versions": version_changes["new_versions"],
            "activePostId": new_submission.id,
        }
    )
    IOHandler.save_bot_state(bot_state)
    logging.info("Regular update post created for digest cycle.")


def _create_and_submit_digest_post(
    config: Any,
    bot_state: dict[str, Any],
    version_changes: dict[str, Any],
    all_versions: dict[str, Any],
    page_url: str,
) -> None:
    """Creates and submits a digest post."""

    # Check if we should start a new cycle
    if should_create_new_digest_cycle(config):
        # Start new cycle and get previous cycle data
        previous_cycle = start_new_digest_cycle()
        releases = previous_cycle.get("releases", [])

        if releases:
            _create_digest_post(
                {
                    "config": config,
                    "releases": releases,
                    "version_changes": version_changes,
                    "all_versions": all_versions,
                    "page_url": page_url,
                    "bot_state": bot_state,
                }
            )
            return

    # Regular update - just add current changes to ongoing cycle
    _create_regular_update_post(
        {
            "config": config,
            "version_changes": version_changes,
            "all_versions": all_versions,
            "page_url": page_url,
            "bot_state": bot_state,
        }
    )


def _generate_digest_post_body(
    config: Any, changelog: str, all_versions: dict[str, Any], page_url: str
) -> str:
    """Generates a post body for digest posts."""
    template_path = Path(paths.TEMPLATES_DIR) / config.reddit.templates.post
    raw_template = template_path.read_text()

    # Create changelog data structure for digest
    changelog_data: dict[str, Any] = {
        "added": {},
        "updated": {},
        "removed": {},
    }

    # Generate placeholders
    placeholders = generate_post_placeholders(
        changelog_data,
        all_versions,
        page_url,
        config,
    )

    # Override changelog with digest content
    placeholders["changelog"] = changelog

    # Process template with placeholders
    return str(process_placeholders(raw_template, placeholders, config))


def main() -> None:
    state = _initialize_state()
    args, config, bot_state = state["args"], state["config"], state["bot_state"]

    releases_path = Path(paths.RELEASES_JSON_FILE)
    if not releases_path.exists():
        logging.info(f"`{releases_path}` not found. Nothing to post.")
        sys.exit(0)

    all_versions = json.loads(releases_path.read_text())
    versions_to_check = bot_state["offline" if args.generate_only else "online"][
        "last_generated_versions" if args.generate_only else "last_posted_versions"
    ]

    version_changes = _get_version_changes(all_versions, versions_to_check)
    if not any(
        [
            version_changes["added"],
            version_changes["updated"],
            version_changes["removed"],
        ]
    ):
        logging.info("No changes detected. State is up-to-date.")
        sys.exit(0)

    page_url = args.page_url or (
        getattr(config.github, "pages_url", "") if config.github else ""
    )
    _create_and_submit_post(config, bot_state, version_changes, all_versions, page_url)


def run_poster() -> None:
    """Run the Reddit poster without argument parsing."""

    # Create mock args object
    class MockArgs:
        def __init__(self) -> None:
            self.page_url = ""
            self.generate_only = False

    args = MockArgs()
    config = load_config()
    bot_state = load_bot_state()
    releases_path = Path(paths.RELEASES_JSON_FILE)
    if not releases_path.exists():
        logging.info(f"`{releases_path}` not found. Nothing to post.")
        return
    all_versions = json.loads(releases_path.read_text())
    versions_to_check = bot_state["online"]["last_posted_versions"]

    version_changes = _get_version_changes(all_versions, versions_to_check)
    if not any(
        [
            version_changes["added"],
            version_changes["updated"],
            version_changes["removed"],
        ]
    ):
        logging.info("No changes detected. State is up-to-date.")
        return

    page_url = args.page_url or (
        getattr(config.github, "pages_url", "") if config.github else ""
    )
    _create_and_submit_post(config, bot_state, version_changes, all_versions, page_url)


if __name__ == "__main__":
    main()
