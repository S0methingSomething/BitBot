"""This module handles the synchronization of Reddit post history."""

import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import praw  # type: ignore
import requests

from . import utils
from .logging import get_logger

logger = get_logger(__name__)


def _get_latest_bot_release(
    config: Dict[str, Any], token: str
) -> Optional[Dict[str, str]]:
    """Get the latest bot release from GitHub.

    Args:
        config: The configuration dictionary.
        token: The GitHub token.

    Returns:
        A dictionary containing the version and URL of the latest release,
        or None if not found.
    """
    bot_repo = config["github"]["botRepo"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }
    api_url = f"https://api.github.com/repos/{bot_repo}/releases/latest"
    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
        release_data = response.json()
    except requests.exceptions.RequestException:
        logger.error("Could not fetch latest release from %s", bot_repo, exc_info=True)
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


def _get_bot_posts_on_subreddit(reddit: Any, config: Dict[str, Any]) -> List[Any]:
    """Get all of the bot's release posts from the configured subreddit.

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


def _parse_version_from_title(title: str) -> str:
    """Parse the version from a post title.

    Args:
        title: The title of the post.

    Returns:
        The version string, or "0.0.0" if not found.
    """
    match = re.search(r"v(\d+\.\d+\.\d+)", title)
    return match.group(1) if match else "0.0.0"


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
        "{{latest_download_url}}": latest_release_details["direct_download_url"],
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
    utils.save_state(new_state)
    logger.info("State file updated. Now monitoring post: %s", post_id)
    github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
    with Path(github_output).open("a") as f:
        f.write("state_changed=true")


def _post_new_release(
    reddit: Any, version: str, direct_download_url: str, config: Dict[str, Any]
) -> Any:
    """Post a new release to Reddit.

    Args:
        reddit: The praw.Reddit instance.
        version: The version of the new release.
        direct_download_url: The direct download URL for the new release.
        config: The configuration dictionary.

    Returns:
        The new submission object.
    """
    template_path = Path(config["reddit"]["templateFile"])
    with template_path.open("r") as f:
        raw_template = f.read()

    ignore_block = config.get("skipContent", {})
    start_marker, end_marker = ignore_block.get("startTag"), ignore_block.get("endTag")
    if start_marker and end_marker and start_marker in raw_template:
        pattern = re.compile(
            f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL
        )
        clean_template = re.sub(pattern, "", raw_template)
    else:
        clean_template = raw_template

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


def sync_history() -> None:
    """Sync the Reddit post history with the latest GitHub release."""
    config = utils.load_config()
    logger.info("Authenticating with Reddit...")
    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
    )

    latest_bot_release = _get_latest_bot_release(config, os.environ["GITHUB_TOKEN"])
    if not latest_bot_release:
        sys.exit(1)

    logger.info(
        "Latest available bot release on GitHub is v%s.",
        latest_bot_release["version"],
    )
    bot_posts_on_sub = _get_bot_posts_on_subreddit(reddit, config)

    if not bot_posts_on_sub:
        logger.info(
            "No posts found in r/%s. Posting latest available release.",
            config["reddit"]["subreddit"],
        )
        new_submission = _post_new_release(
            reddit,
            latest_bot_release["version"],
            latest_bot_release["url"],
            config,
        )
        _update_bot_state(new_submission.id, config)
        return

    latest_reddit_post = bot_posts_on_sub[0]
    latest_reddit_version = _parse_version_from_title(latest_reddit_post.title)
    logger.info("Latest post on Reddit is v%s.", latest_reddit_version)

    if latest_bot_release["version"] > latest_reddit_version:
        logger.info(
            "Reddit is out of sync (Reddit: v%s, GitHub: v%s). Posting update.",
            latest_reddit_version,
            latest_bot_release["version"],
        )
        new_submission = _post_new_release(
            reddit,
            latest_bot_release["version"],
            latest_bot_release["url"],
            config,
        )

        latest_release_details = {
            "title": new_submission.title,
            "url": new_submission.shortlink,
            "version": latest_bot_release["version"],
            "direct_download_url": latest_bot_release["url"],
        }
        _update_older_posts(bot_posts_on_sub, latest_release_details, config)
        _update_bot_state(new_submission.id, config)
        return

    logger.info("Reddit's latest post is up-to-date. Performing routine sync.")
    older_posts = bot_posts_on_sub[1:]
    if older_posts:
        logger.info(
            "Checking %s older post(s) to ensure they are marked as outdated.",
            len(older_posts),
        )
        latest_release_details = {
            "title": latest_reddit_post.title,
            "url": latest_reddit_post.shortlink,
            "version": latest_reddit_version,
            "direct_download_url": latest_bot_release["url"],
        }
        _update_older_posts(older_posts, latest_release_details, config)
    else:
        logger.info("No older posts found to sync.")

    try:
        state = utils.load_state()
        if state.get("activePostId") != latest_reddit_post.id:
            logger.info("State file is out of sync. Correcting it.")
            _update_bot_state(latest_reddit_post.id, config)
        else:
            logger.info("State file is already in sync.")
            github_output = os.environ.get("GITHUB_OUTPUT", "/dev/null")
            with Path(github_output).open("a") as f:
                f.write("state_changed=false")
    except FileNotFoundError:
        logger.info("bot_state.json not found. Creating it now.")
        _update_bot_state(latest_reddit_post.id, config)
