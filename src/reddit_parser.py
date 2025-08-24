"""Parse Reddit posts to extract app version information."""

import re
from typing import Any

from config_loader import load_config
from helpers import init_reddit, parse_versions_from_post
from logging_config import get_logger

logger = get_logger(__name__)


def get_bitbot_posts(subreddit: str, bot_name: str) -> list[dict[str, Any]]:
    """Get all posts with [BitBot] tag from subreddit.

    Args:
        subreddit: Subreddit name
        bot_name: Bot's Reddit username

    Returns:
        List of post dictionaries with title, body, id, etc.
    """
    config = load_config()
    reddit = init_reddit(config)

    posts = []
    try:
        # Search for posts by the bot with [BitBot] tag
        search_query = f"author:{bot_name} [BitBot]"
        logger.info(
            f"Searching Reddit with query: {search_query} in subreddit: {subreddit}"
        )
        subreddit_obj = reddit.subreddit(subreddit)

        search_results = list(subreddit_obj.search(search_query, sort="new", limit=50))
        logger.info(f"Found {len(search_results)} total search results")

        for post in search_results:
            logger.info(f"Checking post: {post.title}")
            if "[BitBot]" in post.title:
                logger.info(f"Found [BitBot] post: {post.title}")
                posts.append(
                    {
                        "id": post.id,
                        "title": post.title,
                        "body": post.selftext,
                        "url": post.url,
                        "created_utc": post.created_utc,
                    }
                )
            else:
                logger.info(f"Post doesn't match [BitBot] tag: {post.title}")
    except Exception as e:
        logger.error(f"Failed to fetch Reddit posts: {e}")

    logger.info(f"Found {len(posts)} [BitBot] posts")
    return posts


def parse_changelog_versions(post_body: str) -> dict[str, str]:
    """Extract app versions from changelog section.

    Args:
        post_body: Reddit post body text

    Returns:
        Dict mapping app names to versions
    """
    versions: dict[str, str] = {}

    # Look for changelog section
    changelog_match = re.search(
        r"## Changelog\s*(.+?)(?:\n#{2,}|$)", post_body, re.DOTALL
    )
    if not changelog_match:
        logger.debug("No changelog section found in post")
        return versions

    changelog_content = changelog_match.group(1)

    # Parse different types of changelog entries
    # Pattern 1: "* Added App Name v1.2.3"
    added_pattern = r"\*\s*Added\s+(.+?)\s+v(\d+\.\d+(?:\.\d+)?)"
    # Pattern 2: "* Updated App Name to version 1.2.3"
    updated_pattern = r"\*\s*Updated\s+(.+?)\s+to\s+version\s+(\d+\.\d+(?:\.\d+)?)"
    # Pattern 3: "* App Name v1.2.3" (generic)
    generic_pattern = r"\*\s*(.+?)\s+v(\d+\.\d+(?:\.\d+)?)"

    # Parse added apps
    for match in re.finditer(added_pattern, changelog_content):
        app_name, version = match.groups()
        versions[app_name.strip()] = version.strip()

    # Parse updated apps
    for match in re.finditer(updated_pattern, changelog_content):
        app_name, version = match.groups()
        versions[app_name.strip()] = version.strip()

    # Parse generic entries (fallback)
    for match in re.finditer(generic_pattern, changelog_content):
        app_name, version = match.groups()
        app_name_clean = app_name.strip()
        if app_name_clean not in versions:  # Don't overwrite specific matches
            versions[app_name_clean] = version.strip()

    logger.debug(f"Parsed {len(versions)} app versions from changelog")
    return versions


def extract_app_versions_from_posts() -> dict[str, str]:
    """Extract app versions from the bot's Reddit posts."""
    config = load_config()
    reddit = init_reddit(config)

    # Search for posts by the bot
    subreddit_obj = reddit.subreddit(config.reddit.subreddit)
    search_query = f"author:{config.reddit.bot_name} [BitBot] in subreddit:{config.reddit.subreddit}"
    logger.info(f"Searching Reddit with query: {search_query}")

    search_results = list(subreddit_obj.search(search_query, sort="new", limit=50))
    logger.info(f"Found {len(search_results)} total search results")

    bot_posts = []
    for post in search_results:
        logger.info(f"Checking post: {post.title}")
        if post.title.startswith("[BitBot]"):
            bot_posts.append(post)

    logger.info(f"Found {len(bot_posts)} [BitBot] posts")

    # Extract versions from each post
    versions: dict[str, str] = {}
    for post in bot_posts:
        post_versions: dict[str, str] = parse_versions_from_post(post, config)
        versions.update(post_versions)

    logger.info(f"Total extracted versions: {len(versions)}")
    return versions


if __name__ == "__main__":
    # Test the parser
    versions = extract_app_versions_from_posts()
    for app, version in versions.items():
        logger.info(f"{app}: {version}")
