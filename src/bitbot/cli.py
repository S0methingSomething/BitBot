"""Command-line interface for BitBot."""

import argparse
import asyncio
import logging
import sys

from dotenv import load_dotenv
from pydantic import ValidationError

from bitbot.bot import run_bot
from bitbot.data.models import Settings
from bitbot.debug import enable_debug_mode
from bitbot.errors import InvalidCredentialsError
from bitbot.services import factory

logger = logging.getLogger(__name__)


async def amain() -> None:
    """The async main entry point for the bot."""
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="A bot for managing Reddit posts about software releases."
    )
    parser.add_argument(
        "--config", default="config.toml", help="Path to the configuration file."
    )
    parser.add_argument(
        "--state", default="data/bot_state.json", help="Path to the state file."
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug logging.")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Enable interactive debugging prompts.",
    )
    args = parser.parse_args()

    if args.debug:
        enable_debug_mode()

    try:
        settings = Settings()
    except ValidationError as e:
        logger.error("Configuration error: Missing environment variables.")
        for error in e.errors():
            loc = error["loc"][0]
            if isinstance(loc, str) and "model." in loc:
                loc = loc.split("model.")[1]
            logger.error(f"  - {loc}: {error['msg']}")
        sys.exit(1)

    services = factory.create_all_services(settings, args)

    try:
        logger.info("Validating credentials...")
        await services["github_manager"].validate_credentials()
        await services["reddit_manager"].validate_credentials()
        logger.info("Credentials are valid.")

        await run_bot(**services)

    except InvalidCredentialsError as e:
        logger.error(f"Credential validation failed: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")


def main() -> None:
    """The main entry point for the bot."""
    asyncio.run(amain())


if __name__ == "__main__":
    main()
