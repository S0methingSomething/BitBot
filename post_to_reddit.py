import os
import sys
import json
import praw

def post_update_to_reddit(version):
    """Posts a new release announcement and updates the state file."""
    
    with open('config.json', 'r') as f:
        config = json.load(f)

    print(f"Loading post format from template: {config['templateFile']}")
    with open(config['templateFile'], 'r') as f:
        post_body_template = f.read()

    print("Authenticating with Reddit...")
    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
        validate_on_submit=True
    )
    
    replacements = {
        "{{version}}": version,
        "{{bot_name}}": config['botName'],
        "{{bot_repo}}": config['botRepo'],
        "{{asset_name}}": config['assetName'],
        "{{creator_username}}": config['creatorRedditUsername'],
        "{{initial_status}}": config['status']['neutralText']
    }

    post_body = post_body_template
    for placeholder, value in replacements.items():
        post_body = post_body.replace(placeholder, value)

    title = f"{config['assetName']} v{version}"
    
    print(f"Submitting to r/{config['subredditTarget']}...")
    submission = reddit.subreddit(config['subredditTarget']).submit(title, selftext=post_body)
    print(f"Post successful: {submission.shortlink}")

    print("Updating state file with new post ID...")
    with open('bot_state.json', 'r') as f:
        state = json.load(f)
    
    state['postId'] = submission.id
    state['lastCheckTimestamp'] = "2024-01-01T00:00:00Z"
    state['currentIntervalSeconds'] = config['intervals']['initialSeconds']
    state['lastCommentCount'] = 0
    
    with open('bot_state.json', 'w') as f:
        json.dump(state, f, indent=2)
    print(f"Updated bot_state.json with new post ID: {submission.id}")

if __name__ == "__main__":
    post_update_to_reddit(sys.argv[1])
