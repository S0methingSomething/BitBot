from __future__ import annotations

import argparse
import logging
import sys

from .actions import run_comment_check, run_release_and_post
from .cache import is_cache_valid, update_cache
from .clients import get_clients
from .config import Config, Credentials
from .messages import ExitMessages
from .utils import log_and_exit


def main() -> None:
    """
    The main entry point for the BitBot CLI.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    parser = argparse.ArgumentParser(description="BitBot: A Reddit bot for managing release posts.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 'run' command
    parser_run = subparsers.add_parser("run", help="Run the bot's main operational loop.")
    parser_run.add_argument("action", choices=["release", "check"], help="The action to perform.")
    parser_run.set_defaults(func=run_bot)

    # 'config' command
    parser_config = subparsers.add_parser("config", help="Configure BitBot credentials.")
    parser_config.set_defaults(func=configure_credentials)

    # 'test-credentials' command
    parser_test = subparsers.add_parser("test-credentials", help="Test the GitHub and Reddit API credentials.")
    parser_test.set_defaults(func=handle_test_credentials)

    args = parser.parse_args()
    args.func(args)


def run_bot(args: argparse.Namespace) -> None:
    """
    Runs the bot's main operational logic.
    """
    try:
        creds = Credentials.load()
        config = Config.load()
        clients = get_clients(config, creds)
        if not clients:
            log_and_exit(ExitMessages.CLIENT_INIT_FAILED)
            return

        gh_client, reddit_client = clients

        if not is_cache_valid():
            logging.info("Performing pre-flight credential check...")
            gh_ok = gh_client.test_connection()
            reddit_ok = reddit_client.test_connection()
            if not (gh_ok and reddit_ok):
                log_and_exit(ExitMessages.PREFLIGHT_CHECK_FAILED)
            update_cache()

        if args.action == "release":
            run_release_and_post(config, gh_client, reddit_client)
        elif args.action == "check":
            run_comment_check(config, gh_client, reddit_client)

    except FileNotFoundError as e:
        log_and_exit(ExitMessages.INITIALIZATION_FAILED.format(error=e), error=e)
    except Exception as e:
        log_and_exit(ExitMessages.UNEXPECTED_ERROR.format(error=e), error=e)


def configure_credentials(args: argparse.Namespace) -> None:
    """
    Handles the 'config' command.
    """
    creds = Credentials()
    creds.github_token = input("Enter your GitHub token: ")
    creds.reddit_client_id = input("Enter your Reddit client ID: ")
    creds.reddit_client_secret = input("Enter your Reddit client secret: ")
    creds.reddit_user_agent = input("Enter your Reddit user agent: ")
    creds.reddit_username = input("Enter your Reddit username: ")
    creds.reddit_password = input("Enter your Reddit password: ")
    creds.save()
    logging.info("Credentials saved successfully.")


def handle_test_credentials(args: argparse.Namespace) -> None:
    """Handles the 'test-credentials' command."""
    logging.info("Performing credential check...")
    creds = Credentials.load()
    missing = [k for k, v in creds.model_dump().items() if v is None]
    if missing:
        log_and_exit(ExitMessages.CREDENTIALS_MISSING.format(missing=", ".join(missing)))

    logging.info("All required credentials are set.")
    logging.info("Now testing API connections...")
    config = Config.load()
    clients = get_clients(config, creds)
    if not clients:
        log_and_exit(ExitMessages.CLIENT_INIT_FAILED_DESPITE_CREDS)
        return

    gh_client, reddit_client = clients
    gh_ok = gh_client.test_connection()
    reddit_ok = reddit_client.test_connection()

    if gh_ok and reddit_ok:
        logging.info("All credentials are valid and connections are successful.")
        update_cache()
        sys.exit(0)
    else:
        log_and_exit(ExitMessages.CREDENTIAL_VALIDATION_FAILED_API)


if __name__ == "__main__":
    main()
