import os
import sys
import json
import re
import praw
import toml
from typing import List, Dict, Optional
import paths

# --- Configuration and State Management ---

def load_config() -> Dict:
    """Loads the main configuration file (config.toml)."""
    try:
        with open(paths.CONFIG_FILE, 'r') as f:
            return toml.load(f)
    except FileNotFoundError:
        print(f"::error::`{paths.CONFIG_FILE}` not found. Please ensure the file exists.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"::error::Failed to parse `{paths.CONFIG_FILE}`: {e}", file=sys.stderr)
        sys.exit(1)

def load_bot_state() -> Dict:
    """Loads the bot's current monitoring state (bot_state.json)."""
    try:
        with open(paths.BOT_STATE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"::warning::`{paths.BOT_STATE_FILE}` not found. Returning empty state.")
        return {}
    except json.JSONDecodeError:
        print(f"::error::Could not decode `{paths.BOT_STATE_FILE}`. The file may be corrupt.", file=sys.stderr)
        sys.exit(1)

def save_bot_state(data: Dict):
    """Saves the bot's monitoring state."""
    with open(paths.BOT_STATE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_release_state() -> List[int]:
    """Loads the list of processed source release IDs."""
    try:
        with open(paths.RELEASE_STATE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_release_state(data: List[int]):
    """Saves the list of processed source release IDs."""
    with open(paths.RELEASE_STATE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def parse_release_notes(body: str, tag_name: str, config: Dict) -> Optional[Dict]:
    """
    Parses release information from its body or tag name, supporting both new and
    legacy formats.
    """
    app_map_by_id = {app['id']: app['displayName'] for app in config.get('apps', [])}
    
    # --- New Format: Parse from release body ---
    parsing_keys = config.get('parsing', {})
    app_key = parsing_keys.get('app_key', 'app')
    version_key = parsing_keys.get('version_key', 'version')

    app_match = re.search(f"^{app_key}:\\s*(\\S+)", body, re.MULTILINE)
    version_match = re.search(f"^{version_key}:\\s*([\\d\\.]+)", body, re.MULTILINE)

    if app_match and version_match:
        app_id = app_match.group(1)
        version = version_match.group(1)
        display_name = app_map_by_id.get(app_id)
        if display_name:
            return {"app_id": app_id, "display_name": display_name, "version": version}

    # --- Legacy Format: Parse from tag name ---
    # Example tag: "bitlife-v3.19.5"
    for app_id, display_name in app_map_by_id.items():
        if tag_name.lower().startswith(app_id.lower()):
            version_part = tag_name.lower().split('-v')
            if len(version_part) == 2:
                return {"app_id": app_id, "display_name": display_name, "version": version_part[1]}

    return None

def parse_versions_from_post(post: praw.models.Submission, config: Dict) -> Dict[str, str]:
    """
    Parses the versions of all apps from a Reddit post, supporting both legacy
    and new post formats.
    """
    versions = {}
    apps_config = config.get('apps', [])
    app_map_by_display_name = {app['displayName'].lower(): app['id'] for app in apps_config}

    # --- New Format: Parse Changelog from Body ---
    changelog_match = re.search(r"## Changelog\n(.+)", post.selftext, re.DOTALL)
    if changelog_match:
        changelog_text = changelog_match.group(1)
        # Example line: "* Updated BitLife MonetizationVars to version 3.20.1"
        for line in changelog_text.splitlines():
            for display_name, app_id in app_map_by_display_name.items():
                # A flexible regex to find the app name and version on a line
                version_match = re.search(f"{re.escape(display_name)}.*?to version ([\\d\\.]+)", line, re.IGNORECASE)
                if version_match:
                    versions[app_id] = version_match.group(1)
                    break # Move to the next line once an app is found
    
    # --- Legacy Format: Parse from Title ---
    # If the changelog didn't exist or was empty, try parsing the title.
    if not versions:
        # Example title: "[BitBot] MonetizationVars for BitLife v3.19.5"
        for display_name, app_id in app_map_by_display_name.items():
            version_match = re.search(f"for {re.escape(display_name)} v([\\d\\.]+)", post.title, re.IGNORECASE)
            if version_match:
                versions[app_id] = version_match.group(1)
                # Legacy posts only ever had one app, so we can stop.
                break
    
    if versions:
        print(f"Parsed the following versions from post '{post.id}': {versions}")
    else:
        print(f"Could not parse any known versions from post '{post.id}'.")
        
    return versions



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
    
    # Legacy format was "[BitBot] MonetizationVars for BitLife v{{version}}"
    # New format is "[BitBot] New MonetizationVars Release"
    # A common, unique prefix is "[BitBot] MonetizationVars"
    post_identifier = "[BitBot] MonetizationVars"
    
    bot_posts = []
    for submission in bot_user.submissions.new(limit=100):
        if (submission.subreddit.display_name.lower() == target_subreddit and 
            submission.title.startswith(post_identifier)):
            bot_posts.append(submission)
    
    print(f"Found {len(bot_posts)} posts matching the identifier '{post_identifier}'.")
    return bot_posts

def update_older_posts(older_posts: List[praw.models.Submission], latest_release_details: Dict, config: Dict):
    """
    Updates older posts by injecting an 'outdated' banner.
    """
    handling_config = config.get('outdatedPostHandling', {})
    mode = handling_config.get('mode', 'overwrite')
    
    # Placeholders for the banner
    placeholders = {
        "{{latest_post_title}}": latest_release_details['title'],
        "{{latest_post_url}}": latest_release_details['url'],
        "{{latest_version}}": latest_release_details['version'],
        "{{asset_name}}": config['github']['assetFileName'],
        "{{bot_name}}": config['reddit']['botName'],
    }

    if mode == 'inject':
        template_name = config['reddit']['templates'].get('inject_banner')
        if not template_name:
            print("::error::'inject' mode selected but 'inject_banner' template is not defined in config.")
            return
        
        template_path = paths.get_template_path(os.path.basename(template_name))
        
        try:
            with open(template_path, 'r') as f:
                raw_template = f.read()
        except FileNotFoundError:
            print(f"::error::Inject template file not found at '{template_path}'.")
            return
    
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