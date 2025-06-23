import json
import re
from pathlib import Path

def load_config():
    """Reads and parses the central config.json file from the project root."""
    with open(PROJECT_ROOT / "config.json", 'r', encoding="utf-8") as f:
        return json.load(f)

def load_state():
    """Loads the bot's current monitoring state from the project root."""
    with open(PROJECT_ROOT / "bot_state.json", 'r', encoding="utf-8") as f:
        return json.load(f)

def save_state(data):
    """Saves the bot's monitoring state back to the project root."""
    with open(PROJECT_ROOT / "bot_state.json", 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# Define the project's root directory to reliably locate files.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

def get_bot_posts_on_subreddit(reddit, config):
    """Finds previous posts made by this bot in the target subreddit."""
    bot_user = reddit.user.me()
    target_subreddit = config['reddit']['subreddit'].lower()
    title_template = config['reddit']['postTitle']
    asset_name = config['github']['assetFileName']
    post_identifier = title_template.split('v{{version}}')[0].strip().replace(
        '{{asset_name}}', asset_name
    )

    bot_posts = []
    for submission in bot_user.submissions.new(limit=100):
        if (submission.subreddit.display_name.lower() == target_subreddit and
                submission.title.startswith(post_identifier)):
            bot_posts.append(submission)
    return bot_posts

def update_older_posts(older_posts, latest_release_details, config):
    """Edits previous release posts to indicate that they are outdated."""
    handling_config = config.get('outdatedPostHandling', {})
    mode = handling_config.get('mode', 'overwrite')

    placeholders = {
        "{{latest_post_title}}": latest_release_details['title'],
        "{{latest_post_url}}": latest_release_details['url'],
        "{{latest_version}}": latest_release_details['version'],
        "{{latest_download_url}}": latest_release_details['direct_download_url'],
        "{{asset_name}}": config['github']['assetFileName'],
        "{{bot_name}}": config['reddit']['botName'],
        "{{bot_repo}}": config['github']['botRepo'],
    }

    template_dir = PROJECT_ROOT / "templates"

    if mode == 'inject':
        template_path = template_dir / handling_config.get('injectTemplateFile', 'inject_template.md')
        if not template_path.exists():
            print(f"::error::Inject template file not found: '{template_path}'.")
            return
        raw_template = template_path.read_text(encoding="utf-8")
        existence_check_string = "⚠️ Outdated Post"
    else:  # overwrite mode
        template_path = template_dir / config['reddit'].get('outdatedTemplateFile', 'outdated_template.md')
        if not template_path.exists():
            print(f"::error::Overwrite template file not found: '{template_path}'.")
            return
        raw_template = template_path.read_text(encoding="utf-8")
        existence_check_string = "This post is outdated."

    ignore_block = config.get('skipContent', {})
    start_marker, end_marker = ignore_block.get('startTag'), ignore_block.get('endTag')
    if start_marker and end_marker and start_marker in raw_template:
        pattern = re.compile(f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
        final_template = re.sub(pattern, '', raw_template).strip()
    else:
        final_template = raw_template

    for placeholder, value in placeholders.items():
        final_template = final_template.replace(placeholder, value)

    updated_count = 0
    for old_post in older_posts:
        if existence_check_string in old_post.selftext:
            continue

        try:
            if mode == 'inject':
                new_body = f"{final_template}\n\n---\n\n{old_post.selftext}"
            else:
                new_body = final_template
            print(f"-> Updating post {old_post.id} (mode: {mode}).")
            old_post.edit(body=new_body)
            updated_count += 1
        except Exception as e:
            print(f"::warning::Failed to update post {old_post.id}: {e}")

    if updated_count > 0:
        print(f"Successfully updated {updated_count} older posts.")

def update_bot_state(post_id, config):
    """Resets the bot's state to monitor a new Reddit post."""
    new_state = {
        "activePostId": post_id,
        "lastCheckTimestamp": "2024-01-01T00:00:00Z",
        "currentIntervalSeconds": config['timing']['firstCheck'],
        "lastCommentCount": 0
    }
    save_state(new_state)
    print(f"State file reset. Now monitoring new post: {post_id}")

def post_new_release(reddit, version, direct_download_url, config):
    """Constructs and submits a new release post to the configured subreddit."""
    template_path = PROJECT_ROOT / "templates" / config['reddit']['templateFile']
    if not template_path.exists():
        print(f"::error::Main post template not found: '{template_path}'")
        return None
    raw_template = template_path.read_text(encoding="utf-8")

    ignore_block = config.get('skipContent', {})
    start_marker, end_marker = ignore_block.get('startTag'), ignore_block.get('endTag')
    if start_marker and end_marker and start_marker in raw_template:
        pattern = re.compile(f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
        post_body_template = re.sub(pattern, '', raw_template).strip()
    else:
        post_body_template = raw_template

    initial_status_line = config['feedback']['statusLineFormat'].replace(
        "{{status}}", config['feedback']['labels']['unknown']
    )
    placeholders = {
        "{{version}}": version, "{{direct_download_url}}": direct_download_url,
        "{{bot_name}}": config['reddit']['botName'], "{{bot_repo}}": config['github']['botRepo'],
        "{{asset_name}}": config['github']['assetFileName'], "{{creator_username}}": config['reddit']['creator'],
        "{{initial_status}}": initial_status_line
    }

    title = config['reddit']['postTitle']
    post_body = post_body_template
    for placeholder, value in placeholders.items():
        post_body = post_body.replace(placeholder, value)
        title = title.replace(placeholder, value)

    print(f"Submitting new post for v{version} to r/{config['reddit']['subreddit']}...")
    submission = reddit.subreddit(config['reddit']['subreddit']).submit(title, selftext=post_body)
    print(f"Post successful: {submission.shortlink}")
    return submission
