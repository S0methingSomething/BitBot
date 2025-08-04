import os
import sys
import json
import re
import argparse
from datetime import datetime, timedelta, timezone
from packaging.version import parse as parse_version
import paths
from helpers import (
    load_config,
    init_reddit,
    get_bot_posts,
    update_older_posts,
    load_bot_state,
    save_bot_state,
    load_changelog,
    save_changelog,
)

def _generate_changelog_from_ledger(config: dict, changelog_ledger: list) -> str:
    """Generates a Markdown changelog from the running ledger."""
    post_mode = config['reddit'].get('postMode', 'landing_page')
    asset_name = config['github'].get('assetFileName', 'asset')
    formats = config['reddit']['formats']['changelog']
    
    # Aggregate changes to show only the latest version of each app
    latest_changes = {}
    for change in changelog_ledger:
        app_id = change['app_id']
        # If the app is already listed, update it only if the new version is higher
        if app_id in latest_changes:
            if parse_version(change['version']) > parse_version(latest_changes[app_id]['version']):
                latest_changes[app_id] = change
        else:
            latest_changes[app_id] = change

    added_section = ["### ✨ Added"]
    updated_section = ["### ⬆️ Updated"]

    # This is a simplified logic; a more robust version would check against a baseline state
    for _, change in latest_changes.items():
        line_format = formats.get(f"added_{post_mode}") # Simplified for this example
        line = line_format.replace('{{display_name}}', change['display_name']) \
                         .replace('{{asset_name}}', asset_name) \
                         .replace('{{version}}', change['version']) \
                         .replace('{{download_url}}', change['url'])
        added_section.append(line)

    sections = []
    if len(added_section) > 1: sections.append("\n".join(added_section))
    if len(updated_section) > 1: sections.append("\n".join(updated_section))
    
    return "\n\n".join(sections) if sections else "No new updates in this cycle."

def _generate_post_body(config: dict, changelog_ledger: list, github_url: str, vercel_url: str) -> str:
    template_path = paths.get_template_path(os.path.basename(config['reddit']['templates']['post']))
    with open(template_path, 'r') as f:
        template = f.read()
    
    changelog = _generate_changelog_from_ledger(config, changelog_ledger)
    
    placeholders = {
        "{{changelog}}": changelog,
        "{{bot_name}}": config['reddit']['botName'],
        "{{bot_repo}}": config['github']['botRepo'],
        "{{creator_username}}": config['reddit']['creator'],
        "{{github_pages_url}}": github_url or "#",
        "{{vercel_url}}": vercel_url or "#",
    }
    
    for ph, value in placeholders.items():
        template = template.replace(ph, str(value))
    return template

def main():
    parser = argparse.ArgumentParser(description="Manages Reddit posts based on a schedule.")
    parser.add_argument('--github-url', help="URL for GitHub Pages.")
    parser.add_argument('--vercel-url', help="URL for Vercel.")
    args = parser.parse_args()

    config = load_config()
    bot_state = load_bot_state()
    changelog = load_changelog()

    if not changelog:
        print("Changelog is empty. Nothing to post or update.")
        sys.exit(0)

    reddit = init_reddit(config)
    post_frequency_days = config['reddit'].get('post_frequency_days', 0)
    now = datetime.now(timezone.utc)
    last_post_time = datetime.fromisoformat(bot_state.get("lastMajorPostTimestamp", "2000-01-01T00:00:00Z").replace("Z", "+00:00"))
    
    time_since_last_post = now - last_post_time
    is_update_mode = post_frequency_days > 0 and time_since_last_post < timedelta(days=post_frequency_days)

    if is_update_mode:
        # --- UPDATE MODE ---
        active_post_id = bot_state.get("activePostId")
        if not active_post_id:
            print("::error::In update mode but no activePostId found in state. Cannot proceed.")
            sys.exit(1)
        
        print(f"In UPDATE mode. Editing post: {active_post_id}")
        post_body = _generate_post_body(config, changelog, args.github_url, args.vercel_url)
        try:
            submission = reddit.submission(id=active_post_id)
            submission.edit(body=post_body)
            print("Successfully edited and updated the active post.")
        except Exception as e:
            print(f"::error::Failed to edit post {active_post_id}: {e}")
            sys.exit(1)
    else:
        # --- NEW POST MODE ---
        print("In NEW POST mode. Creating a new summary post.")
        title = f"[BitBot] Weekly Summary ({now.strftime('%Y-%m-%d')})"
        post_body = _generate_post_body(config, changelog, args.github_url, args.vercel_url)
        
        try:
            submission = reddit.subreddit(config['reddit']['subreddit']).submit(title, selftext=post_body)
            print(f"Successfully created new post: {submission.shortlink}")

            # Update state with new post info
            bot_state['activePostId'] = submission.id
            bot_state['lastMajorPostTimestamp'] = now.isoformat().replace("+00:00", "Z")
            save_bot_state(bot_state)
            
            # Clear the changelog for the next cycle
            save_changelog([])
            print("State updated and changelog cleared for the next cycle.")
            
            # Mark old posts as outdated
            older_posts = [p for p in get_bot_posts(reddit, config) if p.id != submission.id]
            if older_posts:
                update_older_posts(older_posts, {"title": submission.title, "url": submission.shortlink, "version": "latest"}, config)

        except Exception as e:
            print(f"::error::Failed to create new post: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
