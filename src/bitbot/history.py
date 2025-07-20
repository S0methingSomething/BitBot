"""This module handles the synchronization of Reddit post history."""

import os
import re
from pathlib import Path
from typing import Dict, List

from .data.models import AppConfig, BotState, Config, GitHubRelease, RedditPost
from .interfaces.config_protocol import ConfigManagerProtocol
from .interfaces.github_protocol import GitHubManagerProtocol
from .interfaces.reddit_protocol import RedditManagerProtocol
from .interfaces.state_protocol import StateManagerProtocol
from .interfaces.template_protocol import TemplateManagerProtocol
from .logging import get_logger

logger = get_logger(__name__)


def _parse_version_from_title(title: str) -> str:
    """Parse the version from a post title."""
    match = re.search(r"v(\d+\.\d+\.\d+)", title)
    return match.group(1) if match else "0.0.0"


async def _update_older_posts(
    reddit_manager: RedditManagerProtocol,
    template_manager: TemplateManagerProtocol,
    older_posts: List[RedditPost],
    latest_release_details: Dict[str, str],
    config: Config,
) -> None:
    """Update older posts with a banner pointing to the latest release."""
    # This function will need to be updated to handle the new placeholder system.
    # For now, we will leave it as is.
    pass


async def _update_bot_state(
    state_manager: StateManagerProtocol, post_id: str, config: Config
) -> None:
    """Update the bot's state file."""
    new_state = BotState(
        activePostId=post_id,
        lastCheckTimestamp="2024-01-01T00:00:00Z",
        currentIntervalSeconds=config.timing.firstCheck,
        lastCommentCount=0,
    )
    await state_manager.save_state(new_state)
    logger.info("State file updated. Now monitoring post: %s", post_id)
    github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
    with Path(github_output).open("a") as f:
        f.write("state_changed=true")


async def _post_new_release(
    reddit_manager: RedditManagerProtocol,
    template_manager: TemplateManagerProtocol,
    release: GitHubRelease,
    config: Config,
) -> RedditPost:
    """Post a new release to Reddit."""
    raw_template = await template_manager.get_template(config.reddit.templateFile)

    # This is where the magic happens. We will iterate through the apps and
    # replace the placeholders.
    post_body = raw_template
    for app_data in config.apps:
        app = AppConfig(**app_data)
        asset = next((a for a in release.assets if a["name"] == app.assetName), None)
        if not asset:
            continue

        post_body = post_body.replace(f"{{{{{app.id}_display_name}}}}", app.displayName)
        post_body = post_body.replace(f"{{{{{app.id}_asset_name}}}}", app.assetName)
        post_body = post_body.replace(
            f"{{{{{app.id}_download_url}}}}", asset["browser_download_url"]
        )

    # Replace the general placeholders
    post_body = post_body.replace("{{version}}", release.version)
    post_body = post_body.replace("{{bot_name}}", config.reddit.botName)
    post_body = post_body.replace("{{bot_repo}}", config.github.botRepo)
    post_body = post_body.replace("{{creator_username}}", config.reddit.creator)
    post_body = post_body.replace(
        "{{initial_status}}",
        config.feedback.statusLineFormat.replace(
            "{{status}}", config.feedback.labels.unknown
        ),
    )

    title = config.reddit.postTitle.replace("{{version}}", release.version)

    logger.info(
        "Submitting new post for v%s to r/%s...",
        release.version,
        config.reddit.subreddit,
    )
    submission = await reddit_manager.submit_post(title, post_body)
    logger.info("Post successful: %s", submission.url)
    return submission


async def sync_history(
    config_manager: ConfigManagerProtocol,
    state_manager: StateManagerProtocol,
    github_manager: GitHubManagerProtocol,
    reddit_manager: RedditManagerProtocol,
    template_manager: TemplateManagerProtocol,
) -> None:
    """Sync the Reddit post history with the latest GitHub release."""
    config = await config_manager.load_config()
    state = await state_manager.load_state()

    latest_release = await github_manager.get_latest_release(config.github.sourceRepo)
    if not latest_release:
        logger.info("No new releases found.")
        return

    if not state.activePostId:
        logger.info("No active post ID in state file. Submitting a new post.")
        new_submission = await _post_new_release(
            reddit_manager, template_manager, latest_release, config
        )
        await _update_bot_state(state_manager, new_submission.id, config)
        return

    current_post = await reddit_manager.get_post_by_id(state.activePostId)
    if not current_post:
        logger.warning("Could not find the active post on Reddit.")
        return

    latest_version = _parse_version_from_title(latest_release.version)
    current_version = _parse_version_from_title(current_post.title)

    if latest_version > current_version:
        logger.info(
            "Reddit is out of sync (Reddit: v%s, GitHub: v%s). Posting update.",
            current_version,
            latest_version,
        )
        new_submission = await _post_new_release(
            reddit_manager, template_manager, latest_release, config
        )
        await _update_bot_state(state_manager, new_submission.id, config)
    elif latest_release.body != current_post.body:
        logger.info("Release description has changed. Updating post.")
        # This is where we would update the existing post. For now, we will
        # just log it.
        pass
