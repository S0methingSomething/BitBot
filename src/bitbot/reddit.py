import os
import re
from typing import Any, Dict, List

import praw

from .logging import get_logger

logger = get_logger(__name__)


def _process_template(
    template_path: str, placeholders: Dict[str, str], config: Dict[str, Any]
) -> str:
    """Reads and processes a template file, replacing placeholders."""
    try:
        with open(template_path, "r") as f:
            raw_template = f.read()
    except FileNotFoundError:
        logger.error(f"Template file not found at '{template_path}'.", exc_info=True)
        return ""

    ignore_block = config.get("skipContent", {})
    start_marker, end_marker = ignore_block.get("startTag"), ignore_block.get("endTag")
    if start_marker and end_marker and start_marker in raw_template:
        pattern = re.compile(
            f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL
        )
        template = re.sub(pattern, "", raw_template).strip()
    else:
        template = raw_template

    for placeholder, value in placeholders.items():
        template = template.replace(placeholder, value)

    return template


def get_reddit_instance() -> praw.Reddit:
    """Initializes and returns a PRAW Reddit instance."""
    return praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
    )


def get_bot_posts(
    reddit: praw.Reddit, config: Dict[str, Any]
) -> List[praw.models.Submission]:
    """Fetches all of the bot's release posts from the configured subreddit."""
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
    for submission in bot_user.submissions.new(limit=100):
        if (
            submission.subreddit.display_name.lower() == target_subreddit
            and submission.title.startswith(post_identifier)
        ):
            bot_posts.append(submission)
    return bot_posts


def update_older_posts(
    older_posts: List[praw.models.Submission],
    latest_release_details: Dict[str, Any],
    config: Dict[str, Any],
) -> None:
    """
    Updates older posts by either overwriting them or injecting a banner,
    based on the configuration in `config.json`.
    """
    handling_config = config.get("outdatedPostHandling", {})
    mode = handling_config.get("mode", "overwrite")
    template_path = (
        handling_config.get("injectTemplateFile")
        if mode == "inject"
        else config["reddit"]["outdatedTemplateFile"]
    )

    if not template_path:
        logger.error(
            f"'{mode}' mode selected but the required template file is not defined in config."
        )
        return

    placeholders = {
        "{{latest_post_title}}": latest_release_details["title"],
        "{{latest_post_url}}": latest_release_details["url"],
        "{{latest_version}}": latest_release_details["version"],
        "{{latest_download_url}}": latest_release_details["direct_download_url"],
        "{{asset_name}}": config["github"]["assetFileName"],
        "{{bot_name}}": config["reddit"]["botName"],
        "{{bot_repo}}": config["github"]["botRepo"],
    }

    processed_template = _process_template(template_path, placeholders, config)
    if not processed_template:
        return

    updated_count = 0
    for old_post in older_posts:
        if (
            "⚠️ Outdated Post" in old_post.selftext
            or "This post is outdated." in old_post.selftext
        ):
            continue

        try:
            if mode == "inject":
                new_body = f"{processed_template}\n\n---\n\n{old_post.selftext}"
                logger.info(f"Injecting outdated banner into post {old_post.id}.")
            else:
                new_body = processed_template
                logger.info(f"Overwriting post {old_post.id} with outdated template.")

            old_post.edit(body=new_body)
            updated_count += 1
        except Exception as e:
            logger.warning(f"Failed to update post {old_post.id}: {e}", exc_info=True)

    if updated_count > 0:
        logger.info(f"Successfully updated {updated_count} older posts.")


def post_new_release(
    reddit: praw.Reddit, version: str, direct_download_url: str, config: Dict[str, Any]
) -> praw.models.Submission:
    """Composes and submits a new release post to Reddit."""
    initial_status_line = config["feedback"]["statusLineFormat"].replace(
        "{{status}}", config["feedback"]["labels"]["unknown"]
    )
    placeholders = {
        "{{version}}": version,
        "{{direct_download_url}}": direct_download_url,
        "{{bot_name}}": config["reddit"]["botName"],
        "{{bot_repo}}": config["github"]["botRepo"],
        "{{asset_name}}": config["github"]["assetFileName"],
        "{{creator_username}}": config["reddit"]["creator"],
        "{{initial_status}}": initial_status_line,
    }

    post_body = _process_template(
        config["reddit"]["templateFile"], placeholders, config
    )
    title = config["reddit"]["postTitle"]
    for placeholder, value in placeholders.items():
        title = title.replace(placeholder, value)

    logger.info(
        f"Submitting new post for v{version} to r/{config['reddit']['subreddit']}..."
    )
    submission = reddit.subreddit(config["reddit"]["subreddit"]).submit(
        title, selftext=post_body
    )
    logger.info(f"Post successful: {submission.shortlink}")
    return submission
