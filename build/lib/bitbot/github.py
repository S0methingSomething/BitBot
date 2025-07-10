import os
from typing import Any, Dict, Optional

import requests

from .logging import get_logger

logger = get_logger(__name__)


def get_latest_release(config: Dict[str, Any]) -> Optional[Dict[str, str]]:
    """
    Fetches the latest release from the bot's own GitHub repo, which serves
    as the ultimate source of truth for what version is "current".
    """
    bot_repo = config["github"]["botRepo"]
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    api_url = f"https://api.github.com/repos/{bot_repo}/releases/latest"

    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
        release_data = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(
            f"Could not fetch latest release from {bot_repo}: {e}", exc_info=True
        )
        return None

    version = release_data.get("tag_name", "").lstrip("v")
    asset = next(
        (
            a
            for a in release_data.get("assets", [])
            if a["name"] == config["github"]["assetFileName"]
        ),
        None,
    )

    if not version or not asset:
        logger.error(
            "Could not find a valid version and asset in the latest bot release."
        )
        return None

    return {"version": version, "url": asset["browser_download_url"]}
