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

def _post_new_release(reddit, version, urls, page_url, config):
    with open(config['reddit']['templateFile'], 'r') as f:
        raw_template = f.read()

    ignore_block = config.get('skipContent', {})
    start_marker, end_marker = ignore_block.get('startTag'), ignore_block.get('endTag')
    if start_marker and end_marker and start_marker in raw_template:
        pattern = re.compile(f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
        clean_template = re.sub(pattern, '', raw_template)
    else:
        clean_template = raw_template

    post_body_template = clean_template.strip()
    initial_status_line = config['feedback']['statusLineFormat'].replace("{{status}}", config['feedback']['labels']['unknown'])
    
    placeholders = {
        "{{version}}": version,
        "{{bot_name}}": config['reddit']['botName'],
        "{{bot_repo}}": config['github']['botRepo'],
        "{{asset_name}}": config['github']['assetFileName'],
        "{{creator_username}}": config['reddit']['creator'],
        "{{initial_status}}": initial_status_line,
    }

    post_mode = config['reddit'].get('postMode', 'direct_link')
    if post_mode == 'landing_page':
        print("Post mode is 'landing_page'. Using portal URL.")
        placeholders["{{download_portal_url}}"] = page_url
    else:
        print("Post mode is 'direct_link'. Using direct URLs.")
        url_map = json.loads(urls)
        for app in config["apps"]:
            app_id = app['id']
            placeholders[f"direct_download_url_{app_id}"] = url_map.get(app_id, '')

    title = config['reddit']['postTitle']
    post_body = post_body_template
    for placeholder, value in placeholders.items():
        post_body = post_body.replace(placeholder, str(value))
        title = title.replace(placeholder, str(value))

    print(f"Submitting new post for v{version} to r/{config['reddit']['subreddit']}...")
    submission = reddit.subreddit(config['reddit']['subreddit']).submit(title, selftext=post_body)
    print(f"Post successful: {submission.shortlink}")
    return submission

def main():
    parser = argparse.ArgumentParser(description="Post a new release to Reddit.")
    parser.add_argument('--version', required=True)
    parser.add_argument('--urls', required=True)
    parser.add_argument('--page-url', required=False, default='', help="URL to the GitHub Pages landing page.")
    args = parser.parse_args()
    config = load_config()

    print("Authenticating with Reddit...")
    reddit = init_reddit(config)

    print("Fetching existing posts to prepare for update...")
    existing_posts = get_bot_posts(reddit, config)
    new_submission = _post_new_release(reddit, args.version, args.urls, args.page_url, config)

    if existing_posts:
        print(f"Found {len(existing_posts)} older post(s) to update.")
        latest_release_details = {
            "title": new_submission.title,
            "url": new_submission.shortlink,
            "version": args.version
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