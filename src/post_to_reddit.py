import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, cast

import praw
from packaging.version import parse as parse_version

import paths
from helpers import (
    get_bot_posts,
    init_reddit,
    load_bot_state,
    load_config,
    save_bot_state,
    update_older_posts,
)
from logging_config import get_logger

logging = get_logger(__name__)

# --- Constants ---
MAX_OUTBOUND_LINKS_ERROR = 8

def _count_outbound_links(text: str) -> int:
    url_pattern = re.compile(r"https?://[^\s/$.?#].[^\s]*|www\.[^\s/$.?#].[^\s]*")
    return len(set(url_pattern.findall(text)))

def _generate_dynamic_title(config: Dict[str, Any], added: Dict[str, Any], updated: Dict[str, Any]) -> str:
    num_added, num_updated = len(added), len(updated)
    formats = config["reddit"]["formats"]["titles"]

    def create_app_list(apps: Dict[str, Any]) -> str:
        return ", ".join(f"{info.get('display_name', 'Unknown')} v{info.get('version', '?.?.?')}" for _, info in apps.items())

    added_list = create_app_list(added)
    updated_list = create_app_list(updated)

    if num_added > 0 and num_updated == 0:
        return cast(str, formats["added_only"].replace("{{added_list}}", added_list))
    if num_added == 0 and num_updated > 0:
        key = "updated_only_single" if num_updated == 1 else "updated_only_multi"
        return cast(str, formats[key].replace("{{updated_list}}", updated_list))
    if num_added > 0 and num_updated > 0:
        key = "mixed_single_update" if num_updated == 1 else "mixed_multi_update"
        return cast(str, formats[key].replace("{{added_list}}", added_list).replace("{{updated_list}}", updated_list))

    return cast(str, formats["generic"].replace("{{date}}", datetime.utcnow().strftime("%Y-%m-%d")))

def _format_changelog_line(line_format: str, info: Dict[str, Any], asset_name: str, change_type: str) -> str:
    """Formats a single line in the changelog."""
    if change_type == "Added":
        return line_format.format(display_name=info["display_name"], asset_name=asset_name, version=info["version"], download_url=info["url"])
    if change_type == "Updated":
        return line_format.format(display_name=info["new"]["display_name"], asset_name=asset_name, new_version=info["new"]["version"], old_version=info["old"], download_url=info["new"]["url"])
    if change_type == "Removed":
        return line_format.format(display_name=info["display_name"], asset_name=asset_name, old_version=info["version"])
    return ""

def _generate_changelog(config: Dict[str, Any], added: Dict[str, Any], updated: Dict[str, Any], removed: Dict[str, Any]) -> str:
    post_mode = config["reddit"].get("postMode", "landing_page")
    key_suffix = "landing" if post_mode == "landing_page" else "direct"
    asset_name = config["github"].get("assetFileName", "asset")
    formats = config["reddit"]["formats"]["changelog"]
    sections = []

    change_types = {"Added": added, "Updated": updated, "Removed": removed}
    for title, data in change_types.items():
        if not data:
            continue
        lines = [f"### {title}"]
        key_format = f"{title.lower()}_{key_suffix}"
        if line_format := formats.get(key_format):
            for _, info in data.items():
                lines.append(_format_changelog_line(line_format, info, asset_name, title))
        if len(lines) > 1:
            sections.append("\n".join(lines))

    return "\n\n".join(sections) or "No new updates in this version."

def _generate_available_list(config: Dict[str, Any], all_releases: Dict[str, Any]) -> str:
    formats = config["reddit"]["formats"]["table"]
    asset_name = config["github"]["assetFileName"]
    lines = [formats["header"], formats["divider"]]
    sorted_apps = sorted(all_releases.items(), key=lambda item: item[1]["display_name"])
    for _, info in sorted_apps:
        if latest := info.get("latest_release"):
            lines.append(formats["line"].format(display_name=info["display_name"], asset_name=asset_name, version=latest["version"]))
    return "\n".join(lines)

def _generate_post_body(config: Dict[str, Any], changelog_data: Dict[str, Any], all_releases: Dict[str, Any], page_url: str) -> str:
    template_path = Path(paths.TEMPLATES_DIR) / config["reddit"]["templates"]["post"]
    raw_template = template_path.read_text()

    if start_tag := config.get("skipContent", {}).get("startTag"):
        raw_template = re.sub(f"{re.escape(start_tag)}.*?{re.escape(config['skipContent']['endTag'])}", "", raw_template, flags=re.DOTALL)

    placeholders = {
        "changelog": _generate_changelog(config, **changelog_data),
        "available_list": _generate_available_list(config, all_releases),
        "initial_status": config["feedback"]["statusLineFormat"].format(status=config["feedback"]["labels"]["unknown"]),
        "download_portal_url": page_url,
        **config["reddit"],
        **config["github"],
    }
    return cast(str, raw_template.strip().format(**placeholders))

def _post_new_release(reddit: praw.Reddit, title: str, body: str, config: Dict[str, Any]) -> praw.models.Submission:
    link_count = _count_outbound_links(body)
    warn_threshold = config.get("safety", {}).get("max_outbound_links_warn", 5)
    logging.info(f"Post analysis: Found {link_count} unique outbound link(s).")
    if link_count > MAX_OUTBOUND_LINKS_ERROR:
        logging.error(f"Post contains {link_count} links, exceeding safety limit of {MAX_OUTBOUND_LINKS_ERROR}. Aborting.")
        sys.exit(1)
    if link_count > warn_threshold:
        logging.warning(f"Post contains {link_count} links, which is above the warning threshold of {warn_threshold}.")

    logging.info(f"Submitting new post to r/{config['reddit']['subreddit']}: {title}")
    submission = reddit.subreddit(config["reddit"]["subreddit"])
    submission = submission.submit(title, selftext=body)
    logging.info(f"Post successful: {submission.shortlink}")
    return submission

def _get_version_changes(all_versions: Dict[str, Any], versions_to_check: Dict[str, str]) -> Dict[str, Any]:
    """Compares current versions with the latest versions and returns the changes."""
    added: Dict[str, Any] = {}
    updated: Dict[str, Any] = {}
    removed: Dict[str, Any] = {}
    new_versions = versions_to_check.copy()

    for app_id, data in all_versions.items():
        if not (latest := data.get("latest_release")):
            continue
        current_v = versions_to_check.get(app_id, "0.0.0")
        if parse_version(latest["version"]) > parse_version(current_v):
            new_versions[app_id] = latest["version"]
            if current_v == "0.0.0":
                added[app_id] = {"display_name": data["display_name"], "version": latest["version"], "url": latest["download_url"]}
            else:
                updated[app_id] = {"new": {"display_name": data["display_name"], "version": latest["version"], "url": latest["download_url"]}, "old": current_v}

    return {"added": added, "updated": updated, "removed": removed, "new_versions": new_versions}

def _handle_manual_post(title: str, body: str, new_versions: Dict[str, str], bot_state: Dict[str, Any]) -> None:
    """Handles the generation of post files for manual posting."""
    dist_dir = Path(paths.DIST_DIR)
    dist_dir.mkdir(exist_ok=True)
    (dist_dir / "post_title.txt").write_text(title)
    (dist_dir / "post_body.md").write_text(body)
    bot_state["offline"]["last_generated_versions"] = new_versions
    save_bot_state(bot_state)
    logging.info(f"Successfully generated post files in {dist_dir} and updated offline state.")

def _initialize_state() -> Dict[str, Any]:
    """Parses arguments and initializes the state."""
    parser = argparse.ArgumentParser(description="Post a new release to Reddit if it's out of date.")
    parser.add_argument("--page-url", default="", help="URL to the GitHub Pages landing page.")
    parser.add_argument("--generate-only", action="store_true", help="Generate post content without posting.")
    args = parser.parse_args()
    config = load_config()
    bot_state = load_bot_state()
    return {"args": args, "config": config, "bot_state": bot_state}

def _create_and_submit_post(config: Dict[str, Any], bot_state: Dict[str, Any], version_changes: Dict[str, Any], all_versions: Dict[str, Any], page_url: str) -> None:
    """Creates the post content and submits it to Reddit."""
    changelog_data = {k: v for k, v in version_changes.items() if k in ["added", "updated", "removed"]}
    title = _generate_dynamic_title(config, added=changelog_data["added"], updated=changelog_data["updated"])
    body = _generate_post_body(config, changelog_data, all_versions, page_url)

    is_manual = config["reddit"].get("post_manually", False)
    if is_manual:
        _handle_manual_post(title, body, version_changes["new_versions"], bot_state)
        sys.exit(0)

    reddit = init_reddit(config)
    new_submission = _post_new_release(reddit, title, body, config)
    if existing_posts := get_bot_posts(reddit, config):
        update_older_posts(existing_posts, {"title": new_submission.title, "url": new_submission.shortlink, "version": "latest"}, config)

    bot_state["online"].update({"last_posted_versions": version_changes["new_versions"], "activePostId": new_submission.id})
    save_bot_state(bot_state)
    logging.info("Post and update process complete. Online state updated.")

def main() -> None:
    state = _initialize_state()
    args, config, bot_state = state["args"], state["config"], state["bot_state"]

    releases_path = Path(paths.RELEASES_JSON_FILE)
    if not releases_path.exists():
        logging.info(f"`{releases_path}` not found. Nothing to post.")
        sys.exit(0)

    all_versions = json.loads(releases_path.read_text())
    versions_to_check = bot_state["offline" if args.generate_only else "online"]["last_generated_versions" if args.generate_only else "last_posted_versions"]

    version_changes = _get_version_changes(all_versions, versions_to_check)
    if not any([version_changes["added"], version_changes["updated"], version_changes["removed"]]):
        logging.info("No changes detected. State is up-to-date.")
        sys.exit(0)

    page_url = args.page_url or config.get("github", {}).get("pages_url", "")
    _create_and_submit_post(config, bot_state, version_changes, all_versions, page_url)

if __name__ == "__main__":
    main()
