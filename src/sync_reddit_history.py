import os
import sys
from helpers import (
    load_config,
    init_reddit,
    get_bot_posts,
    update_older_posts,
    save_bot_state,
    load_bot_state,
    parse_versions_from_post,
)

def main():
    """
    A maintenance script to ensure the bot's state is aligned with the actual
    state of Reddit. It ensures old posts are marked as outdated and that the
    bot is monitoring the single latest post.
    """
    config = load_config()
    print("Authenticating with Reddit...")
    reddit = init_reddit(config)

    print("Fetching bot posts from subreddit...")
    bot_posts = get_bot_posts(reddit, config)

    if not bot_posts:
        print("No posts found. Nothing to sync.")
        sys.exit(0)

    latest_post = bot_posts[0]
    older_posts = bot_posts[1:]
    print(f"Latest post identified: {latest_post.id}. Found {len(older_posts)} older post(s).")

    # 1. Ensure all older posts are correctly marked as outdated
    if older_posts:
        latest_versions = parse_versions_from_post(latest_post, config)
        # For the banner, we just need a representative version. We'll grab the first one.
        latest_version_str = next(iter(latest_versions.values()), "latest")

        latest_release_details = {
            "title": latest_post.title,
            "url": latest_post.shortlink,
            "version": latest_version_str,
        }
        update_older_posts(older_posts, latest_release_details, config)
    else:
        print("No older posts found to update.")

    # 2. Ensure the state file is pointing to the latest post
    state = load_bot_state()
    if state.get('activePostId') != latest_post.id:
        print(f"State file is out of sync. Pointing to '{state.get('activePostId')}', but should be '{latest_post.id}'. Correcting it now.")
        new_state = {
            "activePostId": latest_post.id,
            "lastCheckTimestamp": "2024-01-01T00:00:00Z",
            "currentIntervalSeconds": config['timing']['firstCheck'],
            "lastCommentCount": 0
        }
        save_bot_state(new_state)
        with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
            print("state_changed=true", file=f)
    else:
        print("State file is already in sync.")
        with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
            print("state_changed=false", file=f)
            
    print("Sync complete.")

if __name__ == "__main__":
    main()
