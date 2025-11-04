"""Reddit post management."""

import re
from pathlib import Path
from typing import Any

import deal
import praw
import praw.models
from beartype import beartype

from bitbot import paths
from bitbot.config_models import Config
from bitbot.core.error_logger import get_logger
from bitbot.core.errors import RedditAPIError
from bitbot.core.result import Err, Ok, Result
from bitbot.core.state import load_bot_state, save_bot_state

logger = get_logger()


@deal.pre(lambda reddit, config: reddit is not None)
@deal.pre(lambda reddit, config: isinstance(config, Config))
@beartype
def get_bot_posts(
    reddit: praw.Reddit, config: Config
) -> Result[list[praw.models.Submission], RedditAPIError]:
    """Fetches all of the bot's release posts from the configured subreddit.

    Uses hybrid detection:
    1. Primary: Check if post.id in bot_state["allPostIds"]
    2. Fallback: Check author == bot_user AND title.startswith(config identifier)
    3. Self-healing: Add discovered posts to state
    """
    try:
        bot_user = reddit.user.me()
        target_subreddit = config.reddit.subreddit.lower()
        post_identifier = "[BitBot]"  # Default identifier

        # Load state for post ID tracking
        state_result = load_bot_state()
        known_post_ids = set(state_result.unwrap().all_post_ids) if state_result.is_ok() else set()

        posts = []
        newly_discovered_ids = []

        for submission in bot_user.submissions.new(limit=100):
            if submission.subreddit.display_name.lower() != target_subreddit:
                continue

            # Primary detection: known post ID
            if submission.id in known_post_ids:
                posts.append(submission)
                continue

            # Fallback detection: title starts with identifier
            if submission.title.startswith(post_identifier):
                posts.append(submission)
                newly_discovered_ids.append(submission.id)

        # Self-healing: save newly discovered post IDs
        if newly_discovered_ids and state_result.is_ok():
            state = state_result.unwrap()
            state.all_post_ids.extend(newly_discovered_ids)
            save_bot_state(state)

        return Ok(posts)
    except Exception as e:
        return Err(RedditAPIError(f"Failed to fetch bot posts: {e}"))


@deal.pre(lambda older_posts, latest_release_details, config: isinstance(older_posts, list))
@deal.pre(
    lambda older_posts, latest_release_details, config: isinstance(latest_release_details, dict)
)
@deal.pre(lambda older_posts, latest_release_details, config: isinstance(config, Config))
@beartype
def update_older_posts(
    older_posts: list[praw.models.Submission],
    latest_release_details: dict[str, Any],
    config: Config,
) -> Result[None, RedditAPIError]:
    """Updates older posts by injecting an 'outdated' banner."""
    try:
        mode = config.outdated_post_handling.get("mode", "overwrite")

        placeholders = {
            "{{latest_post_title}}": latest_release_details["title"],
            "{{latest_post_url}}": latest_release_details["url"],
            "{{latest_version}}": latest_release_details["version"],
            "{{asset_name}}": config.github.asset_file_name,
            "{{bot_name}}": config.reddit.bot_name,
        }

        raw_template = ""
        if mode == "inject":
            template_name = config.reddit.templates.inject_banner
            if not template_name:
                return Ok(None)

            template_path = paths.get_template_path(Path(template_name).name)

            try:
                with Path(template_path).open() as f:
                    raw_template = f.read()
            except FileNotFoundError:
                return Ok(None)

        ignore_block = config.skip_content
        start_marker, end_marker = ignore_block.get("startTag"), ignore_block.get("endTag")
        if start_marker and end_marker and start_marker in raw_template:
            pattern = re.compile(f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
            banner_template = re.sub(pattern, "", raw_template).strip()
        else:
            banner_template = raw_template

        injection_banner = banner_template
        for placeholder, value in placeholders.items():
            injection_banner = injection_banner.replace(placeholder, str(value))

        updated_count = 0
        existence_check_string = "## ⚠️ Outdated Post"

        for old_post in older_posts:
            original_body = old_post.selftext
            new_body = ""

            try:
                if existence_check_string in original_body:
                    pattern = re.compile(
                        f"^{re.escape(existence_check_string)}.*?---", re.DOTALL | re.MULTILINE
                    )
                    new_body = pattern.sub(f"{injection_banner}\n\n---", original_body, 1)
                else:
                    new_body = f"{injection_banner}\n\n---\n\n{original_body}"

                if new_body.strip() and new_body != original_body:
                    old_post.edit(body=new_body)
                    updated_count += 1
            except Exception as e:
                logger.warning("Failed to update post %s: %s", old_post.id, e)
                continue

        return Ok(None)
    except Exception as e:
        return Err(RedditAPIError(f"Failed to update older posts: {e}"))
