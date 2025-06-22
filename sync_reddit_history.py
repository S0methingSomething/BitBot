# sync_reddit_history.py
import os
import sys
import json
import re
import requests
import praw

# Note: Some helper functions are duplicated from post_to_reddit.py. This is a
# deliberate design choice to keep the scripts self-contained, simplifying
# debugging and maintenance as per the user's request.

def _load_config():
    """Loads the main configuration file."""
    with open('config.json', 'r') as f:
        return json.load(f)

def _get_latest_bot_release(config, token):
    """Fetches the latest release from the bot's own GitHub repo (the source of truth)."""
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
    
    version = release_data.get('tag_name', '').lstrip('v')
    asset = next((a for a in release_data.get('assets', []) if a['name'] == config['github']['assetFileName']), None)
    
    if not version or not asset:
        print("::error::Could not find a valid version and asset in the latest bot release.", file=sys.stderr)
        return None
        
    return {"version": version, "url": asset['browser_download_url']}

def _get_bot_posts_on_subreddit(reddit, config):
    """Fetches all of the bot's release posts from the configured subreddit."""
    bot_user = reddit.user.me()
    target_subreddit = config['reddit']['subreddit'].lower()
    
    title_template = config['reddit']['postTitle']
    asset_name = config['github']['assetFileName']
    post_identifier = title_template.split('v{{version}}')[0].strip().replace('{{asset_name}}', asset_name)
    
    bot_posts = []
    for submission in bot_user.submissions.new(limit=100):
        if (submission.subreddit.display_name.lower() == target_subreddit and 
            submission.title.startswith(post_identifier)):
            bot_posts.append(submission)
    return bot_posts

def _parse_version_from_title(title):
    """Extracts a version string from a post title, with a fallback."""
    match = re.search(r'v(\d+\.\d+\.\d+)', title)
    return match.group(1) if match else "0.0.0"

def _update_older_posts(older_posts, latest_post, config):
    """Edits a list of older posts to mark them as outdated."""
    outdated_format = config['messages']['outdatedPostFormat']
    status_regex = re.compile(config['feedback']['statusLineRegex'], re.MULTILINE)
    
    outdated_message = outdated_format.replace(
        "{{new_post_title}}", latest_post.title
    ).replace(
        "{{new_post_url}}", latest_post.shortlink
    )

    for old_post in older_posts:
        if outdated_message in old_post.selftext: continue
        try:
            new_body = status_regex.sub(outdated_message, old_post.selftext)
            if new_body != old_post.selftext:
                old_post.edit(body=new_body)
        except Exception as e:
            print(f"::warning::Failed to edit post {old_post.id}: {e}")

def _update_bot_state(post_id, config):
    """Resets bot_state.json and signals a change to the workflow."""
    new_state = {
        "activePostId": post_id, "lastCheckTimestamp": "2024-01-01T00:00:00Z",
        "currentIntervalSeconds": config['timing']['firstCheck'], "lastCommentCount": 0
    }
    with open('bot_state.json', 'w') as f: json.dump(new_state, f, indent=2)
    print(f"State file updated. Now monitoring post: {post_id}")
    with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
        print("state_changed=true", file=f)

def _post_new_release(reddit, version, direct_download_url, config):
    """Composes and submits a new release post to Reddit."""
    with open(config['reddit']['templateFile'], 'r') as f: post_body_template = f.read()
    
    ignore_block = config.get('skipContent', {})
    start_marker, end_marker = ignore_block.get('startTag'), ignore_block.get('endTag')
    if start_marker and end_marker and start_marker in post_body_template:
        pattern = re.compile(f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
        post_body = re.sub(pattern, '', post_body_template).strip()
    else: post_body = post_body_template

    initial_status_line = config['feedback']['statusLineFormat'].replace("{{status}}", config['feedback']['labels']['unknown'])
    placeholders = {
        "{{version}}": version, "{{direct_download_url}}": direct_download_url,
        "{{bot_name}}": config['reddit']['botName'], "{{bot_repo}}": config['github']['botRepo'],
        "{{asset_name}}": config['github']['assetFileName'], "{{creator_username}}": config['reddit']['creator'],
        "{{initial_status}}": initial_status_line
    }
    
    title = config['reddit']['postTitle']
    for placeholder, value in placeholders.items():
        post_body = post_body.replace(placeholder, value)
        title = title.replace(placeholder, value)

    print(f"Submitting new post for v{version} to r/{config['reddit']['subreddit']}...")
    submission = reddit.subreddit(config['reddit']['subreddit']).submit(title, selftext=post_body)
    print(f"Post successful: {submission.shortlink}")
    return submission

def main():
    """
    Main entry point for syncing Reddit state. This script is called when no
    new version was built and is responsible for all self-healing logic.
    """
    config = _load_config()
    
    print("Authenticating with Reddit...")
    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"], client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"], username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
    )

    # The bot's GitHub repo is the ultimate source of truth.
    latest_bot_release = _get_latest_bot_release(config, os.environ['GITHUB_TOKEN'])
    if not latest_bot_release:
        sys.exit(1)
    
    print(f"Latest available bot release on GitHub is v{latest_bot_release['version']}.")
    bot_posts_on_sub = _get_bot_posts_on_subreddit(reddit, config)

    # Scenario 1: First run or migration to an empty subreddit.
    if not bot_posts_on_sub:
        print(f"No posts found in r/{config['reddit']['subreddit']}. Posting latest available release.")
        new_submission = _post_new_release(reddit, latest_bot_release['version'], latest_bot_release['url'], config)
        _update_bot_state(new_submission.id, config)
        return

    # Scenario 2: Posts exist. Compare latest on Reddit to latest on GitHub.
    latest_reddit_post = bot_posts_on_sub[0]
    latest_reddit_version = _parse_version_from_title(latest_reddit_post.title)
    print(f"Latest post on Reddit is v{latest_reddit_version}.")

    # Sub-Scenario 2a: Reddit is stale. Post the newer version from GitHub.
    if latest_bot_release['version'] > latest_reddit_version:
        print(f"Reddit is out of sync (Reddit: v{latest_reddit_version}, GitHub: v{latest_bot_release['version']}). Posting update.")
        new_submission = _post_new_release(reddit, latest_bot_release['version'], latest_bot_release['url'], config)
        _update_older_posts(bot_posts_on_sub, new_submission, config)
        _update_bot_state(new_submission.id, config)
    # Sub-Scenario 2b: Reddit is up-to-date. Perform a standard self-heal sync.
    else:
        print("Reddit is up-to-date. Performing routine history sync.")
        older_posts = bot_posts_on_sub[1:]
        _update_older_posts(older_posts, latest_reddit_post, config)
        
        with open('bot_state.json', 'r') as f: state = json.load(f)
        if state.get('activePostId') != latest_reddit_post.id:
            print("State file is out of sync. Correcting it.")
            _update_bot_state(latest_reddit_post.id, config)
        else:
            print("Reddit history and state file are already in sync.")
            with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
                print("state_changed=false", file=f)

if __name__ == "__main__":
    main()
