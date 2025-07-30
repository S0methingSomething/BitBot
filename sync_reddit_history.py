import os
import sys
import re
import requests
from helpers import (
    load_config,
    init_reddit,
    get_bot_posts,
    update_older_posts,
    save_bot_state,
    load_bot_state,
)

def _get_latest_bot_release(config, token):
    bot_repo = config['github']['botRepo']
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    api_url = f"https://api.github.com/repos/{bot_repo}/releases/latest"
    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
        release_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"::error::Could not fetch latest release from {bot_repo}: {e}", file=sys.stderr)
        return None
    
    version_match = re.search(r'v([\d\.]+)', release_data.get('tag_name', ''))
    if not version_match:
        print("::error::Could not parse version from tag name.", file=sys.stderr)
        return None
    version = version_match.group(1)

    asset = next((a for a in release_data.get('assets', []) if a['name'] == config['github']['assetFileName']), None)
    if not asset:
        print("::error::Could not find a valid asset in the latest bot release.", file=sys.stderr)
        return None
        
    return {"version": version, "url": asset['browser_download_url']}

def _parse_version_from_title(title):
    match = re.search(r'v(\d+\.\d+\.\d+)', title)
    return match.group(1) if match else "0.0.0"

def main():
    config = load_config()
    print("Authenticating with Reddit...")
    reddit = init_reddit(config)

    latest_bot_release = _get_latest_bot_release(config, os.environ['GITHUB_TOKEN'])
    if not latest_bot_release:
        sys.exit(1)
    
    print(f"Latest available bot release on GitHub is v{latest_bot_release['version']}.")
    bot_posts_on_sub = get_bot_posts(reddit, config)

    if not bot_posts_on_sub:
        print(f"No posts found in r/{config['reddit']['subreddit']}. Cannot sync history.")
        # In a real-world scenario, you might want to post the latest release here.
        # For a sync script, exiting is safer.
        sys.exit(0)

    latest_reddit_post = bot_posts_on_sub[0]
    latest_reddit_version = _parse_version_from_title(latest_reddit_post.title)
    print(f"Latest post on Reddit is v{latest_reddit_version}.")

    # This script primarily ensures old posts are marked correctly and state is in sync.
    # It does NOT post new releases. That is the job of post_to_reddit.py.
    print("Routine sync initiated. Ensuring all older posts are correctly marked.")
    
    older_posts = bot_posts_on_sub[1:]
    if older_posts:
        print(f"Checking {len(older_posts)} older post(s) to ensure they are marked as outdated.")
        latest_release_details = {
            "title": latest_reddit_post.title,
            "url": latest_reddit_post.shortlink,
            "version": latest_reddit_version,
        }
        update_older_posts(older_posts, latest_release_details, config)
    else:
        print("No older posts found to sync.")
    
    # Check if the state file is pointing to the latest post
    state = load_bot_state()
    if state.get('activePostId') != latest_reddit_post.id:
        print("State file is out of sync. Correcting it now.")
        new_state = {
            "activePostId": latest_reddit_post.id,
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

if __name__ == "__main__":
    main()