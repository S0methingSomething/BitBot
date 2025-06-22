import os
import sys
import json
import re
import praw

def find_and_update_previous_posts(reddit, new_submission, config):
    """
    Finds previous bot posts in the subreddit and updates them to an outdated state.

    This function identifies posts by matching the start of their title against
    the format defined in config.json, making it robust against version changes.
    """
    print("Searching for previous posts to mark as outdated...")
    bot_user = reddit.user.me()
    target_subreddit = config['reddit']['subreddit'].lower()
    
    # Create a unique identifier from the title template to find old posts.
    # e.g., "[BitBot] {{asset_name}} for BitLife v{{version}}" -> "[BitBot] MonetizationVars for BitLife"
    title_template = config['reddit']['postTitle']
    asset_name = config['github']['assetFileName']
    post_identifier = title_template.split('v{{version}}')[0].strip().replace('{{asset_name}}', asset_name)
    
    print(f"Using title identifier: '{post_identifier}'")
    
    outdated_format = config['messages']['outdatedPostFormat']
    status_regex = re.compile(config['feedback']['statusLineRegex'], re.MULTILINE)
    updated_count = 0

    # Iterate through the bot's own recent submissions to find candidates
    for old_submission in bot_user.submissions.new(limit=100):
        if old_submission.id == new_submission.id:
            continue
            
        is_in_target_subreddit = old_submission.subreddit.display_name.lower() == target_subreddit
        is_bot_post = old_submission.title.startswith(post_identifier)

        if is_in_target_subreddit and is_bot_post:
            try:
                print(f"-> Found old post to update: {old_submission.id} ('{old_submission.title}')")
                outdated_message = outdated_format.replace(
                    "{{new_post_title}}", new_submission.title
                ).replace(
                    "{{new_post_url}}", new_submission.shortlink
                )
                
                # Replace the status line with the "OUTDATED" message
                new_body = status_regex.sub(outdated_message, old_submission.selftext)
                
                if new_body != old_submission.selftext:
                    old_submission.edit(body=new_body)
                    print(f"   Successfully marked as outdated.")
                    updated_count += 1
                else:
                    # This means the post might already be marked or has a non-standard body
                    print(f"   Status line already updated or not found.")
            except Exception as e:
                print(f"::warning::Could not update post {old_submission.id}: {e}")
                
    print(f"Finished updating {updated_count} previous post(s).")


def post_update_to_reddit(version, direct_download_url):
    """
    Posts a new release announcement, updates old posts, and resets the monitoring state.
    """
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Load and process the post template, removing the tutorial block
    with open(config['reddit']['templateFile'], 'r') as f:
        post_body_template = f.read()
    
    ignore_block = config.get('skipContent', {})
    start_marker, end_marker = ignore_block.get('startTag'), ignore_block.get('endTag')
    if start_marker and end_marker and start_marker in post_body_template:
        pattern = re.compile(f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
        post_body = re.sub(pattern, '', post_body_template).strip()
    else:
        post_body = post_body_template

    # Dynamically build placeholders for the new post
    initial_status_text = config['feedback']['labels']['unknown']
    initial_status_line = config['feedback']['statusLineFormat'].replace("{{status}}", initial_status_text)
    
    placeholders = {
        "{{version}}": version,
        "{{direct_download_url}}": direct_download_url,
        "{{bot_name}}": config['reddit']['botName'],
        "{{bot_repo}}": config['github']['botRepo'],
        "{{asset_name}}": config['github']['assetFileName'],
        "{{creator_username}}": config['reddit']['creator'],
        "{{initial_status}}": initial_status_line
    }
    
    # Replace placeholders in both title and body
    title = config['reddit']['postTitle']
    for placeholder, value in placeholders.items():
        post_body = post_body.replace(placeholder, value)
        title = title.replace(placeholder, value)

    # Authenticate with Reddit and submit the new post
    print("Authenticating with Reddit...")
    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
        validate_on_submit=True
    )
    print(f"Submitting to r/{config['reddit']['subreddit']}...")
    submission = reddit.subreddit(config['reddit']['subreddit']).submit(title, selftext=post_body)
    print(f"Post successful: {submission.shortlink}")

    # Find and update all previous posts by this bot
    find_and_update_previous_posts(reddit, submission, config)

    # Reset the bot_state.json to monitor only the new post
    print("Updating state file to monitor the new post...")
    new_state = {
        "activePostId": submission.id,
        "lastCheckTimestamp": "2024-01-01T00:00:00Z",
        "currentIntervalSeconds": config['timing']['firstCheck'],
        "lastCommentCount": 0
    }
    with open('bot_state.json', 'w') as f:
        json.dump(new_state, f, indent=2)
    print(f"Updated bot_state.json. New active post is {submission.id}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python post_to_reddit.py <version> <direct_download_url>", file=sys.stderr)
        sys.exit(1)
    post_update_to_reddit(sys.argv[1], sys.argv[2])
