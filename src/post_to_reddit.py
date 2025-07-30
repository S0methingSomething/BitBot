import os
import sys
import json
import re
import argparse
from helpers import (
    load_config,
    init_reddit,
    get_bot_posts,
    update_older_posts,
    save_bot_state,
)

def _generate_changelog(config: dict) -> str:
    """Generates a changelog string from the releases.json file."""
    releases_path = '../dist/releases.json'
    if not os.path.exists(releases_path):
        return "No release data found."

    with open(releases_path, 'r') as f:
        releases_data = json.load(f)

    changelog_lines = []
    line_format = config['reddit'].get('changelog_line_format', "* {{display_name}} updated to v{{version}}")
    asset_name = config['github'].get('assetFileName', 'asset')

    for app_id, release_info in releases_data.items():
        line = line_format.replace('{{display_name}}', release_info['display_name'])
        line = line.replace('{{asset_name}}', asset_name)
        line = line.replace('{{version}}', release_info['version'])
        line = line.replace('{{download_url}}', release_info['url'])
        changelog_lines.append(line)
    
    return "\n".join(changelog_lines)

def _post_new_release(reddit, page_url, config):
    with open(config['reddit']['templateFile'], 'r') as f:
        raw_template = f.read()

    # Clean the template by removing tutorial blocks
    ignore_block = config.get('skipContent', {})
    start_marker, end_marker = ignore_block.get('startTag'), ignore_block.get('endTag')
    if start_marker and end_marker and start_marker in raw_template:
        pattern = re.compile(f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
        clean_template = re.sub(pattern, '', raw_template)
    else:
        clean_template = raw_template

    post_body_template = clean_template.strip()
    
    # --- Placeholder Replacements ---
    # 1. Generate the changelog
    changelog = _generate_changelog(config)

    # 2. Prepare other placeholders
    initial_status_line = config['feedback']['statusLineFormat'].replace("{{status}}", config['feedback']['labels']['unknown'])
    placeholders = {
        "{{changelog}}": changelog,
        "{{bot_name}}": config['reddit']['botName'],
        "{{bot_repo}}": config['github']['botRepo'],
        "{{asset_name}}": config['github']['assetFileName'],
        "{{creator_username}}": config['reddit']['creator'],
        "{{initial_status}}": initial_status_line,
        "{{download_portal_url}}": page_url,
    }

    # 3. Apply all placeholders
    title = config['reddit']['postTitle']
    post_body = post_body_template
    for placeholder, value in placeholders.items():
        post_body = post_body.replace(placeholder, str(value))
        title = title.replace(placeholder, str(value)) # In case title uses placeholders

    print("Submitting new post to r/{}.format(config['reddit']['subreddit']))
    submission = reddit.subreddit(config['reddit']['subreddit']).submit(title, selftext=post_body)
    print(f"Post successful: {submission.shortlink}")
    return submission

def main():
    parser = argparse.ArgumentParser(description="Post a new release to Reddit.")
    parser.add_argument('--page-url', required=False, default='', help="URL to the GitHub Pages landing page.")
    args = parser.parse_args()
    config = load_config()

    print("Authenticating with Reddit...")
    reddit = init_reddit(config)

    print("Fetching existing posts to prepare for update...")
    existing_posts = get_bot_posts(reddit, config)
    
    # The script now generates the content from files, not args
    new_submission = _post_new_release(reddit, args.page_url, config)

    if existing_posts:
        print(f"Found {len(existing_posts)} older post(s) to update.")
        # The version is now generic, so we use the new post's title directly
        latest_release_details = {
            "title": new_submission.title,
            "url": new_submission.shortlink,
            "version": "latest" 
        }
        update_older_posts(existing_posts, latest_release_details, config)

    print("Updating state file to monitor latest post.")
    new_state = {
        "activePostId": new_submission.id,
        "lastCheckTimestamp": "2024-01-01T00:00:00Z",
        "currentIntervalSeconds": config['timing']['firstCheck'],
        "lastCommentCount": 0
    }
    save_bot_state(new_state)
    print("Post and update process complete.")

if __name__ == "__main__":
    main()
