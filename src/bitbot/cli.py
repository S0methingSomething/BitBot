"""The command-line interface for the bot."""

import argparse
import asyncio
import sys

from .comments import check_comments
from .data.models import Settings
from .errors import BitBotError
from .history import sync_history
from .logging import get_logger
from .services.factory import create_services

logger = get_logger(__name__)


def main() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    try:
        settings = Settings()
        services = create_services(settings)

        if args.command == "sync":
            asyncio.run(
                sync_history(
                    config_manager=services["config_manager"],
                    state_manager=services["state_manager"],
                    github_manager=services["github_manager"],
                    reddit_manager=services["reddit_manager"],
                    template_manager=services["template_manager"],
                )
            )
        elif args.command == "pulse":
            asyncio.run(
                check_comments(
                    config_manager=services["config_manager"],
                    state_manager=services["state_manager"],
                    reddit_manager=services["reddit_manager"],
                )
            )
        else:
            parser.print_help()
    except BitBotError as e:
        logger.error(e)
        sys.exit(1)
