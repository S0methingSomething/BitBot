"""Reddit post management."""

import re
from pathlib import Path
from typing import Any

import deal
import praw
import praw.models
from beartype import beartype

import paths
from core.errors import RedditAPIError
from core.result import Err, Ok, Result
from core.retry import retry


@deal.pre(lambda reddit, config: reddit is not None)  # type: ignore[misc]
@deal.pre(lambda reddit, config: isinstance(config, dict))  # type: ignore[misc]
@beartype  # type: ignore[misc]
@retry(max_attempts=3, on=[RedditAPIError])
def get_bot_posts(
    reddit: praw.Reddit, config: dict[str, Any]
) -> Result[list[praw.models.Submission], RedditAPIError]:
    """Fetches all of the bot's release posts from the configured subreddit."""
    try:
        bot_user = reddit.user.me()
        target_subreddit = config["reddit"]["subreddit"].lower()
        post_identifier = "[BitBot] MonetizationVars"

        posts = [
            submission
            for submission in bot_user.submissions.new(limit=100)
            if (
                submission.subreddit.display_name.lower() == target_subreddit
                and submission.title.startswith(post_identifier)
            )
        ]
        return Ok(posts)
    except Exception as e:
        return Err(RedditAPIError(f"Failed to fetch bot posts: {e}"))


@deal.pre(lambda older_posts, latest_release_details, config: isinstance(older_posts, list))  # type: ignore[misc]
@deal.pre(lambda older_posts, latest_release_details, config: isinstance(latest_release_details, dict))  # type: ignore[misc]
@deal.pre(lambda older_posts, latest_release_details, config: isinstance(config, dict))  # type: ignore[misc]
@beartype  # type: ignore[misc]
@retry(max_attempts=3, on=[RedditAPIError])
def update_older_posts(  # noqa: C901
    older_posts: list[praw.models.Submission],
    latest_release_details: dict[str, Any],
    config: dict[str, Any],
) -> Result[None, RedditAPIError]:
    """Updates older posts by injecting an 'outdated' banner."""
    try:
        handling_config = config.get("outdatedPostHandling", {})
        mode = handling_config.get("mode", "overwrite")

        placeholders = {
            "{{latest_post_title}}": latest_release_details["title"],
            "{{latest_post_url}}": latest_release_details["url"],
            "{{latest_version}}": latest_release_details["version"],
            "{{asset_name}}": config["github"]["assetFileName"],
            "{{bot_name}}": config["reddit"]["botName"],
        }

        if mode == "inject":
            template_name = config["reddit"]["templates"].get("inject_banner")
            if not template_name:
                return Ok(None)

            template_path = paths.get_template_path(Path(template_name).name)

            try:
                with Path(template_path).open() as f:
                    raw_template = f.read()
            except FileNotFoundError:
                return Ok(None)

        ignore_block = config.get("skipContent", {})
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
            except Exception:  # noqa: BLE001, S110
                pass
        
        return Ok(None)
    except Exception as e:
        return Err(RedditAPIError(f"Failed to update older posts: {e}"))
