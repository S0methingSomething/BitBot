import argparse
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast
from unittest.mock import MagicMock

import praw
from packaging.version import parse as parse_version

import paths
from config_loader import load_config
from digest_aggregator import (
    format_digest_changelog,
    should_create_new_digest_cycle,
    start_new_digest_cycle,
)
from dry_run import (
    DryRunLevel,
    get_dry_run_level,
    is_dry_run,
)
from helpers import (
    get_bot_posts,
    init_reddit,
    load_bot_state,
    update_older_posts,
)
from io_handler import IOHandler
from logging_config import get_logger

logging = get_logger(__name__)

# --- Constants ---
MAX_OUTBOUND_LINKS_ERROR = 8


def _count_outbound_links(text: str) -> int:
    url_pattern = re.compile(r"https?://[^\s/$.?#].[^\s]*|www\.[^\s/$.?#].[^\s]*")
    return len(set(url_pattern.findall(text)))


def _create_app_list(apps: dict[str, Any]) -> str:
    """Create a formatted list of apps."""
    return ", ".join(
        f"{info.get('display_name', 'Unknown')} v{info.get('version', '?.?.?')}"
        for _, info in apps.items()
    )


def _format_title_for_added_apps(formats: Any, added_list: str) -> str:
    """Format title for added apps only."""
    template = formats.added_only
    return cast(str, template.replace("{{added_list}}", added_list))


def _format_title_for_updated_apps(
    formats: Any, updated_list: str, num_updated: int
) -> str:
    """Format title for updated apps only."""
    if num_updated == 1:
        template = formats.updated_only_single
    else:
        template = formats.updated_only_multi
    return cast(str, template.replace("{{updated_list}}", updated_list))


def _format_title_for_mixed_apps(
    formats: Any, added_list: str, updated_list: str, num_updated: int
) -> str:
    """Format title for mixed added and updated apps."""
    if num_updated == 1:
        template = formats.mixed_single_update
    else:
        template = formats.mixed_multi_update
    return cast(
        str,
        template.replace("{{added_list}}", added_list).replace(
            "{{updated_list}}", updated_list
        ),
    )


def _format_generic_title(formats: Any) -> str:
    """Format generic title."""
    template = formats.generic
    return cast(
        str, template.replace("{{date}}", datetime.now(UTC).strftime("%Y-%m-%d"))
    )


def _generate_dynamic_title(
    config: Any,
    added: dict[str, Any],
    updated: dict[str, Any],
    fresh_start: bool = False,
) -> str:
    num_added, num_updated = len(added), len(updated)
    formats = config.reddit.formats.titles

    # Special handling for fresh start
    if fresh_start and num_added > 0 and num_updated == 0:
        # For fresh start with only added apps, use a startup title
        return "[BitBot] Startup - Initial Release"

    def create_app_list(apps: dict[str, Any]) -> str:
        return ", ".join(
            f"{info.get('display_name', 'Unknown')} v{info.get('version', '?.?.?')}"
            for _, info in apps.items()
        )

    added_list = create_app_list(added)
    updated_list = create_app_list(updated)

    # Determine which format to use based on the counts
    if num_added > 0 and num_updated == 0:
        return _format_title_for_added_apps(formats, added_list)

    if num_added == 0 and num_updated > 0:
        return _format_title_for_updated_apps(formats, updated_list, num_updated)

    if num_added > 0 and num_updated > 0:
        return _format_title_for_mixed_apps(
            formats, added_list, updated_list, num_updated
        )

    # Generic case
    return _format_generic_title(formats)


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
    post_mode = config.reddit.post_mode
    key_suffix = "landing" if post_mode == "landing_page" else "direct"
    asset_name = config.github.asset_file_name
    formats = config.reddit.formats.changelog
    sections = []

    # Format each section
    for title, data in [("Added", added), ("Updated", updated), ("Removed", removed)]:
        section = _format_changelog_section(
            title, data, formats, asset_name, key_suffix
        )
        if section:
            sections.append(section)

    return "\n\n".join(sections) or "No new updates in this version."


def _generate_available_list(config: Any, all_releases: dict[str, Any]) -> str:
    formats = config.reddit.formats.table
    asset_name = config.github.asset_file_name
    lines = [formats.header, formats.divider]
    sorted_apps = sorted(all_releases.items(), key=lambda item: item[1]["display_name"])
    for _, info in sorted_apps:
        if latest := info.get("latest_release"):
            lines.append(
                formats.line.format(
                    display_name=info["display_name"],
                    asset_name=asset_name,
                    version=latest["version"],
                )
            )
    return "\n".join(lines)


def _generate_post_body(
    config: Any,
    changelog_data: dict[str, Any],
    all_releases: dict[str, Any],
    page_url: str,
) -> str:
    template_path = Path(paths.TEMPLATES_DIR) / config.reddit.templates.post
    raw_template = template_path.read_text()

    if start_tag := config.skip_content.start_tag:
        raw_template = re.sub(
            f"{re.escape(start_tag)}.*?{re.escape(config.skip_content.end_tag)}",
            "",
            raw_template,
            flags=re.DOTALL,
        )

    placeholders = {
        "changelog": _generate_changelog(config, **changelog_data),
        "available_list": _generate_available_list(config, all_releases),
        "initial_status": config.feedback.status_line_format.format(
            status=config.feedback.labels.unknown
        ),
        "download_portal_url": page_url,
        "bot_name": config.reddit.bot_name,
        "creator_username": config.reddit.creator,
        "subreddit": config.reddit.subreddit,
        "post_mode": config.reddit.post_mode,
        "bot_repo": config.github.bot_repo,
        "source_repo": config.github.source_repo,
        "asset_name": config.github.asset_file_name,
        "pages_url": config.github.pages_url or "",
        "version": "",  # Will be set based on releases
        "status": config.feedback.labels.unknown,  # Add status placeholder
    }

    # Add version information if we have releases
    if all_releases:
        # Get the first app's version as the main version
        for app_data in all_releases.values():
            if "latest_release" in app_data and "version" in app_data["latest_release"]:
                placeholders["version"] = app_data["latest_release"]["version"]
                break

    # Replace double curly brace placeholders
    for key, value in placeholders.items():
        raw_template = raw_template.replace(f"{{{{{key}}}}}", str(value))

    # Also replace single brace placeholders that might be left over
    for key, value in placeholders.items():
        raw_template = raw_template.replace(f"{{{key}}}", str(value))

    return cast(str, raw_template.strip())
    # Replace double curly brace placeholders
    for key, value in placeholders.items():
        raw_template = raw_template.replace(f"{{{{{key}}}}}", str(value))

    return cast(str, raw_template.strip())


def _post_new_release(
    reddit: praw.Reddit, title: str, body: str, config: Any
) -> praw.models.Submission:
    link_count = _count_outbound_links(body)
    warn_threshold = config.safety.max_outbound_links_warn
    logging.info(f"Post analysis: Found {link_count} unique outbound link(s).")
    if link_count > MAX_OUTBOUND_LINKS_ERROR:
        logging.error(
            f"Post contains {link_count} links, exceeding safety limit of {MAX_OUTBOUND_LINKS_ERROR}. Aborting."
        )
        sys.exit(1)
    if link_count > warn_threshold:
        logging.warning(
            f"Post contains {link_count} links, which is above the warning threshold of {warn_threshold}."
        )

    # Check dry-run level for different behaviors
    dry_run_level = get_dry_run_level()

    if dry_run_level == 0:  # Full dry-run
        logging.info(f"DRY_RUN: Would submit new post to r/{config.reddit.subreddit}")
        logging.info(f"  Title: {title}")
        logging.info(f"  Body: {body[:200]}...")  # Log first 200 chars of body
        # Return a mock submission object
        mock_submission = MagicMock()
        mock_submission.id = "mock-post-id-dry-run"
        mock_submission.title = title
        mock_submission.shortlink = "https://dry-run.reddit.post/mock-post-id"
        return mock_submission
    if dry_run_level in [1, 2]:  # Read-only or safe writes
        logging.info(
            f"DRY_RUN_LEVEL_{dry_run_level}: Would submit new post to r/{config.reddit.subreddit}"
        )
        logging.info(f"  Title: {title}")
        logging.info(f"  Body: {body[:200]}...")  # Log first 200 chars of body
        # Return a mock submission object
        mock_submission = MagicMock()
        mock_submission.id = "mock-post-id-read-only"
        mock_submission.title = title
        mock_submission.shortlink = "https://dry-run.reddit.post/mock-post-id"
        return mock_submission
    if dry_run_level == DryRunLevel.PUBLIC_PREVIEW:  # Public preview - create draft
        if is_dry_run():
            logging.info(
                f"PUBLIC_PREVIEW: Would submit draft post to r/{config.reddit.subreddit}"
            )
            logging.info(f"  Title: {title}")
            logging.info(f"  Body: {body[:200]}...")
            mock_submission = MagicMock()
            mock_submission.id = "mock-post-id-preview"
            mock_submission.title = f"[DRAFT] {title}"
            mock_submission.shortlink = "https://preview.reddit.post/mock-post-id"
            return mock_submission
        logging.info(f"Submitting draft post to r/{config.reddit.subreddit}: {title}")
        submission = reddit.subreddit(config.reddit.subreddit)
        # Submit as selftext but mark as draft (if Reddit API supports it)
        submission = submission.submit(f"[DRAFT] {title}", selftext=body)
        logging.info(f"Draft post successful: {submission.shortlink}")
        return submission
    # Production mode
    logging.info(f"Submitting new post to r/{config.reddit.subreddit}: {title}")
    submission = reddit.subreddit(config.reddit.subreddit)
    submission = submission.submit(title, selftext=body)
    logging.info(f"Post successful: {submission.shortlink}")
    return submission


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
    """Process added or updated apps."""
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


def _process_removed_apps(
    versions_to_check: dict[str, str],
    all_versions: dict[str, Any],
    removed: dict[str, Any],
    config: Any,
) -> None:
    """Process removed apps."""
    for app_id, current_v in versions_to_check.items():
        if app_id not in all_versions and current_v != "0.0.0":
            # Find the app display name from config
            display_name = app_id  # Default to app_id
            for app in config.apps:
                if app.id == app_id:
                    display_name = app.display_name
                    break
            removed[app_id] = {"display_name": display_name, "version": current_v}


def _get_version_changes(
    all_versions: dict[str, Any], versions_to_check: dict[str, str]
) -> dict[str, Any]:
    """Compares current versions with the latest versions and returns the changes."""
    added: dict[str, Any] = {}
    updated: dict[str, Any] = {}
    removed: dict[str, Any] = {}
    new_versions = versions_to_check.copy()

    # Load config to get app display names
    config = load_config()

    # Check for added or updated apps
    _process_added_or_updated_apps(
        all_versions, versions_to_check, added, updated, new_versions
    )

    # Check for removed apps (apps that were in versions_to_check but not in all_versions)
    _process_removed_apps(versions_to_check, all_versions, removed, config)

    return {
        "added": added,
        "updated": updated,
        "removed": removed,
        "new_versions": new_versions,
    }


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

    if start_tag := config.skip_content.start_tag:
        raw_template = re.sub(
            f"{re.escape(start_tag)}.*?{re.escape(config.skip_content.end_tag)}",
            "",
            raw_template,
            flags=re.DOTALL,
        )

    placeholders = {
        "changelog": changelog,
        "available_list": _generate_available_list(config, all_versions),
        "initial_status": config.feedback.status_line_format.format(
            status=config.feedback.labels.unknown
        ),
        "download_portal_url": page_url,
        "bot_name": config.reddit.bot_name,
        "creator_username": config.reddit.creator,
        "subreddit": config.reddit.subreddit,
        "post_mode": config.reddit.post_mode,
        "bot_repo": config.github.bot_repo,
        "source_repo": config.github.source_repo,
        "asset_name": config.github.asset_file_name,
        "pages_url": config.github.pages_url or "",
        "version": "",  # Will be set based on releases
        "status": config.feedback.labels.unknown,  # Add status placeholder
    }

    # Add version information if we have releases
    if all_versions:
        # Get the first app's version as the main version
        for app_data in all_versions.values():
            if "latest_release" in app_data and "version" in app_data["latest_release"]:
                placeholders["version"] = app_data["latest_release"]["version"]
                break

    # Replace double curly brace placeholders
    for key, value in placeholders.items():
        raw_template = raw_template.replace(f"{{{{{key}}}}}", str(value))

    # Also replace single brace placeholders that might be left over
    for key, value in placeholders.items():
        raw_template = raw_template.replace(f"{{{key}}}", str(value))

    return cast(str, raw_template.strip())


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
