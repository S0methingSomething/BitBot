import argparse
import logging
import os
import sys
from pathlib import Path

import yaml
from pydantic import ValidationError

from .actions import run_comment_check, run_release_and_post
from .clients import GitHubClient, RedditClient
from .config import Config

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def load_validated_config() -> Config:
    """Loads and validates the configuration from config.yaml."""
    config_path = Path("config.yaml")
    if not config_path.exists():
        logging.critical(f"Configuration file not found at: {config_path}")
        sys.exit(1)

    with config_path.open("r", encoding="utf-8") as f:
        raw_config = yaml.safe_load(f)

    try:
        return Config.model_validate(raw_config)
    except ValidationError as e:
        logging.critical(f"Configuration validation failed:\n{e}")
        sys.exit(1)


def _get_github_token() -> str:
    """Retrieves the GitHub token from environment variables, exiting if not found."""
    gh_token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_PAT")
    if not gh_token:
        logging.critical("GITHUB_TOKEN or GH_PAT environment variable not set.")
        sys.exit(1)
    return gh_token


def handle_release(config: Config) -> None:
    """Handler for the 'release' command."""
    github_client = GitHubClient(config, token=_get_github_token())
    reddit_client = RedditClient(config)
    run_release_and_post(config, github_client, reddit_client)


def handle_check_comments(config: Config) -> None:
    """Handler for the 'check-comments' command."""
    github_client = GitHubClient(config, token=_get_github_token())
    reddit_client = RedditClient(config)
    run_comment_check(config, github_client, reddit_client)


def main() -> None:
    """Main CLI entry point."""
    config = load_validated_config()

    parser = argparse.ArgumentParser(description="BitBot command-line interface.")
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )

    # Command: bitbot release
    release_parser = subparsers.add_parser(
        "release",
        help=(
            "Check for new versions, patch, create GitHub release, and post to Reddit."
        ),
    )
    release_parser.set_defaults(func=lambda args: handle_release(config))

    # Command: bitbot check-comments
    check_parser = subparsers.add_parser(
        "check-comments",
        help="Check for comments on the active Reddit post and update status.",
    )
    check_parser.set_defaults(func=lambda args: handle_check_comments(config))

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
