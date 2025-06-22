# post_to_reddit.py
import os
import sys
import json
import re
import argparse
import praw

def _load_config():
    """Loads the main configuration file."""
    with open('config.json', 'r') as f:
        return json.load(f)

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

def _update_older_posts(older_posts, latest_post, config):
    """Edits a list of older posts to mark them as outdated."""
    outdated_format = config['messages']['outdatedPostFormat']
    status_regex = re.compile(config['feedback']['statusLineRegex'], re.MULTILINE)
    
    outdated_message = outdated_format.replace(
        "{{new_post_title}}", latest_post.title
    ).replace(
        "{{new_post_url}}", latest_post.shortlink
    )
    
    updated_count = 0
    for old_post in older_posts:
        if outdated_message in old_post.selftext: continue
        try:
            new_body = status_regex.sub(outdated_message, old_post.selftext)
            if new_body != old_post.selftext:
                print(f"-> Updating post {old_post.id} to OUTDATED.")
                old_post.edit(body=new_body)
                updated_count += 1
        except Exception as e:
            print(f"::warning::Failed to edit post {old_post.id}: {e}")
    
    if updated_count > 0:
        print(f"Successfully updated {updated_count} older posts.")

def _update_bot_state(post_id, config):
    """Resets bot_state.json to monitor a new post."""
    new_state = {
        "activePostId": post_id, "lastCheckTimestamp": "2024-01-01T00:00:00Z",
        "currentIntervalSeconds": config['timing']['firstCheck'], "lastCommentCount": 0
    }
    with open('bot_state.json', 'w') as f: json.dump(new_state, f, indent=2)

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
    Main entry point for posting a new version. This script is called by the
    workflow when a new release has been successfully built.
    """
    parser = argparse.ArgumentParser(description="Post a new release to Reddit.")
    parser.add_argument('--version', required=True)
    parser.add_argument('--direct-download-url', required=True)
    args = parser.parse_args()

    config = _load_config()
    
    print("Authenticating with Reddit...")
    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"], client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"], username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
    )

    print("Fetching existing posts to prepare for update...")
    existing_posts = _get_bot_posts_on_subreddit(reddit, config)

    new_submission = _post_new_release(reddit, args.version, args.direct_download_url, config)

    if existing_posts:
        print(f"Found {len(existing_posts)} older post(s) to update.")
        _update_older_posts(existing_posts, new_submission, config)
    
    print("Updating state file to monitor new post.")
    _update_bot_state(new_submission.id, config)

    print("Post and update process complete.")

if __name__ == "__main__":
    main()        pattern = re.compile(f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
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
    Main entry point for posting a new version. This script is called by the
    workflow when a new release has been successfully built.
    """
    parser = argparse.ArgumentParser(description="Post a new release to Reddit.")
    parser.add_argument('--version', required=True)
    parser.add_argument('--direct-download-url', required=True)
    args = parser.parse_args()

    config = _load_config()
    
    print("Authenticating with Reddit...")
    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"], client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"], username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
    )

    print("Fetching existing posts to prepare for update...")
    existing_posts = _get_bot_posts_on_subreddit(reddit, config)

    new_submission = _post_new_release(reddit, args.version, args.direct_download_url, config)

    if existing_posts:
        print(f"Updating {len(existing_posts)} older post(s)...")
        _update_older_posts(existing_posts, new_submission, config)
    
    print("Updating state file to monitor new post.")
    _update_bot_state(new_submission.id, config)

    print("Post and update process complete.")

if __name__ == "__main__":
    main()
