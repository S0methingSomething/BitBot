"""Core bot logic."""

import asyncio
import logging

from bitbot.githandler import check_new_release
from bitbot.interfaces.config_manager import ConfigManagerProtocol
from bitbot.interfaces.github_manager import GitHubManagerProtocol
from bitbot.interfaces.reddit_manager import RedditManagerProtocol
from bitbot.interfaces.state_manager import StateManagerProtocol

logging.basicConfig(level=logging.INFO)


async def run_bot(
    config_manager: ConfigManagerProtocol,
    github_manager: GitHubManagerProtocol,
    reddit_manager: RedditManagerProtocol,
    state_manager: StateManagerProtocol,
) -> None:
    """The main bot loop."""
    logging.info("Bot is running...")
    config = await config_manager.load_config()
    while True:
        for app in config.apps:
            logging.info(f"Checking for new releases for {app.name}...")
            new_release = await check_new_release(app, github_manager, state_manager)
            if new_release:
                logging.info(f"New release found for {app.name}: {new_release.version}")
                title = app.post_title_template.format(version=new_release.version)
                body = (
                    new_release.body
                    or f"Version {new_release.version} of {app.name} has been released."
                )
                await reddit_manager.submit_post(app.subreddit, title, body)
                logging.info(f"Posted to Reddit: {title}")
        logging.info("Sleeping for 60 seconds...")
        await asyncio.sleep(60)


async def main() -> None:
    """The main entry point for the bot."""
    # This is where you would initialize your managers (config, github, reddit, state)
    # and then call run_bot.
    # For now, this is just a placeholder.
    pass


if __name__ == "__main__":
    asyncio.run(main())
