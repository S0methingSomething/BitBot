import os
import sys
import json
import re
import argparse
from packaging.version import parse as parse_version
import paths
from helpers import (
    load_config,
    init_reddit,
    get_bot_posts,
    update_older_posts,
    save_bot_state,
    parse_versions_from_post,
)

def _generate_changelog(config: dict, added: dict, updated: dict, removed: dict) -> str:
    """Generates a semantic changelog with Added, Updated, and Removed sections."""
    post_mode = config['reddit'].get('postMode', 'landing_page')
    asset_name = config['github'].get('assetFileName', 'asset')
    
    sections = []

    # --- Added Section ---
    if added:
        key = f"changelog_format_added_{post_mode}"
        line_format = config['reddit'].get(key)
        lines = ["### Added"]
        for app_id, info in added.items():
            line = line_format.replace('{{display_name}}', info['display_name'])
            line = line.replace('{{asset_name}}', asset_name)
            line = line.replace('{{version}}', info['version'])
            line = line.replace('{{download_url}}', info['url'])
            lines.append(line)
        sections.append("\n".join(lines))

    # --- Updated Section ---
    if updated:
        key = f"changelog_format_updated_{post_mode}"
        line_format = config['reddit'].get(key)
        lines = ["### Updated"]
        for app_id, info in updated.items():
            line = line_format.replace('{{display_name}}', info['new']['display_name'])
            line = line.replace('{{asset_name}}', asset_name)
            line = line.replace('{{new_version}}', info['new']['version'])
            line = line.replace('{{old_version}}', info['old'])
            line = line.replace('{{download_url}}', info['new']['url'])
            lines.append(line)
        sections.append("\n".join(lines))

    # --- Removed Section ---
    if removed:
        key = f"changelog_format_removed_{post_mode}"
        line_format = config['reddit'].get(key)
        lines = ["### Removed"]
        for app_id, info in removed.items():
            line = line_format.replace('{{display_name}}', info['display_name'])
            line = line.replace('{{asset_name}}', asset_name)
            line = line.replace('{{old_version}}', info['version'])
            lines.append(line)
        sections.append("\n".join(lines))

    return "\n\n".join(sections) if sections else "No new updates in this version."

def _generate_available_list(config: dict, all_releases_data: dict) -> str:
    """Generates a Markdown table of all available releases."""
    header = config['reddit'].get('available_table_header', '| App | Asset | Version |')
    divider = config['reddit'].get('available_table_divider', '|---|---|---:|')
    line_format = config['reddit'].get('available_line_format', '| {{display_name}} | {{asset_name}} | v{{version}} |')

    table_lines = [header, divider]
    asset_name = config['github'].get('assetFileName', 'asset')
    sorted_apps = sorted(all_releases_data.items(), key=lambda item: item[1]['display_name'])

    for app_id, release_info in sorted_apps:
        line = line_format.replace('{{display_name}}', release_info['display_name'])
        line = line.replace('{{asset_name}}', asset_name)
        line = line.replace('{{version}}', release_info['version'])
        table_lines.append(line)
        
    return "\n".join(table_lines)

def _post_new_release(reddit, page_url, config, changelog_data, all_releases_data):
    template_name = os.path.basename(config['reddit']['templateFile'])
    template_path = paths.get_template_path(template_name)
    with open(template_path, 'r') as f:
        raw_template = f.read()

    # Clean template
    ignore_block = config.get('skipContent', {})
    start_marker, end_marker = ignore_block.get('startTag'), ignore_block.get('endTag')
    if start_marker and end_marker and start_marker in raw_template:
        pattern = re.compile(f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
        clean_template = re.sub(pattern, '', raw_template)
    else:
        clean_template = raw_template
    post_body_template = clean_template.strip()
    
    # Generate content
    changelog = _generate_changelog(config, **changelog_data)
    available_list = _generate_available_list(config, all_releases_data)
    initial_status_line = config['feedback']['statusLineFormat'].replace("{{status}}", config['feedback']['labels']['unknown'])
    
    # Populate placeholders
    placeholders = {
        "{{changelog}}": changelog,
        "{{available_list}}": available_list,
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

    print("Submitting new post to r/{}...".format(config['reddit']['subreddit']))
    submission = reddit.subreddit(config['reddit']['subreddit']).submit(title, selftext=post_body)
    print(f"Post successful: {submission.shortlink}")
    return submission

def main():
    parser = argparse.ArgumentParser(description="Post a new release to Reddit if it's out of date.")
    parser.add_argument('--page-url', required=False, default='', help="URL to the GitHub Pages landing page.")
    args = parser.parse_args()
    config = load_config()

    if not os.path.exists(paths.RELEASES_JSON_FILE):
        print(f"`{paths.RELEASES_JSON_FILE}` not found. Nothing to post.")
        sys.exit(0)
    with open(paths.RELEASES_JSON_FILE, 'r') as f:
        all_available_versions = json.load(f)

    reddit = init_reddit(config)
    existing_posts = get_bot_posts(reddit, config)
    
    versions_on_reddit = {}
    if existing_posts:
        versions_on_reddit = parse_versions_from_post(existing_posts[0], config)

    # Categorize changes
    added_apps = {}
    updated_apps = {}
    
    available_app_ids = set(all_available_versions.keys())
    reddit_app_ids = set(versions_on_reddit.keys())

    for app_id, release_info in all_available_versions.items():
        if app_id not in versions_on_reddit:
            added_apps[app_id] = release_info
        else:
            latest_version = parse_version(release_info['version'])
            reddit_version = parse_version(versions_on_reddit.get(app_id, "0.0.0"))
            if latest_version > reddit_version:
                updated_apps[app_id] = {"new": release_info, "old": str(reddit_version)}

    removed_apps = {}
    app_map_by_id = {app['id']: app for app in config.get('apps', [])}
    for app_id in reddit_app_ids - available_app_ids:
        removed_apps[app_id] = {
            "display_name": app_map_by_id.get(app_id, {}).get('displayName', app_id),
            "version": versions_on_reddit[app_id]
        }

    changelog_data = {"added": added_apps, "updated": updated_apps, "removed": removed_apps}
    if not any(changelog_data.values()):
        print("Reddit is already up-to-date. No new post needed.")
        sys.exit(0)

    print(f"Found changes: {len(added_apps)} added, {len(updated_apps)} updated, {len(removed_apps)} removed. Proceeding to post.")
    new_submission = _post_new_release(reddit, args.page_url, config, changelog_data, all_available_versions)

    if existing_posts:
        update_older_posts(existing_posts, {"title": new_submission.title, "url": new_submission.shortlink, "version": "latest"})

    print("Updating state file to monitor latest post.")
    save_bot_state({
        "activePostId": new_submission.id,
        "lastCheckTimestamp": "2024-01-01T00:00:00Z",
        "currentIntervalSeconds": config['timing']['firstCheck'],
        "lastCommentCount": 0
    })
    print("Post and update process complete.")

if __name__ == "__main__":
    main()
