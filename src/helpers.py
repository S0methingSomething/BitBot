import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, cast
from unittest.mock import MagicMock

import praw

import paths
from dry_run import (
    is_dry_run,
)
from io_handler import IOHandler
from logging_config import get_logger

logging = get_logger(__name__)

# --- Dry Run Utilities ---
# NOTE: is_dry_run() is now imported from dry_run.py
# Use is_dry_run() instead of checking os.environ directly


def run_command_dry(
    command: list[str], check: bool = True  # noqa: ARG001
) -> subprocess.CompletedProcess[str]:
    """Simulates running a shell command in dry-run mode."""
    logging.info(f"DRY_RUN: Would execute: {' '.join(command)}")
    # Return a mock result
    result: subprocess.CompletedProcess[str] = subprocess.CompletedProcess(
        args=command, returncode=0, stdout="", stderr=""
    )
    return result


# --- Configuration and State Management ---


def load_bot_state() -> dict[str, Any]:
    """Loads the bot's state, ensuring the nested structure exists."""
    state = IOHandler.load_bot_state()
    return cast(dict[str, Any], state)


def save_bot_state(data: dict[str, Any]) -> None:
    """Saves the bot's monitoring state."""
    IOHandler.save_bot_state(data)


def load_release_state() -> list[int]:
    """Loads the list of processed source release IDs."""
    state = IOHandler.load_release_state()
    return cast(list[int], state)


def save_release_state(data: list[int]) -> None:
    """Saves the list of processed source release IDs."""
    IOHandler.save_release_state(data)


def _parse_structured_format(
    body: str, app_map: dict[str, str]
) -> dict[str, str] | None:
    """Parses the new structured format from the release body."""
    app_match = re.search(r"^app:\s*(\S+)", body, re.MULTILINE)
    version_match = re.search(r"^version:\s*([\d\.]+)", body, re.MULTILINE)
    asset_match = re.search(r"^asset_name:\s*(\S+)", body, re.MULTILINE)
    if app_match and version_match and asset_match:
        app_id = app_match.group(1)
        if app_id in app_map:
            return {
                "app_id": app_id,
                "display_name": app_map[app_id],
                "version": version_match.group(1),
                "asset_name": asset_match.group(1),
            }
    return None


def _parse_legacy_formats(
    tag_name: str, title: str, app_map: dict[str, str], asset_file: str
) -> dict[str, str] | None:
    """Parses legacy formats from the tag name or title."""
    for app_id, display_name in app_map.items():
        if tag_name.lower().startswith(f"{app_id.lower()}-v"):
            version = tag_name.split("-v")[-1]
            return {
                "app_id": app_id,
                "display_name": display_name,
                "version": version,
                "asset_name": asset_file,
            }
        match = re.search(
            rf"{re.escape(display_name)}.*?v([\d\.]+)", title, re.IGNORECASE
        )
        if match:
            return {
                "app_id": app_id,
                "display_name": display_name,
                "version": match.group(1),
                "asset_name": asset_file,
            }
    return None


def _extract_app_map(config: Any) -> dict[str, str]:
    """Extract app map from config, handling both dict and Pydantic model configs."""
    # Handle both dict and Pydantic model configs
    if hasattr(config, "apps"):
        # Pydantic model
        return {app.id: app.display_name for app in config.apps}
    # Dict format - handle both old and new key formats
    apps = config.get("apps", [])
    # Convert apps to use correct keys if needed
    if apps and isinstance(apps[0], dict):
        if "display_name" in apps[0]:
            # New format
            return {app["id"]: app["display_name"] for app in apps}
        # Old format with displayName
        return {app["id"]: app["displayName"] for app in apps}
    return {}


def _extract_asset_file(config: Any) -> str:
    """Extract asset file name from config, handling both dict and Pydantic model configs."""
    # Handle both dict and Pydantic model configs
    if hasattr(config, "github"):
        # Pydantic model
        return str(config.github.asset_file_name)
    # Dict format - handle both old and new key formats
    github_config = config.get("github", {})
    if "asset_file_name" in github_config:
        # New format
        return str(github_config["asset_file_name"])
    # Old format with assetFileName
    return str(github_config.get("assetFileName", ""))


def parse_release_notes(
    body: str, tag_name: str, title: str, config: Any
) -> dict[str, str] | None:
    """Parses release info from body, tag, or title to support legacy formats."""
    app_map = _extract_app_map(config)
    asset_file = _extract_asset_file(config)

    if structured_result := _parse_structured_format(body, app_map):
        return structured_result
    if legacy_result := _parse_legacy_formats(tag_name, title, app_map, asset_file):
        return legacy_result

    if "bitlife" in app_map and (match := re.search(r"([\d\.]+)", tag_name)):
        return {
            "app_id": "bitlife",
            "display_name": "BitLife",
            "version": match.group(1),
            "asset_name": asset_file,
        }

    return None


def _extract_app_map_for_versions(config: Any) -> dict[str, str]:
    """Extract app map for version parsing from config, handling both dict and Pydantic model configs."""
    # Handle both dict and Pydantic model configs
    if hasattr(config, "apps"):
        # Pydantic model
        return {app.display_name.lower(): app.id for app in config.apps}
    # Dict format - handle both old and new key formats
    apps = config.get("apps", [])
    # Convert apps to use correct keys if needed
    if apps and isinstance(apps[0], dict):
        if "display_name" in apps[0]:
            # New format
            return {app["display_name"].lower(): app["id"] for app in apps}
        # Old format with displayName
        return {app["displayName"].lower(): app["id"] for app in apps}
    return {}


def _parse_changelog_versions(
    post: praw.models.Submission, app_map: dict[str, str]
) -> dict[str, str]:
    """Parse versions from changelog format."""
    versions: dict[str, str] = {}
    if changelog_match := re.search(r"## Changelog\n(.+)", post.selftext, re.DOTALL):
        for line in changelog_match.group(1).splitlines():
            for name, app_id in app_map.items():
                if match := re.search(
                    rf"{re.escape(name)}.*?to version ([\d\.]+)", line, re.IGNORECASE
                ):
                    versions[app_id] = match.group(1)
                    break
    return versions


def _parse_title_versions(
    post: praw.models.Submission, app_map: dict[str, str]
) -> dict[str, str]:
    """Parse versions from title format."""
    versions: dict[str, str] = {}
    for name, app_id in app_map.items():
        if match := re.search(
            rf"for {re.escape(name)} v([\d\.]+)", post.title, re.IGNORECASE
        ):
            versions[app_id] = match.group(1)
            break
    return versions


def parse_versions_from_post(
    post: praw.models.Submission, config: Any
) -> dict[str, str]:
    """Parses app versions from a Reddit post, supporting multiple formats."""
    versions: dict[str, str] = {}
    app_map = _extract_app_map_for_versions(config)

    # --- New Format: Changelog ---
    versions = _parse_changelog_versions(post, app_map)

    # --- Legacy Format: Title ---
    if not versions:
        versions = _parse_title_versions(post, app_map)

    return versions


# --- Reddit Client and Post Management ---


def init_reddit(config: Any) -> praw.Reddit | MagicMock:  # noqa: ARG001
    """Initializes and returns a PRAW Reddit instance, or a mock if DRY_RUN is enabled."""
    if is_dry_run():
        logging.info("DRY_RUN: Initializing mock Reddit client.")
        mock_submission = MagicMock()
        mock_submission.id = "mock-post-id-dry-run"
        mock_submission.title = "Mock Post Title"
        mock_submission.shortlink = "https://dry-run.reddit.post/mock-post-id"

        mock_reddit = MagicMock()
        mock_reddit.user.me().submissions.new.return_value = []
        mock_reddit.subreddit.return_value.submit.return_value = mock_submission
        return mock_reddit
    
    # Check if all required Reddit credentials are available
    required_vars = ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USERNAME", "REDDIT_PASSWORD", "REDDIT_USER_AGENT"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        raise ValueError(f"Missing required Reddit credentials: {', '.join(missing_vars)}. Please check your credentials.toml file.")
    
    return praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
        validate_on_submit=True,
    )


def get_bot_posts(reddit: praw.Reddit, config: Any) -> list[praw.models.Submission]:
    """Fetches all of the bot's release posts from the configured subreddit."""
    bot_user = reddit.user.me()
    subreddit = config.reddit.subreddit.lower()
    identifier = "[BitBot] MonetizationVars"
    return [
        p
        for p in bot_user.submissions.new(limit=100)
        if p.subreddit.display_name.lower() == subreddit
        and p.title.startswith(identifier)
    ]


def _create_banner(
    template_path: Path, latest_details: dict[str, Any], config: Any
) -> str:
    """Creates the banner to inject into older posts."""
    raw_template = template_path.read_text()
    start_tag, end_tag = (
        config.get("skip_content", {}).get("start_tag"),
        config.get("skip_content", {}).get("end_tag"),
    )
    if start_tag and end_tag and start_tag in raw_template:
        raw_template = re.sub(
            f"{re.escape(start_tag)}.*?{re.escape(end_tag)}",
            "",
            raw_template,
            flags=re.DOTALL,
        )
    return raw_template.strip().format(**latest_details)


def _inject_banner_into_post(post: praw.models.Submission, banner: str) -> None:
    """Injects the banner into a single post."""
    existence_check = "## ⚠️ Outdated Post"
    try:
        if existence_check in post.selftext:
            pattern = re.compile(
                f"^{re.escape(existence_check)}.*?---", re.DOTALL | re.MULTILINE
            )
            new_body = pattern.sub(f"{banner}\n\n---", post.selftext, 1)
        else:
            new_body = f"{banner}\n\n---\n\n{post.selftext}"
        if new_body != post.selftext:
            post.edit(body=new_body)
    except Exception as e:
        logging.warning(f"Failed to update banner in post {post.id}: {e}")


def update_older_posts(
    older_posts: list[praw.models.Submission],
    latest_details: dict[str, Any],
    config: Any,
) -> None:
    """Updates older posts by injecting an 'outdated' banner."""
    mode = config.get("outdatedPostHandling", {}).get("mode", "inject")
    if mode != "inject":
        return

    template_name = config.reddit.templates.inject_banner
    if not template_name:
        logging.error(
            "'inject' mode is enabled, but 'inject_banner' template is not defined."
        )
        return

    try:
        template_path = Path(paths.TEMPLATES_DIR) / Path(template_name).name
        banner = _create_banner(template_path, latest_details, config)
        for post in older_posts:
            _inject_banner_into_post(post, banner)
    except FileNotFoundError:
        logging.error(f"Inject template not found at '{template_path}'.")
        return


# --- Common Utility Functions ---


def run_command(
    command: list[str], check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a shell command."""
    if is_dry_run():
        return run_command_dry(command, check=check)

    logging.info(f"Executing: {' '.join(command)}")
    return subprocess.run(command, capture_output=True, text=True, check=check)


def get_github_data(url: str) -> Any:
    """Fetch data from GitHub API."""
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token and not is_dry_run():
        raise ValueError("GitHub token is required but not available")

    result = run_command(["gh", "api", "-H", f"Authorization: token {token}", url])
    return json.loads(result.stdout)


def save_json_data(data: Any, file_path: Path) -> None:
    """Save data as JSON to file."""
    file_path.parent.mkdir(exist_ok=True)
    file_path.write_text(json.dumps(data, indent=2))


def load_json_data(file_path: Path) -> Any:
    """Load data from JSON file."""
    try:
        if file_path.exists():
            return json.loads(file_path.read_text())
        return {}
    except (OSError, json.JSONDecodeError) as e:
        logging.warning(f"Could not load data from {file_path}: {e}")
        return {}
