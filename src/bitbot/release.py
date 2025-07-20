"""This module handles checking for new releases."""

import re
from typing import Optional

from .data.models import AppConfig
from .interfaces.config_protocol import ConfigManagerProtocol
from .interfaces.github_protocol import GitHubManagerProtocol
from .interfaces.reddit_protocol import RedditManagerProtocol
from .interfaces.state_protocol import StateManagerProtocol
from .logging import get_logger

logger = get_logger(__name__)


def _parse_version_from_description(description: str, app_name: str) -> Optional[str]:
    """Parse the version from a release description."""
    match = re.search(rf"For {app_name} v(\d+\.\d+\.\d+)", description)
    return match.group(1) if match else None


async def check_new_release(
    config_manager: ConfigManagerProtocol,
    state_manager: StateManagerProtocol,
    github_manager: GitHubManagerProtocol,
    reddit_manager: RedditManagerProtocol,
) -> None:
    """Check for new releases and post them to Reddit."""
    config = await config_manager.load_config()
    state = await state_manager.load_state()

    latest_release = await github_manager.get_latest_release(config.github.sourceRepo)
    if not latest_release:
        logger.info("No new releases found.")
        return

    if not state.activePostId:
        logger.info("No active post ID in state file. Submitting a new post.")
        # This will be handled by the history module, but we should consider
        # what to do here. For now, we'll just log it.
        return

    current_post = await reddit_manager.get_post_by_id(state.activePostId)
    if not current_post:
        logger.warning("Could not find the active post on Reddit.")
        return

    for app in config.apps:
        app_config = AppConfig(**app)
        latest_version = _parse_version_from_description(
            latest_release.body, app_config.displayName
        )
        if not latest_version:
            continue

        current_version = _parse_version_from_description(
            current_post.body, app_config.displayName
        )

        if latest_version > (current_version or "0.0.0"):
            logger.info(
                "New version found for %s: %s", app_config.displayName, latest_version
            )
            # This will be handled by the history module.
            return
