"""Synchronize Reddit state with local state."""

import sys
from pathlib import Path

from beartype import beartype

from core.config import load_config
from core.state import load_bot_state, save_bot_state
from reddit.client import init_reddit
from reddit.posts import get_bot_posts
from reddit.parser import parse_versions_from_post


@beartype  # type: ignore[misc]
def main() -> None:
    """TODO: Add docstring."""
    """Synchronizes the bot's online state with the latest post on Reddit.
    This script reads the latest Reddit post, parses the versions from it,
    and updates the `online.last_posted_versions` in `bot_state.json`.
    """
    config = load_config()

    reddit = init_reddit(config)

    bot_posts = get_bot_posts(reddit, config)

    if not bot_posts:
        sys.exit(0)

    latest_post = bot_posts[0]

    versions_on_reddit = parse_versions_from_post(latest_post, config)

    if not versions_on_reddit:
        sys.exit(1)

    bot_state = load_bot_state()
    bot_state["online"]["last_posted_versions"] = versions_on_reddit
    bot_state["online"]["activePostId"] = latest_post.id

    save_bot_state(bot_state)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))
    main()
