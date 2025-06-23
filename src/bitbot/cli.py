import argparse
import os
import re
import sys
from datetime import datetime, timezone, timedelta

import praw

from . import github as github_utils
from . import reddit as reddit_utils


def get_reddit_instance():
    """Initializes and returns a PRAW Reddit instance from environment variables."""
    return praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
    )

def handle_post(args):
    """Action for the 'post' command: post a new release to Reddit."""
    config = reddit_utils.load_config()
    reddit = get_reddit_instance()

    print("Fetching existing bot posts to mark as outdated...")
    existing_posts = reddit_utils.get_bot_posts_on_subreddit(reddit, config)

    new_submission = reddit_utils.post_new_release(reddit, args.version, args.direct_download_url, config)
    if not new_submission:
        sys.exit(1)  # Exit if posting failed

    if existing_posts:
        print(f"Found {len(existing_posts)} older post(s) to update.")
        latest_release_details = {
            "title": new_submission.title, "url": new_submission.shortlink,
            "version": args.version, "direct_download_url": args.direct_download_url,
        }
        reddit_utils.update_older_posts(existing_posts, latest_release_details, config)

    print("Updating bot state to monitor the new post.")
    reddit_utils.update_bot_state(new_submission.id, config)
    print("\nPost and update process complete.")

def handle_sync(_args):
    """Action for the 'sync' command: sync Reddit history with GitHub releases."""
    config = reddit_utils.load_config()
    reddit = get_reddit_instance()
    state_changed = False

    latest_bot_release = github_utils.get_latest_bot_release(config, os.environ['GITHUB_TOKEN'])
    if not latest_bot_release:
        sys.exit(1)

    print(f"Latest GitHub Release found: v{latest_bot_release['version']}.")
    bot_posts_on_sub = reddit_utils.get_bot_posts_on_subreddit(reddit, config)

    if not bot_posts_on_sub:
        print(f"No posts found in r/{config['reddit']['subreddit']}. Posting the latest available release.")
        new_submission = reddit_utils.post_new_release(
            reddit, latest_bot_release['version'], latest_bot_release['url'], config
        )
        reddit_utils.update_bot_state(new_submission.id, config)
        state_changed = True
    else:
        latest_reddit_post = bot_posts_on_sub[0]
        latest_reddit_version = github_utils.parse_version_from_title(latest_reddit_post.title)
        print(f"Latest Reddit Post found: v{latest_reddit_version}.")

        if latest_bot_release['version'] > latest_reddit_version:
            print(f"Reddit is out of sync. Posting update for v{latest_bot_release['version']}.")
            new_submission = reddit_utils.post_new_release(
                reddit, latest_bot_release['version'], latest_bot_release['url'], config
            )
            latest_release_details = {
                "title": new_submission.title, "url": new_submission.shortlink,
                "version": latest_bot_release['version'], "direct_download_url": latest_bot_release['url']
            }
            reddit_utils.update_older_posts(bot_posts_on_sub, latest_release_details, config)
            reddit_utils.update_bot_state(new_submission.id, config)
            state_changed = True
        else:
            print("Reddit's latest post is up-to-date. Performing routine sync.")
            older_posts = bot_posts_on_sub[1:]
            if older_posts:
                latest_release_details = {
                    "title": latest_reddit_post.title, "url": latest_reddit_post.shortlink,
                    "version": latest_bot_release['version'], "direct_download_url": latest_bot_release['url']
                }
                reddit_utils.update_older_posts(older_posts, latest_release_details, config)

            current_state = reddit_utils.load_state()
            if current_state.get('activePostId') != latest_reddit_post.id:
                print(f"State file is out of sync. Correcting it to monitor post {latest_reddit_post.id}.")
                reddit_utils.update_bot_state(latest_reddit_post.id, config)
                state_changed = True
            else:
                print("State file is already in sync.")

    github_utils.set_github_output("state_changed", str(state_changed).lower())

def handle_check_comments(_args):
    """Action for 'check-comments': check for new feedback on Reddit."""
    config = reddit_utils.load_config()
    state = reddit_utils.load_state()
    state_was_meaningfully_updated = False
    real_check_performed = False

    if not state.get("activePostId"):
        print("No active post ID in state file. Nothing to check.")
        sys.exit(0)

    now = datetime.now(timezone.utc)
    last_check = datetime.fromisoformat(state["lastCheckTimestamp"].replace("Z", "+00:00"))

    if now < (last_check + timedelta(seconds=state["currentIntervalSeconds"])):
        wait_seconds = (last_check + timedelta(seconds=state['currentIntervalSeconds'])) - now
        print(f"Not time for a full check yet. Next check in {int(wait_seconds.total_seconds())}s.")
        github_utils.set_github_output("state_changed", "false")
        sys.exit(0)

    try:
        print(f"Time for a real check on post: {state['activePostId']}")
        real_check_performed = True
        reddit = get_reddit_instance()
        submission = reddit.submission(id=state["activePostId"])
        submission.comments.replace_more(limit=0)
        comments = submission.comments.list()

        working_kw = re.compile("|".join(config["feedback"]["workingKeywords"]), re.I)
        not_working_kw = re.compile("|".join(config["feedback"]["notWorkingKeywords"]), re.I)
        positive_score = sum(1 for c in comments if working_kw.search(c.body))
        negative_score = sum(1 for c in comments if not_working_kw.search(c.body))
        net_score = positive_score - negative_score
        print(f"Comment analysis: Positive={positive_score}, Negative={negative_score}, Net Score={net_score}")

        threshold = config["feedback"]["minFeedbackCount"]
        new_status_text = config['feedback']['labels']['unknown']
        if net_score <= -threshold:
            new_status_text = config["feedback"]["labels"]["broken"]
        elif net_score >= threshold:
            new_status_text = config["feedback"]["labels"]["working"]

        new_status_line = config["feedback"]["statusLineFormat"].replace("{{status}}", new_status_text)

        status_regex = re.compile(config["feedback"]["statusLineRegex"], re.MULTILINE)
        if not status_regex.search(submission.selftext):
            print("::warning::Could not find status line in the post. It may have been edited.")
        elif new_status_line not in submission.selftext:
            updated_body = status_regex.sub(new_status_line, submission.selftext)
            submission.edit(body=updated_body)
            print(f"Post status updated to: {new_status_text}")
        else:
            print("Post status is already correct.")

        if len(comments) > state["lastCommentCount"]:
            state["currentIntervalSeconds"] = config["timing"]["firstCheck"]
            state_was_meaningfully_updated = True
        elif state["currentIntervalSeconds"] < config["timing"]["maxWait"]:
            new_interval = state["currentIntervalSeconds"] + config["timing"]["increaseBy"]
            state["currentIntervalSeconds"] = min(config["timing"]["maxWait"], new_interval)
            state_was_meaningfully_updated = True

        if state["lastCommentCount"] != len(comments):
            state["lastCommentCount"] = len(comments)
            state_was_meaningfully_updated = True

    except praw.exceptions.PRAWException as e:
        print(f"::error::A PRAW-specific error occurred during check: {e}", file=sys.stderr)
    except requests.exceptions.RequestException as e:
        print(f"::error::A network error occurred during check: {e}", file=sys.stderr)

    finally:
        state["lastCheckTimestamp"] = now.isoformat().replace("+00:00", "Z")
        should_commit_state = state_was_meaningfully_updated or real_check_performed
        if should_commit_state:
            print("Meaningful state change detected. Saving state file.")
            reddit_utils.save_state(state)
        else:
            print("No meaningful state change detected. Skipping file write.")
        github_utils.set_github_output("state_changed", str(should_commit_state).lower())
        print(f"Pulse check complete. Next interval: {state['currentIntervalSeconds']}s")

def handle_release(_args):
    """Action for 'release' command: Create a new GitHub release."""
    github_utils.create_release()

def main():
    """Main CLI entry point for all bot operations."""
    parser = argparse.ArgumentParser(description="BitBot command-line interface.")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Command: bitbot release
    release_parser = subparsers.add_parser("release", help="Check for new versions and create a GitHub release.")
    release_parser.set_defaults(func=handle_release)

    # Command: bitbot post
    post_parser = subparsers.add_parser("post", help="Post a new release to Reddit.")
    post_parser.add_argument('--version', required=True)
    post_parser.add_argument('--direct-download-url', required=True)
    post_parser.set_defaults(func=handle_post)

    # Command: bitbot sync
    sync_parser = subparsers.add_parser("sync", help="Sync Reddit history with GitHub releases.")
    sync_parser.set_defaults(func=handle_sync)

    # Command: bitbot check-comments
    check_parser = subparsers.add_parser("check-comments", help="Check for comments on the active Reddit post.")
    check_parser.set_defaults(func=handle_check_comments)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
