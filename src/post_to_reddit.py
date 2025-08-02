import os
import sys
import json
import re
import argparse
from datetime import datetime
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

# --- Constants ---
MAX_OUTBOUND_LINKS_ERROR = 8

def _count_outbound_links(text: str) -> int:
    url_pattern = re.compile(r'https?://[^\s/$.?#].[^\s]*|www\.[^\s/$.?#].[^\s]*')
    matches = url_pattern.findall(text)
    return len(set(matches))

def _generate_dynamic_title(config: dict, added: dict, updated: dict) -> str:
    # This function remains the same
    num_added = len(added)
    num_updated = len(updated)
    total_changes = num_added + num_updated
    formats = config['reddit']['formats']['titles']
    def create_app_list(app_dict):
        return ", ".join([f"{info['display_name']} v{info.get('version') or info.get('new', {}).get('version')}" for _, info in app_dict.items()])
    added_list = create_app_list(added)
    updated_list = create_app_list(updated)
    title_key, placeholders = None, {}
    if num_added > 0 and num_updated == 0:
        title_key = "added_only"
        placeholders = {"{{added_list}}": added_list}
    elif num_added == 0 and num_updated > 0:
        title_key = "updated_only_single" if num_updated == 1 else "updated_only_multi"
        placeholders = {"{{updated_list}}": updated_list}
    elif num_added > 0 and num_updated > 0:
        title_key = "mixed_single_update" if num_updated == 1 else "mixed_multi_update"
        placeholders = {"{{added_list}}": added_list, "{{updated_list}}": updated_list}
    if total_changes > 3 or title_key is None:
        title_key = "generic"
        placeholders = {"{{date}}": datetime.utcnow().strftime('%Y-%m-%d')}
    title_format = formats.get(title_key, "[BitBot] Default Fallback Title")
    final_title = title_format
    for ph, value in placeholders.items():
        final_title = final_title.replace(ph, value)
    return final_title

def _generate_changelog(config: dict, added: dict, updated: dict, removed: dict) -> str:
    # This function remains the same
    post_mode = config['reddit'].get('postMode', 'landing_page')
    asset_name = config['github'].get('assetFileName', 'asset')
    formats = config['reddit']['formats']['changelog']
    sections = []
    if added:
        key = f"added_{post_mode}"
        line_format = formats.get(key)
        if line_format:
            lines = ["### Added"]
            for app_id, info in added.items():
                line = line_format.replace('{{display_name}}', info['display_name']).replace('{{asset_name}}', asset_name).replace('{{version}}', info['version']).replace('{{download_url}}', info['url'])
                lines.append(line)
            sections.append("\n".join(lines))
    if updated:
        key = f"updated_{post_mode}"
        line_format = formats.get(key)
        if line_format:
            lines = ["### Updated"]
            for app_id, info in updated.items():
                line = line_format.replace('{{display_name}}', info['new']['display_name']).replace('{{asset_name}}', asset_name).replace('{{new_version}}', info['new']['version']).replace('{{old_version}}', info['old']).replace('{{download_url}}', info['new']['url'])
                lines.append(line)
            sections.append("\n".join(lines))
    if removed:
        key = f"removed_{post_mode}"
        line_format = formats.get(key)
        if line_format:
            lines = ["### Removed"]
            for app_id, info in removed.items():
                line = line_format.replace('{{display_name}}', info['display_name']).replace('{{asset_name}}', asset_name).replace('{{old_version}}', info['version'])
                lines.append(line)
            sections.append("\n".join(lines))
    return "\n\n".join(sections) if sections else "No new updates in this version."

def _generate_available_list(config: dict, all_releases_data: dict) -> str:
    # This function remains the same
    formats = config['reddit']['formats']['table']
    header = formats.get('header', '| App | Asset | Version |')
    divider = formats.get('divider', '|---|---|---:|')
    line_format = formats.get('line', '| {{display_name}} | {{asset_name}} | v{{version}} |')
    table_lines = [header, divider]
    asset_name = config['github'].get('assetFileName', 'asset')
    sorted_apps = sorted(all_releases_data.items(), key=lambda item: item[1]['display_name'])
    for app_id, release_info in sorted_apps:
        line = line_format.replace('{{display_name}}', release_info['display_name']).replace('{{asset_name}}', asset_name).replace('{{version}}', release_info['latest_release']['version'])
        table_lines.append(line)
    return "\n".join(table_lines)

def _post_new_release(reddit, page_url, config, changelog_data, all_releases_data):
    # This function remains mostly the same
    template_name = os.path.basename(config['reddit']['templates']['post'])
    template_path = paths.get_template_path(template_name)
    with open(template_path, 'r') as f:
        raw_template = f.read()
    ignore_block = config.get('skipContent', {})
    start_marker, end_marker = ignore_block.get('startTag'), ignore_block.get('endTag')
    if start_marker and end_marker and start_marker in raw_template:
        pattern = re.compile(f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
        clean_template = re.sub(pattern, '', raw_template)
    else:
        clean_template = raw_template
    post_body_template = clean_template.strip()
    changelog = _generate_changelog(config, **changelog_data)
    available_list = _generate_available_list(config, all_releases_data)
    initial_status_line = config['feedback']['statusLineFormat'].replace("{{status}}", config['feedback']['labels']['unknown'])
    placeholders = {
        "{{changelog}}": changelog, "{{available_list}}": available_list,
        "{{bot_name}}": config['reddit']['botName'], "{{bot_repo}}": config['github']['botRepo'],
        "{{asset_name}}": config['github']['assetFileName'], "{{creator_username}}": config['reddit']['creator'],
        "{{initial_status}}": initial_status_line, "{{download_portal_url}}": page_url,
    }
    title = _generate_dynamic_title(config, changelog_data['added'], changelog_data['updated'])
    post_body = post_body_template
    for placeholder, value in placeholders.items():
        post_body = post_body.replace(placeholder, str(value))
    link_count = _count_outbound_links(post_body)
    warn_threshold = config.get('safety', {}).get('max_outbound_links_warn', 5)
    print(f"Post analysis: Found {link_count} unique outbound link(s).")
    if link_count > MAX_OUTBOUND_LINKS_ERROR:
        print(f"::error::Post contains {link_count} links, which exceeds the hardcoded safety limit of {MAX_OUTBOUND_LINKS_ERROR}. Aborting.")
        sys.exit(1)
    if link_count > warn_threshold:
        print(f"::warning::Post contains {link_count} links, which is above the warning threshold of {warn_threshold}.")
    print(f"Submitting new post to r/{config['reddit']['subreddit']}...")
    print(f"Title: {title}")
    submission = reddit.subreddit(config['reddit']['subreddit']).submit(title, selftext=post_body)
    print(f"Post successful: {submission.shortlink}")
    return submission

def main():
    parser = argparse.ArgumentParser(description="Post a new release to Reddit if it's out of date.")
    parser.add_argument('--page-url', required=False, default='', help="URL to the GitHub Pages landing page.")
    parser.add_argument('--dry-run', action='store_true', help="Run the script without actually posting to Reddit.")
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

    added_apps, updated_apps, removed_apps = {}, {}, {}
    
    for app_id, app_data in all_available_versions.items():
        if not app_data.get('latest_release'):
            continue
        
        latest_version_str = app_data['latest_release']['version']
        reddit_version_str = versions_on_reddit.get(app_id, "0.0.0")

        if parse_version(latest_version_str) > parse_version(reddit_version_str):
            if reddit_version_str == "0.0.0":
                added_apps[app_id] = {"display_name": app_data['display_name'], "version": latest_version_str, "url": app_data['latest_release']['download_url']}
            else:
                updated_apps[app_id] = {"new": {"display_name": app_data['display_name'], "version": latest_version_str, "url": app_data['latest_release']['download_url']}, "old": reddit_version_str}

    # This logic for removed apps needs to be re-evaluated, but is out of scope of the main bug
    # For now, we focus on the main posting logic.

    changelog_data = {"added": added_apps, "updated": updated_apps, "removed": removed_apps}
    if not any(changelog_data.values()):
        print("Reddit is already up-to-date. No new post needed.")
        sys.exit(0)

    print(f"Found changes: {len(added_apps)} added, {len(updated_apps)} updated, {len(removed_apps)} removed. Proceeding to post.")
    
    if args.dry_run:
        # Dry run logic remains the same
        title = _generate_dynamic_title(config, added_apps, updated_apps)
        print("\n--- DRY RUN ---")
        print("Title:", title)
        # ... (rest of dry run logic)
        sys.exit(0)

    new_submission = _post_new_release(reddit, args.page_url, config, changelog_data, all_available_versions)

    if existing_posts:
        update_older_posts(existing_posts, {"title": new_submission.title, "url": new_submission.shortlink, "version": "latest"})

    save_bot_state({
        "activePostId": new_submission.id,
        "lastCheckTimestamp": "2024-01-01T00:00:00Z",
        "currentIntervalSeconds": config['timing']['firstCheck'],
        "lastCommentCount": 0
    })
    print("Post and update process complete.")

if __name__ == "__main__":
    main()
