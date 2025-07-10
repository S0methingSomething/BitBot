import argparse
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from typing import Any

from . import config, github, reddit, state
from .logging import get_logger

logger = get_logger(__name__)


def _update_bot_state(post_id: str) -> None:
    """Resets bot_state.json and signals a change to the workflow."""
    cfg = config.Config.get_instance()
    st = state.get_state()
    st.update(
        {
            "activePostId": post_id,
            "lastCheckTimestamp": datetime.now(timezone.utc).isoformat(),
            "currentIntervalSeconds": cfg.timing.first_check,
            "lastCommentCount": 0,
        }
    )
    state.save_state(st)
    logger.info(f"State file updated. Now monitoring post: {post_id}")
    with open(os.environ.get("GITHUB_OUTPUT", "/dev/null"), "a") as f:
        f.write("state_changed=true\n")


def _post(args: argparse.Namespace) -> None:
    """Handles posting a new release."""
    cfg = config.Config.get_instance()
    r = reddit.get_reddit_instance()

    logger.info("Fetching existing posts to prepare for update...")
    existing_posts = reddit.get_bot_posts(r, cfg.model_dump())

    new_submission = reddit.post_new_release(
        r, args.version, args.direct_download_url, cfg.model_dump()
    )

    if existing_posts:
        logger.info(f"Found {len(existing_posts)} older post(s) to update.")
        latest_release_details = {
            "title": new_submission.title,
            "url": new_submission.shortlink,
            "version": args.version,
            "direct_download_url": args.direct_download_url,
        }
        reddit.update_older_posts(
            existing_posts, latest_release_details, cfg.model_dump()
        )

    logger.info("Updating state file to monitor latest post.")
    _update_bot_state(new_submission.id)
    logger.info("Post and update process complete.")


def _sync() -> None:
    """Handles syncing Reddit state with GitHub releases."""
    cfg = config.Config.get_instance()
    st = state.get_state()
    r = reddit.get_reddit_instance()

    latest_bot_release = github.get_latest_release(cfg.model_dump())
    if not latest_bot_release:
        sys.exit(1)

    logger.info(
        f"Latest available bot release on GitHub is v{latest_bot_release['version']}."
    )
    bot_posts_on_sub = reddit.get_bot_posts(r, cfg.model_dump())

    if not bot_posts_on_sub:
        logger.info(
            f"No posts found in r/{cfg.reddit.subreddit}. Posting latest available release."
        )
        new_submission = reddit.post_new_release(
            r,
            latest_bot_release["version"],
            latest_bot_release["url"],
            cfg.model_dump(),
        )
        _update_bot_state(new_submission.id)
        return

    latest_reddit_post = bot_posts_on_sub[0]

    match = re.search(r"v(\d+\.\d+\.\d+)", latest_reddit_post.title)
    latest_reddit_version = match.group(1) if match else "0.0.0"

    logger.info(f"Latest post on Reddit is v{latest_reddit_version}.")

    if latest_bot_release["version"] > latest_reddit_version:
        logger.info(
            f"Reddit is out of sync (Reddit: v{latest_reddit_version}, GitHub: v{latest_bot_release['version']}). Posting update."
        )
        new_submission = reddit.post_new_release(
            r,
            latest_bot_release["version"],
            latest_bot_release["url"],
            cfg.model_dump(),
        )

        latest_release_details = {
            "title": new_submission.title,
            "url": new_submission.shortlink,
            "version": latest_bot_release["version"],
            "direct_download_url": latest_bot_release["url"],
        }
        reddit.update_older_posts(
            bot_posts_on_sub, latest_release_details, cfg.model_dump()
        )
        _update_bot_state(new_submission.id)
        return

    logger.info("Reddit's latest post is up-to-date. Performing routine sync.")

    older_posts = bot_posts_on_sub[1:]
    if older_posts:
        logger.info(
            f"Checking {len(older_posts)} older post(s) to ensure they are marked as outdated."
        )
        latest_release_details = {
            "title": latest_reddit_post.title,
            "url": latest_reddit_post.shortlink,
            "version": latest_bot_release["version"],
            "direct_download_url": latest_bot_release["url"],
        }
        reddit.update_older_posts(older_posts, latest_release_details, cfg.model_dump())
    else:
        logger.info("No older posts found to sync.")

    if st.get("activePostId") != latest_reddit_post.id:
        logger.info("State file is out of sync. Correcting it.")
        _update_bot_state(latest_reddit_post.id)
    else:
        logger.info("State file is already in sync.")
        with open(os.environ.get("GITHUB_OUTPUT", "/dev/null"), "a") as f:
            f.write("state_changed=false\n")


def _analyze_comments(comments: list[Any], cfg: config.Config) -> str:
    """Analyzes comments and returns a new status."""
    working_kw = re.compile("|".join(cfg.feedback.working_keywords), re.I)
    not_working_kw = re.compile("|".join(cfg.feedback.not_working_keywords), re.I)
    positive_score = sum(1 for c in comments if working_kw.search(c.body))
    negative_score = sum(1 for c in comments if not_working_kw.search(c.body))
    net_score = positive_score - negative_score
    logger.info(
        f"Comment analysis: Positive={positive_score}, Negative={negative_score}, Net Score={net_score}"
    )

    threshold = cfg.feedback.min_feedback_count
    if net_score <= -threshold:
        return cfg.feedback.labels["broken"]
    elif net_score >= threshold:
        return cfg.feedback.labels["working"]
    else:
        return cfg.feedback.labels["unknown"]


def _update_post_status(submission: Any, new_status: str, cfg: config.Config) -> None:
    """Updates the status line in a post."""
    new_status_line = cfg.messages.status_line.replace("{{status}}", new_status)
    status_regex = re.compile(cfg.feedback.status_line_regex, re.MULTILINE)
    if not status_regex.search(submission.selftext):
        logger.warning(
            "Could not find status line in post. It may have been edited or is an outdated post."
        )
    elif new_status_line not in submission.selftext:
        updated_body = status_regex.sub(new_status_line, submission.selftext)
        submission.edit(body=updated_body)
        logger.info(f"Status updated to: {new_status}")
    else:
        logger.info("Status is already correct.")


def _check() -> None:
    """
    Checks for comments on the active Reddit post, analyzes feedback, and
    updates the post status with an adaptive timer.
    """
    cfg = config.Config.get_instance()
    st = state.get_state()

    if not st.get("activePostId"):
        logger.info("No active post ID in state file. Exiting pulse.")
        sys.exit(0)

    now = datetime.now(timezone.utc)
    last_check = datetime.fromisoformat(st["lastCheckTimestamp"].replace("Z", "+00:00"))

    if now < (last_check + timedelta(seconds=st["currentIntervalSeconds"])):
        logger.info(
            f"Not time yet. Next check in {int(((last_check + timedelta(seconds=st['currentIntervalSeconds'])) - now).total_seconds())}s."
        )
        with open(os.environ.get("GITHUB_OUTPUT", "/dev/null"), "a") as f:
            f.write("state_changed=false\n")
        sys.exit(0)

    logger.info(f"Time for a real check on post: {st['activePostId']}")
    state_was_meaningfully_updated = False
    try:
        r = reddit.get_reddit_instance()
        submission = r.submission(id=st["activePostId"])
        submission.comments.replace_more(limit=0)
        comments = submission.comments.list()

        new_status = _analyze_comments(comments, cfg)
        _update_post_status(submission, new_status, cfg)

        if len(comments) > st["lastCommentCount"]:
            st["currentIntervalSeconds"] = cfg.timing.first_check
            state_was_meaningfully_updated = True
        elif st["currentIntervalSeconds"] < cfg.timing.max_wait:
            st["currentIntervalSeconds"] = min(
                cfg.timing.max_wait,
                st["currentIntervalSeconds"] + cfg.timing.increase_by,
            )
            state_was_meaningfully_updated = True

        if st["lastCommentCount"] != len(comments):
            st["lastCommentCount"] = len(comments)
            state_was_meaningfully_updated = True

    except Exception as e:
        logger.error(f"An exception occurred during check: {e}", exc_info=True)
    finally:
        st["lastCheckTimestamp"] = now.isoformat().replace("+00:00", "Z")
        if state_was_meaningfully_updated:
            logger.info("Meaningful state change detected. Saving state file.")
            state.save_state(st)
        else:
            logger.info("No meaningful state change detected. Skipping file write.")

        with open(os.environ.get("GITHUB_OUTPUT", "/dev/null"), "a") as f:
            f.write(f"state_changed={str(state_was_meaningfully_updated).lower()}\n")
        logger.info(
            f"Pulse check complete. Next interval: {st['currentIntervalSeconds']}s"
        )


def main() -> None:
    """Main entry point for the bot."""
    parser = argparse.ArgumentParser(
        description="BitBot: A Reddit bot for managing release posts."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    post_parser = subparsers.add_parser("post", help="Post a new release to Reddit.")
    post_parser.add_argument("--version", required=True)
    post_parser.add_argument("--direct-download-url", required=True)
    post_parser.set_defaults(func=_post)

    sync_parser = subparsers.add_parser(
        "sync", help="Sync Reddit history with GitHub releases."
    )
    sync_parser.set_defaults(func=_sync)

    check_parser = subparsers.add_parser(
        "check", help="Check for comments on the active post."
    )
    check_parser.set_defaults(func=_check)

    args = parser.parse_args()

    config.Config.load()
    state.load_state()

    if hasattr(args, "func"):
        if args.command == "post":
            args.func(args)
        else:
            args.func()


if __name__ == "__main__":
    main()
