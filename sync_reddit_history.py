import os
import sys
import json
import re
import praw

def sync_reddit_posts():
    """
    Scans the bot's Reddit post history to ensure only the latest post is active
    and all others are marked as outdated. It also self-heals bot_state.json.
    
    This script is intended to be run when no new version is found, acting as a
    resilient maintenance and synchronization mechanism.
    """
    print("Starting Reddit post history synchronization...")
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Authenticate with Reddit
    try:
        reddit = praw.Reddit(
            client_id=os.environ["REDDIT_CLIENT_ID"],
            client_secret=os.environ["REDDIT_CLIENT_SECRET"],
            user_agent=os.environ["REDDIT_USER_AGENT"],
            username=os.environ["REDDIT_USERNAME"],
            password=os.environ["REDDIT_PASSWORD"],
        )
        bot_user = reddit.user.me()
        print(f"Authenticated as u/{bot_user.name}")
    except Exception as e:
        print(f"::error::Failed to authenticate with Reddit: {e}", file=sys.stderr)
        sys.exit(1)

    # Identify bot posts based on the title format from config
    title_template = config['reddit']['postTitle']
    asset_name = config['github']['assetFileName']
    post_identifier = title_template.split('v{{version}}')[0].strip().replace('{{asset_name}}', asset_name)
    print(f"Searching for posts with titles starting with: '{post_identifier}'")

    bot_posts = []
    target_subreddit = config['reddit']['subreddit'].lower()
    for submission in bot_user.submissions.new(limit=100):
        if (submission.subreddit.display_name.lower() == target_subreddit and 
            submission.title.startswith(post_identifier)):
            bot_posts.append(submission)

    if not bot_posts:
        print("No relevant posts found. Nothing to sync.")
        return

    # The first post in the list from .new() is always the most recent one
    latest_post = bot_posts[0]
    older_posts = bot_posts[1:]
    print(f"Latest post identified: {latest_post.id} ('{latest_post.title}')")

    # Update all older posts to link to the latest one
    outdated_format = config['messages']['outdatedPostFormat']
    status_regex = re.compile(config['feedback']['statusLineRegex'], re.MULTILINE)
    updated_count = 0

    for old_post in older_posts:
        outdated_message = outdated_format.replace(
            "{{new_post_title}}", latest_post.title
        ).replace(
            "{{new_post_url}}", latest_post.shortlink
        )
        
        # Avoid needless edits if the post is already correctly updated
        if outdated_message in old_post.selftext:
            continue
        try:
            new_body = status_regex.sub(outdated_message, old_post.selftext)
            if new_body != old_post.selftext:
                old_post.edit(body=new_body)
                print(f"-> Marked older post {old_post.id} as outdated.")
                updated_count += 1
        except Exception as e:
            print(f"::warning::Failed to edit post {old_post.id}: {e}")

    if updated_count > 0:
        print(f"Successfully updated {updated_count} older posts.")
    else:
        print("All older posts were already correctly marked as outdated.")
        
    # Self-heal bot_state.json to ensure the comment checker monitors the correct post
    with open('bot_state.json', 'r') as f:
        state = json.load(f)
        
    if state.get('activePostId') != latest_post.id:
        print(f"State file is out of sync. Current: {state.get('activePostId')}, Expected: {latest_post.id}.")
        state['activePostId'] = latest_post.id
        state['lastCheckTimestamp'] = "2024-01-01T00:00:00Z"
        state['currentIntervalSeconds'] = config['timing']['firstCheck']
        state['lastCommentCount'] = 0
        
        with open('bot_state.json', 'w') as f:
            json.dump(state, f, indent=2)
        print("-> Corrected bot_state.json to monitor the latest post.")
        # Set output for the GitHub Actions workflow to commit the change
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            print("state_changed=true", file=f)
    else:
        print("bot_state.json is already in sync.")
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            print("state_changed=false", file=f)

if __name__ == "__main__":
    sync_reddit_posts()
