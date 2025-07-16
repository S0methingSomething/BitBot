"""This module provides a command-line interface for the BitBot library."""

import argparse

from . import comments, debug, history, reddit, release


def main() -> None:
    """The main entry point for the BitBot CLI."""
    parser = argparse.ArgumentParser(
        description="BitBot: A bot for managing Reddit posts about software releases."
    )
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug logging."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- Release Command ---
    parser_release = subparsers.add_parser("release", help="Manage GitHub releases.")
    parser_release.set_defaults(func=release.main)

    # --- Reddit Command ---
    parser_reddit = subparsers.add_parser("reddit", help="Manage Reddit posts.")
    reddit_subparsers = parser_reddit.add_subparsers(
        dest="reddit_command", required=True
    )

    # reddit post command
    parser_reddit_post = reddit_subparsers.add_parser(
        "post", help="Post a new release to Reddit."
    )
    parser_reddit_post.add_argument("--version", required=True)
    parser_reddit_post.add_argument("--urls", required=True)
    parser_reddit_post.set_defaults(
        func=lambda args: reddit.post_new_release(args.version, args.urls)
    )

    # --- Comments Command ---
    parser_comments = subparsers.add_parser(
        "comments", help="Check comments on Reddit posts."
    )
    parser_comments.set_defaults(func=lambda args: comments.check_comments())

    # --- History Command ---
    parser_history = subparsers.add_parser("history", help="Sync Reddit post history.")
    parser_history.set_defaults(func=lambda args: history.sync_history())

    args = parser.parse_args()

    if args.debug:
        debug.enable_debug_mode()

    args.func(args)


if __name__ == "__main__":
    main()
