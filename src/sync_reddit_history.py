import sys
from pathlib import Path

from config_loader import load_config
from helpers import (
    get_bot_posts,
    init_reddit,
    load_bot_state,
    parse_versions_from_post,
    save_bot_state,
)
from logging_config import get_logger

logging = get_logger(__name__)


def main() -> None:
    """
    Synchronizes the bot's online state with the latest post on Reddit.
    """
    config = load_config()

    logging.info("Initializing Reddit client...")
    reddit = init_reddit(config)

    logging.info("Fetching latest bot posts...")
    bot_posts = get_bot_posts(reddit, config)

    if not bot_posts:
        logging.warning("No posts found on Reddit. Cannot sync state.")
        sys.exit(0)

    latest_post = bot_posts[0]
    logging.info(f"Found latest post: {latest_post.title} ({latest_post.id})")

    versions_on_reddit = parse_versions_from_post(latest_post, config)

    if not versions_on_reddit:
        logging.error(
            "Could not parse any versions from the latest post. State will not be updated."
        )
        sys.exit(1)

    logging.info(
        f"Updating local state with versions from Reddit: {versions_on_reddit}"
    )

    bot_state = load_bot_state()
    bot_state["online"]["last_posted_versions"] = versions_on_reddit
    bot_state["online"]["activePostId"] = latest_post.id

    save_bot_state(bot_state)

    logging.info("Successfully synchronized Reddit state to bot_state.json.")


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    main()
