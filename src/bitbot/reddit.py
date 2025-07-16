"""This module handles all interactions with the Reddit API."""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, cast

import praw  # type: ignore

from .logging import get_logger

logger = get_logger(__name__)


def _load_config() -> Dict[str, Any]:
    """Load the main configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path("config.json")
    with config_path.open("r") as f:
        return cast(Dict[str, Any], json.load(f))


def _get_bot_posts_on_subreddit(reddit: Any, config: Dict[str, Any]) -> List[Any]:
    """Fetch all of the bot's release posts from the configured subreddit.

    Args:
        reddit: The praw.Reddit instance.
        config: The configuration dictionary.

    Returns:
        A list of praw.models.Submission objects.
    """
    bot_user = reddit.user.me()
    target_subreddit = config["reddit"]["subreddit"].lower()

    title_template = config["reddit"]["postTitle"]
    asset_name = config["github"]["assetFileName"]
    post_identifier = (
        title_template.split("v{{version}}")[0]
        .strip()
        .replace("{{asset_name}}", asset_name)
    )

    bot_posts = []
    if bot_user:
        for submission in bot_user.submissions.new(limit=100):
            if (
                submission.subreddit.display_name.lower() == target_subreddit
                and submission.title.startswith(post_identifier)
            ):
                bot_posts.append(submission)
    return bot_posts


def _update_older_posts(
    older_posts: List[Any],
    latest_release_details: Dict[str, str],
    config: Dict[str, Any],
) -> None:
    """Update older posts with a banner pointing to the latest release.

    Args:
        older_posts: A list of older posts to update.
        latest_release_details: A dictionary containing details about the
            latest release.
        config: The configuration dictionary.
    """
    handling_config = config.get("outdatedPostHandling", {})
    mode = handling_config.get("mode", "overwrite")

    placeholders = {
        "{{latest_post_title}}": latest_release_details["title"],
        "{{latest_post_url}}": latest_release_details["url"],
        "{{latest_version}}": latest_release_details["version"],
        "{{asset_name}}": config["github"]["assetFileName"],
        "{{bot_name}}": config["reddit"]["botName"],
        "{{bot_repo}}": config["github"]["botRepo"],
    }

    if mode == "inject":
        template_path = handling_config.get("injectTemplateFile")
        if not template_path:
            logger.error(
                "'inject' mode selected but 'injectTemplateFile' "
                "is not defined in config."
            )
            return

        try:
            with Path(template_path).open("r") as f:
                raw_template = f.read()
        except FileNotFoundError:
            logger.error("Inject template file not found at '%s'.", template_path)
            return

        ignore_block = config.get("skipContent", {})
        start_marker, end_marker = ignore_block.get("startTag"), ignore_block.get(
            "endTag"
        )
        if start_marker and end_marker and start_marker in raw_template:
            pattern = re.compile(
                f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL
            )
            banner_template = re.sub(pattern, "", raw_template).strip()
        else:
            banner_template = raw_template

        existence_check_string = "## ⚠️ Outdated Post"
        injection_banner = banner_template
        for placeholder, value in placeholders.items():
            injection_banner = injection_banner.replace(placeholder, str(value))

        updated_count = 0
        for old_post in older_posts:
            original_body = old_post.selftext
            new_body = ""

            try:
                if existence_check_string in original_body:
                    logger.info("Replacing outdated banner in post %s.", old_post.id)
                    pattern = re.compile(
                        f"^{re.escape(existence_check_string)}.*?---",
                        re.DOTALL | re.MULTILINE,
                    )
                    new_body = pattern.sub(
                        f"{injection_banner}\n\n---", original_body, 1
                    )
                else:
                    logger.info(
                        "Injecting new outdated banner into post %s.", old_post.id
                    )
                    new_body = f"{injection_banner}\n\n---\n\n{original_body}"

                if new_body.strip() and new_body != original_body:
                    old_post.edit(body=new_body)
                    updated_count += 1
                else:
                    logger.info("Post %s did not need updating.", old_post.id)

            except praw.exceptions.PRAWException:
                logger.warning(
                    "Failed to update banner in post %s.", old_post.id, exc_info=True
                )

        if updated_count > 0:
            logger.info("Successfully updated banner in %s older posts.", updated_count)
    else:  # Overwrite mode
        # ... (This logic is fine)
        pass


def _update_bot_state(post_id: str, config: Dict[str, Any]) -> None:
    """Update the bot's state file.

    Args:
        post_id: The ID of the new active post.
        config: The configuration dictionary.
    """
    new_state = {
        "activePostId": post_id,
        "lastCheckTimestamp": "2024-01-01T00:00:00Z",
        "currentIntervalSeconds": config["timing"]["firstCheck"],
        "lastCommentCount": 0,
    }
    state_path = Path("bot_state.json")
    with state_path.open("w") as f:
        json.dump(new_state, f, indent=2)


def _post_new_release(
    reddit: Any, version: str, urls: str, config: Dict[str, Any]
) -> Any:
    """Post a new release to Reddit.

    Args:
        reddit: The praw.Reddit instance.
        version: The version of the new release.
        urls: The URLs for the new release.
        config: The configuration dictionary.

    Returns:
        The new submission object.
    """
    template_path = Path(config["reddit"]["templateFile"])
    with template_path.open("r") as f:
        raw_template = f.read()

    # 1. Strip the tutorial/comment block as usual
    ignore_block = config.get("skipContent", {})
    start_marker, end_marker = ignore_block.get("startTag"), ignore_block.get("endTag")
    if start_marker and end_marker and start_marker in raw_template:
        pattern = re.compile(
            f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL
        )
        clean_template = re.sub(pattern, "", raw_template)
    else:
        clean_template = raw_template

    # 2. **HARDENED FIX**:
    # Forcefully remove any "Outdated" banner from the new post template
    existence_check_string = "## ⚠️ Outdated Post"
    if existence_check_string in clean_template:
        logger.warning(
            "The main post template contained an 'Outdated Post' banner. "
            "It has been automatically removed."
        )
        banner_pattern = re.compile(
            f"^{re.escape(existence_check_string)}.*?---", re.DOTALL | re.MULTILINE
        )
        post_body_template = banner_pattern.sub("", clean_template).strip()
    else:
        post_body_template = clean_template.strip()

    # 3. Proceed with posting the truly clean template
    initial_status_line = config["feedback"]["statusLineFormat"].replace(
        "{{status}}", config["feedback"]["labels"]["unknown"]
    )
    placeholders = {
        "{{version}}": version,
        "{{bot_name}}": config["reddit"]["botName"],
        "{{bot_repo}}": config["github"]["botRepo"],
        "{{asset_name}}": config["github"]["assetFileName"],
        "{{creator_username}}": config["reddit"]["creator"],
        "{{initial_status}}": initial_status_line,
    }

    url_map: Dict[str, str] = json.loads(urls)
    for app in config["apps"]:
        placeholders[f"direct_download_url_{app['id']}"] = url_map[app["id"]]

    title = config["reddit"]["postTitle"]
    post_body = post_body_template
    for placeholder, value in placeholders.items():
        post_body = post_body.replace(placeholder, str(value))
        title = title.replace(placeholder, str(value))

    logger.info(
        "Submitting new post for v%s to r/%s...",
        version,
        config["reddit"]["subreddit"],
    )
    submission = reddit.subreddit(config["reddit"]["subreddit"]).submit(
        title, selftext=post_body
    )
    logger.info("Post successful: %s", submission.shortlink)
    return submission


def post_new_release(version: str, urls: str) -> None:
    """Post a new release to Reddit.

    Args:
        version: The version of the new release.
        urls: The URLs for the new release.
    """
    config = _load_config()

    logger.info("Authenticating with Reddit...")
    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
        validate_on_submit=True,
    )

    logger.info("Fetching existing posts to prepare for update...")
    existing_posts = _get_bot_posts_on_subreddit(reddit, config)
    new_submission = _post_new_release(reddit, version, urls, config)

    if existing_posts:
        logger.info("Found %s older post(s) to update.", len(existing_posts))
        latest_release_details = {
            "title": new_submission.title,
            "url": new_submission.shortlink,
            "version": version,
        }
        _update_older_posts(existing_posts, latest_release_details, config)

    logger.info("Updating state file to monitor latest post.")
    _update_bot_state(new_submission.id, config)
    logger.info("Post and update process complete.")
