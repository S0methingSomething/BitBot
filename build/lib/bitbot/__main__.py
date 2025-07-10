import argparse
import logging
import sys

from .actions import run_comment_check, run_release_and_post
from .cache import is_cache_valid, update_cache
from .clients import get_clients
from .config import Config, Credentials
from .messages import ExitMessages
from .utils import log_and_exit


def handle_test_credentials(creds: Credentials) -> None:
    """Handles the 'test-credentials' command."""
    logging.info("Performing credential check...")
    missing = [k for k, v in creds.model_dump().items() if v is None]
    if missing:
        log_and_exit(
            ExitMessages.CREDENTIALS_MISSING.format(missing=", ".join(missing))
        )

    logging.info("All required credentials are set.")
    logging.info("Now testing API connections...")
    config = Config.load()
    clients = get_clients(config, creds)
    if not clients:
        log_and_exit(ExitMessages.CLIENT_INIT_FAILED_DESPITE_CREDS)
        return  # Should be unreachable

    gh_client, reddit_client = clients
    gh_ok = gh_client.test_connection()
    reddit_ok = reddit_client.test_connection()

    if gh_ok and reddit_ok:
        logging.info("All credentials are valid and connections are successful.")
        update_cache()
        sys.exit(0)
    else:
        log_and_exit(ExitMessages.CREDENTIAL_VALIDATION_FAILED_API)


def main() -> None:
    """Main entry point for the bot."""
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    parser = argparse.ArgumentParser(
        description="BitBot: A Reddit bot for managing release posts."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser(
        "release",
        help="Check for a new source release, patch it, and post it to Reddit.",
    )
    subparsers.add_parser(
        "check", help="Check for comments on the active post and update its status."
    )
    subparsers.add_parser(
        "test-credentials", help="Test the GitHub and Reddit API credentials."
    )

    args = parser.parse_args()

    try:
        creds = Credentials.load()

        if args.command == "test-credentials":
            handle_test_credentials(creds)
            return  # Should be unreachable if handle_test_credentials exits

        config = Config.load()
        clients = get_clients(config, creds)
        if not clients:
            log_and_exit(ExitMessages.CLIENT_INIT_FAILED)
            return  # Should be unreachable

        gh_client, reddit_client = clients

        if not is_cache_valid():
            logging.info("Performing pre-flight credential check...")
            gh_ok = gh_client.test_connection()
            reddit_ok = reddit_client.test_connection()
            if not (gh_ok and reddit_ok):
                log_and_exit(ExitMessages.PREFLIGHT_CHECK_FAILED)
            update_cache()

        if args.command == "release":
            run_release_and_post(config, gh_client, reddit_client)
        elif args.command == "check":
            run_comment_check(config, gh_client, reddit_client)

    except FileNotFoundError as e:
        log_and_exit(ExitMessages.INITIALIZATION_FAILED.format(error=e), error=e)
    except Exception as e:
        log_and_exit(ExitMessages.UNEXPECTED_ERROR.format(error=e), error=e)


if __name__ == "__main__":
    main()
