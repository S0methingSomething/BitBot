import os
import sys
import json
import re
import argparse
from packaging.version import parse as parse_version
from helpers (
    load_config,
    init_reddit,
    get_bot_posts,
    update_older_posts,
    save_bot_state,
    parse_versions_from_post,
)

def _generate_changelog(config: dict, releases_data: dict) -> str:
    """Generates a changelog string from the releases data."""
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

def _post_new_release(reddit, page_url, config, releases_data):
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
    
    changelog = _generate_changelog(config, releases_data)
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

    title = config['reddit']['postTitle']
    post_body = post_body_template
    for placeholder, value in placeholders.items():
        post_body = post_body.replace(placeholder, str(value))
        title = title.replace(placeholder, str(value))

    print("Submitting new post to r/{}...".format(config['reddit']['subreddit']))
    submission = reddit.subreddit(config['reddit']['subreddit']).submit(title, selftext=post_body)
    print(f"Post successful: {submission.shortlink}")
    return submission

def main():
    parser = argparse.ArgumentParser(description="Post a new release to Reddit if it's out of date.")
    parser.add_argument('--page-url', required=False, default='', help="URL to the GitHub Pages landing page.")
    args = parser.parse_args()
    config = load_config()

    # Load the latest versions that SHOULD be on Reddit
    releases_path = '../dist/releases.json'
    if not os.path.exists(releases_path):
        print("`releases.json` not found. Nothing to post.")
        sys.exit(0)
    with open(releases_path, 'r') as f:
        latest_versions = json.load(f)

    print("Authenticating with Reddit...")
    reddit = init_reddit(config)

    print("Fetching latest bot post from Reddit...")
    existing_posts = get_bot_posts(reddit, config)
    
    versions_on_reddit = {}
    if existing_posts:
        latest_post = existing_posts[0]
        print(f"Found latest post: {latest_post.id} - '{latest_post.title}'")
        versions_on_reddit = parse_versions_from_post(latest_post, config)
    else:
        print("No previous posts found on Reddit.")

    # Compare versions to see if an update is needed
    is_update_needed = False
    for app_id, release_info in latest_versions.items():
        latest_version = parse_version(release_info['version'])
        reddit_version_str = versions_on_reddit.get(app_id, "0.0.0")
        reddit_version = parse_version(reddit_version_str)
        
        if latest_version > reddit_version:
            print(f"Update needed for '{app_id}': Reddit has v{reddit_version}, latest is v{latest_version}.")
            is_update_needed = True
            break # One change is enough to trigger a new post

    if not is_update_needed:
        print("Reddit is already up-to-date with the latest versions. No new post needed.")
        sys.exit(0)

    print("Update required. Proceeding to post a new release announcement.")
    new_submission = _post_new_release(reddit, args.page_url, config, latest_versions)

    # Update older posts (which now includes the post we just superseded)
    if existing_posts:
        print(f"Found {len(existing_posts)} older post(s) to update.")
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