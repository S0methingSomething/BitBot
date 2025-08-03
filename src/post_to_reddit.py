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
    load_bot_state,
    save_bot_state,
)

# --- Constants ---
MAX_OUTBOUND_LINKS_ERROR = 8

def _count_outbound_links(text: str) -> int:
    url_pattern = re.compile(r'https?://[^\s/$.?#].[^\s]*|www\.[^\s/$.?#].[^\s]*')
    matches = url_pattern.findall(text)
    return len(set(matches))

def _generate_dynamic_title(config: dict, added: dict, updated: dict) -> str:
    num_added = len(added)
    num_updated = len(updated)
    total_changes = num_added + num_updated
    formats = config['reddit']['formats']['titles']
    
    def create_app_list(app_dict):
        parts = []
        for _, info in app_dict.items():
            display_name = info.get('display_name') or info.get('new', {}).get('display_name', 'Unknown App')
            version = info.get('version') or info.get('new', {}).get('version', '?.?.?')
            parts.append(f"{display_name} v{version}")
        return ", ".join(parts)

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
    post_mode = config['reddit'].get('postMode', 'landing_page')
    
    if post_mode == 'landing_page':
        key_suffix = 'landing'
    elif post_mode == 'direct_link':
        key_suffix = 'direct'
    else:
        key_suffix = 'landing' # Default fallback

    asset_name = config['github'].get('assetFileName', 'asset')
    formats = config['reddit']['formats']['changelog']
    sections = []

    def create_section(title, data, key_format):
        lines = [f"### {title}"]
        for _, info in data.items():
            line_format = formats.get(key_format)
            if not line_format:
                print(f"::warning::Changelog format for '{key_format}' not found in config.")
                continue
            
            if title == "Added":
                line = line_format.replace('{{display_name}}', info['display_name']).replace('{{asset_name}}', asset_name).replace('{{version}}', info['version']).replace('{{download_url}}', info['url'])
            elif title == "Updated":
                line = line_format.replace('{{display_name}}', info['new']['display_name']).replace('{{asset_name}}', asset_name).replace('{{new_version}}', info['new']['version']).replace('{{old_version}}', info['old']).replace('{{download_url}}', info['new']['url'])
            elif title == "Removed":
                 line = line_format.replace('{{display_name}}', info['display_name']).replace('{{asset_name}}', asset_name).replace('{{old_version}}', info['version'])
            lines.append(line)
        if len(lines) > 1:
            sections.append("\n".join(lines))

    if added: create_section("Added", added, f"added_{key_suffix}")
    if updated: create_section("Updated", updated, f"updated_{key_suffix}")
    if removed: create_section("Removed", removed, f"removed_{key_suffix}")
    
    return "\n\n".join(sections) if sections else "No new updates in this version."

def _generate_available_list(config: dict, all_releases_data: dict) -> str:
    formats = config['reddit']['formats']['table']
    header = formats.get('header', '| App | Asset | Version |')
    divider = formats.get('divider', '|---|---|---:|')
    line_format = formats.get('line', '| {{display_name}} | {{asset_name}} | v{{version}} |')
    table_lines = [header, divider]
    asset_name = config['github'].get('assetFileName', 'asset')
    sorted_apps = sorted(all_releases_data.items(), key=lambda item: item[1]['display_name'])
    for _, release_info in sorted_apps:
        if release_info.get('latest_release'):
            line = line_format.replace('{{display_name}}', release_info['display_name']).replace('{{asset_name}}', asset_name).replace('{{version}}', release_info['latest_release']['version'])
            table_lines.append(line)
    return "\n".join(table_lines)

def _generate_post_body(config: dict, changelog_data: dict, all_releases_data: dict, page_url: str) -> str:
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
    
    post_body = post_body_template
    for placeholder, value in placeholders.items():
        post_body = post_body.replace(placeholder, str(value))
    return post_body

def _post_new_release(reddit, title, post_body, config):
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
    parser.add_argument('--generate-only', action='store_true', help="Generate post content without posting to Reddit.")
    args = parser.parse_args()
    config = load_config()
    bot_state = load_bot_state()

    if not os.path.exists(paths.RELEASES_JSON_FILE):
        print(f"`{paths.RELEASES_JSON_FILE}` not found. Nothing to post.")
        sys.exit(0)
    with open(paths.RELEASES_JSON_FILE, 'r') as f:
        all_available_versions = json.load(f)

    is_manual_mode = config['reddit'].get('post_manually', False) or args.generate_only
    
    if is_manual_mode:
        print("---" + "-" * 10 + " MANUAL MODE " + "-" * 10 + "---")
        versions_to_check = bot_state['offline']['last_generated_versions']
    else:
        print("---" + "-" * 10 + " AUTOMATIC MODE " + "-" * 10 + "---")
        versions_to_check = bot_state['online']['last_posted_versions']

    added_apps, updated_apps, removed_apps = {}, {}, {}
    new_versions_state = versions_to_check.copy()

    for app_id, app_data in all_available_versions.items():
        if not app_data.get('latest_release'): continue
        
        latest_version_str = app_data['latest_release']['version']
        current_version_str = versions_to_check.get(app_id, "0.0.0")

        if parse_version(latest_version_str) > parse_version(current_version_str):
            new_versions_state[app_id] = latest_version_str
            if current_version_str == "0.0.0":
                added_apps[app_id] = {"display_name": app_data['display_name'], "version": latest_version_str, "url": app_data['latest_release']['download_url']}
            else:
                updated_apps[app_id] = {"new": {"display_name": app_data['display_name'], "version": latest_version_str, "url": app_data['latest_release']['download_url']}, "old": current_version_str}

    changelog_data = {"added": added_apps, "updated": updated_apps, "removed": removed_apps}
    if not any(changelog_data.values()):
        print("No changes detected. State is up-to-date.")
        sys.exit(0)

    title = _generate_dynamic_title(config, added_apps, updated_apps)
    body = _generate_post_body(config, changelog_data, all_available_versions, args.page_url or "https://example.com/preview-link")

    if is_manual_mode:
        os.makedirs(paths.DIST_DIR, exist_ok=True)
        title_path = os.path.join(paths.DIST_DIR, 'post_title.txt')
        body_path = os.path.join(paths.DIST_DIR, 'post_body.md')
        with open(title_path, 'w') as f: f.write(title)
        with open(body_path, 'w') as f: f.write(body)
        bot_state['offline']['last_generated_versions'] = new_versions_state
        save_bot_state(bot_state)
        print(f"Successfully generated post files in {paths.DIST_DIR} and updated offline state.")
        sys.exit(0)

    # --- Automatic Posting Logic ---
    reddit = init_reddit(config)
    existing_posts = get_bot_posts(reddit, config)
    new_submission = _post_new_release(reddit, title, body, config)
    
    if existing_posts:
        update_older_posts(existing_posts, {"title": new_submission.title, "url": new_submission.shortlink, "version": "latest"})
    
    bot_state['online']['last_posted_versions'] = new_versions_state
    bot_state['online']['activePostId'] = new_submission.id
    save_bot_state(bot_state)
    print("Post and update process complete. Online state updated.")

if __name__ == "__main__":
    main()