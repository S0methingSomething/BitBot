import os
import sys
import json
import re
import praw

def post_update_to_reddit(version, direct_download_url):
    """Posts a new release announcement using the new config structure."""
    
    with open('config.json', 'r') as f:
        config = json.load(f)

    print(f"Loading post format from template: {config['reddit']['templateFile']}")
    with open(config['reddit']['templateFile'], 'r') as f:
        post_body_template = f.read()

    # --- Reliably remove the tutorial block ---
    ignore_block = config.get('skipContent', {})
    start_marker = ignore_block.get('startTag')
    end_marker = ignore_block.get('endTag')

    if start_marker and end_marker and start_marker in post_body_template:
        print("Found tutorial markers. Removing tutorial block from post body.")
        pattern = re.compile(f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
        post_body = re.sub(pattern, '', post_body_template).strip()
    else:
        post_body = post_body_template

    print("Authenticating with Reddit...")
    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
        validate_on_submit=True
    )
    
    # Define all available placeholders
    placeholders = {
        "{{version}}": version,
        "{{direct_download_url}}": direct_download_url,
        "{{bot_name}}": config['reddit']['botName'],
        "{{bot_repo}}": config['github']['botRepo'],
        "{{asset_name}}": config['github']['assetFileName'],
        "{{creator_username}}": config['reddit']['creator'],
        "{{initial_status}}": config['feedback']['labels']['unknown']
    }

    # Replace placeholders in the post body
    for placeholder, value in placeholders.items():
        post_body = post_body.replace(placeholder, value)

    # Replace placeholders in the post title
    title_template = config['reddit']['postTitle']
    title = title_template.replace("{{asset_name}}", config['github']['assetFileName']).replace("{{version}}", version)
    
    print(f"Submitting to r/{config['reddit']['subreddit']}...")
    submission = reddit.subreddit(config['reddit']['subreddit']).submit(title, selftext=post_body)
    print(f"Post successful: {submission.shortlink}")

    # After posting, update bot_state.json to monitor the new post
    print("Updating state file with new post ID...")
    with open('bot_state.json', 'r') as f:
        state = json.load(f)
    
    state['postId'] = submission.id
    state['lastCheckTimestamp'] = "2024-01-01T00:00:00Z"
    state['currentIntervalSeconds'] = config['timing']['firstCheck']
    state['lastCommentCount'] = 0
    
    with open('bot_state.json', 'w') as f:
        json.dump(state, f, indent=2)
    print(f"Updated bot_state.json with new post ID: {submission.id}")

if __name__ == "__main__":
    post_update_to_reddit(sys.argv[1], sys.argv[2])
