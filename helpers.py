import os
import sys
import json
import re
import praw
import toml
from typing import List, Dict

# --- Configuration and State Management ---

def load_config() -> Dict:
    """Loads the main configuration file (config.toml)."""
    try:
        with open('config.toml', 'r') as f:
            return toml.load(f)
    except FileNotFoundError:
        print("::error::`config.toml` not found. Please ensure the file exists.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"::error::Failed to parse `config.toml`: {e}", file=sys.stderr)
        sys.exit(1)

def load_bot_state() -> Dict:
    """Loads the bot's current monitoring state (bot_state.json)."""
    try:
        with open("bot_state.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("::warning::`bot_state.json` not found. Returning empty state.")
        return {}
    except json.JSONDecodeError:
        print("::error::Could not decode `bot_state.json`. The file may be corrupt.", file=sys.stderr)
        sys.exit(1)

def save_bot_state(data: Dict):
    """Saves the bot's monitoring state."""
    with open("bot_state.json", "w") as f:
        json.dump(data, f, indent=2)

# --- Reddit Client and Post Management ---

def init_reddit(config: Dict) -> praw.Reddit:
    """Initializes and returns a PRAW Reddit instance."""
    return praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
        validate_on_submit=True,
    )

def get_bot_posts(reddit: praw.Reddit, config: Dict) -> List[praw.models.Submission]:
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

def update_older_posts(older_posts: List[praw.models.Submission], latest_release_details: Dict, config: Dict):
    """
    Updates older posts by injecting an 'outdated' banner.
    """
    handling_config = config.get('outdatedPostHandling', {})
    if handling_config.get('mode') != 'inject':
        print("-> Skipping update of older posts as mode is not 'inject'.")
        return

    template_path = handling_config.get('injectTemplateFile')
    if not template_path:
        print("::error::'inject' mode selected but 'injectTemplateFile' is not defined in config.")
        return
    
    try:
        with open(template_path, 'r') as f:
            raw_template = f.read()
    except FileNotFoundError:
        print(f"::error::Inject template file not found at '{template_path}'.")
        return

    # Prepare the banner content
    placeholders = {
        "{{latest_post_title}}": latest_release_details['title'],
        "{{latest_post_url}}": latest_release_details['url'],
        "{{latest_version}}": latest_release_details['version'],
        "{{asset_name}}": config['github']['assetFileName'],
        "{{bot_name}}": config['reddit']['botName'],
        "{{bot_repo}}": config['github']['botRepo'],
    }
    
    ignore_block = config.get('skipContent', {})
    start_marker, end_marker = ignore_block.get('startTag'), ignore_block.get('endTag')
    if start_marker and end_marker and start_marker in raw_template:
        pattern = re.compile(f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
        banner_template = re.sub(pattern, '', raw_template).strip()
    else:
        banner_template = raw_template

    injection_banner = banner_template
    for placeholder, value in placeholders.items():
        injection_banner = injection_banner.replace(placeholder, str(value))
    
    # Update each old post
    updated_count = 0
    existence_check_string = "## ⚠️ Outdated Post" # A key part of the banner to check for existence
    
    for old_post in older_posts:
        original_body = old_post.selftext
        new_body = ""
        
        try:
            if existence_check_string in original_body:
                # Replace existing banner to ensure it's up-to-date
                pattern = re.compile(f"^{re.escape(existence_check_string)}.*?---", re.DOTALL | re.MULTILINE)
                new_body = pattern.sub(f"{injection_banner}\n\n---", original_body, 1)
            else:
                # Inject a new banner at the top
                new_body = f"{injection_banner}\n\n---\n\n{original_body}"
            
            if new_body.strip() and new_body != original_body:
                old_post.edit(body=new_body)
                updated_count += 1
        except Exception as e:
            print(f"::warning::Failed to update banner in post {old_post.id}: {e}")

    if updated_count > 0:
        print(f"Successfully updated banner in {updated_count} older posts.")
