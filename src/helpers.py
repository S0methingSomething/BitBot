import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, cast

import praw
import toml

import paths
from logging_config import get_logger

logging = get_logger(__name__)

# --- Configuration and State Management ---

def load_config() -> Dict[str, Any]:
    """Loads the main configuration file (config.toml)."""
    try:
        return toml.loads(Path(paths.CONFIG_FILE).read_text())
    except FileNotFoundError:
        logging.error(f"`{paths.CONFIG_FILE}` not found. Please ensure the file exists.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Failed to parse `{paths.CONFIG_FILE}`: {e}")
        sys.exit(1)

def load_bot_state() -> Dict[str, Any]:
    """Loads the bot's state, ensuring the nested structure exists."""
    try:
        state: Dict[str, Any] = json.loads(Path(paths.BOT_STATE_FILE).read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        state = {}
    # Ensure nested structure for robustness
    state.setdefault("online", {}).setdefault("last_posted_versions", {})
    state.setdefault("offline", {}).setdefault("last_generated_versions", {})
    return state

def save_bot_state(data: Dict[str, Any]) -> None:
    """Saves the bot's monitoring state."""
    Path(paths.BOT_STATE_FILE).write_text(json.dumps(data, indent=2))

def load_release_state() -> List[int]:
    """Loads the list of processed source release IDs."""
    try:
        return cast(List[int], json.loads(Path(paths.RELEASE_STATE_FILE).read_text()))
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_release_state(data: List[int]) -> None:
    """Saves the list of processed source release IDs."""
    Path(paths.RELEASE_STATE_FILE).write_text(json.dumps(data, indent=2))

def _parse_structured_format(body: str, app_map: Dict[str, str]) -> Optional[Dict[str, str]]:
    """Parses the new structured format from the release body."""
    app_match = re.search(r"^app:\s*(\S+)", body, re.MULTILINE)
    version_match = re.search(r"^version:\s*([\d\.]+)", body, re.MULTILINE)
    asset_match = re.search(r"^asset_name:\s*(\S+)", body, re.MULTILINE)
    if app_match and version_match and asset_match:
        app_id = app_match.group(1)
        if app_id in app_map:
            return {"app_id": app_id, "display_name": app_map[app_id], "version": version_match.group(1), "asset_name": asset_match.group(1)}
    return None

def _parse_legacy_formats(tag_name: str, title: str, app_map: Dict[str, str], asset_file: str) -> Optional[Dict[str, str]]:
    """Parses legacy formats from the tag name or title."""
    for app_id, display_name in app_map.items():
        if tag_name.lower().startswith(f"{app_id.lower()}-v"):
            version = tag_name.split("-v")[-1]
            return {"app_id": app_id, "display_name": display_name, "version": version, "asset_name": asset_file}
        match = re.search(rf"{re.escape(display_name)}.*?v([\d\.]+)", title, re.IGNORECASE)
        if match:
            return {"app_id": app_id, "display_name": display_name, "version": match.group(1), "asset_name": asset_file}
    return None

def parse_release_notes(body: str, tag_name: str, title: str, config: Dict[str, Any]) -> Optional[Dict[str, str]]:
    """Parses release info from body, tag, or title to support legacy formats."""
    app_map = {app["id"]: app["displayName"] for app in config.get("apps", [])}
    asset_file = config["github"]["assetFileName"]

    if structured_result := _parse_structured_format(body, app_map):
        return structured_result
    if legacy_result := _parse_legacy_formats(tag_name, title, app_map, asset_file):
        return legacy_result

    if "bitlife" in app_map and (match := re.search(r"([\d\.]+)", tag_name)):
        return {"app_id": "bitlife", "display_name": "BitLife", "version": match.group(1), "asset_name": asset_file}

    return None

def parse_versions_from_post(post: praw.models.Submission, config: Dict[str, Any]) -> Dict[str, str]:
    """Parses app versions from a Reddit post, supporting multiple formats."""
    versions: Dict[str, str] = {}
    app_map = {app["displayName"].lower(): app["id"] for app in config.get("apps", [])}

    # --- New Format: Changelog ---
    if changelog_match := re.search(r"## Changelog\n(.+)", post.selftext, re.DOTALL):
        for line in changelog_match.group(1).splitlines():
            for name, app_id in app_map.items():
                if match := re.search(rf"{re.escape(name)}.*?to version ([\d\.]+)", line, re.IGNORECASE):
                    versions[app_id] = match.group(1)
                    break
    # --- Legacy Format: Title ---
    if not versions:
        for name, app_id in app_map.items():
            if match := re.search(rf"for {re.escape(name)} v([\d\.]+)", post.title, re.IGNORECASE):
                versions[app_id] = match.group(1)
                break
    return versions

# --- Reddit Client and Post Management ---

def init_reddit(config: Dict[str, Any]) -> praw.Reddit:
    """Initializes and returns a PRAW Reddit instance."""
    return praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
        validate_on_submit=True,
    )

def get_bot_posts(reddit: praw.Reddit, config: Dict[str, Any]) -> List[praw.models.Submission]:
    """Fetches all of the bot's release posts from the configured subreddit."""
    bot_user = reddit.user.me()
    subreddit = config["reddit"]["subreddit"].lower()
    identifier = "[BitBot] MonetizationVars"
    return [p for p in bot_user.submissions.new(limit=100) if p.subreddit.display_name.lower() == subreddit and p.title.startswith(identifier)]

def _create_banner(template_path: Path, latest_details: Dict[str, Any], config: Dict[str, Any]) -> str:
    """Creates the banner to inject into older posts."""
    raw_template = template_path.read_text()
    start_tag, end_tag = config.get("skipContent", {}).get("startTag"), config.get("skipContent", {}).get("endTag")
    if start_tag and end_tag and start_tag in raw_template:
        raw_template = re.sub(f"{re.escape(start_tag)}.*?{re.escape(end_tag)}", "", raw_template, flags=re.DOTALL)
    return raw_template.strip().format(**latest_details)

def _inject_banner_into_post(post: praw.models.Submission, banner: str) -> None:
    """Injects the banner into a single post."""
    existence_check = "## ⚠️ Outdated Post"
    try:
        if existence_check in post.selftext:
            pattern = re.compile(f"^{re.escape(existence_check)}.*?---", re.DOTALL | re.MULTILINE)
            new_body = pattern.sub(f"{banner}\n\n---", post.selftext, 1)
        else:
            new_body = f"{banner}\n\n---\n\n{post.selftext}"
        if new_body != post.selftext:
            post.edit(body=new_body)
    except Exception as e:
        logging.warning(f"Failed to update banner in post {post.id}: {e}")

def update_older_posts(older_posts: List[praw.models.Submission], latest_details: Dict[str, Any], config: Dict[str, Any]) -> None:
    """Updates older posts by injecting an 'outdated' banner."""
    mode = config.get("outdatedPostHandling", {}).get("mode", "inject")
    if mode != "inject":
        return

    template_name = config["reddit"]["templates"].get("inject_banner")
    if not template_name:
        logging.error("'inject' mode is enabled, but 'inject_banner' template is not defined.")
        return

    try:
        template_path = Path(paths.TEMPLATES_DIR) / Path(template_name).name
        banner = _create_banner(template_path, latest_details, config)
        for post in older_posts:
            _inject_banner_into_post(post, banner)
    except FileNotFoundError:
        logging.error(f"Inject template not found at '{template_path}'.")
        return

