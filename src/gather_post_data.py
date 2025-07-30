import os
import sys
import json
import re
from helpers import load_config
from typing import List, Dict

def run_command(command: List[str], check: bool = True) -> str:
    """Runs a shell command and returns its stdout."""
    print(f"Executing: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True, check=check)
    return result.stdout

def get_all_bot_releases(bot_repo: str) -> List[Dict]:
    """Fetches all releases from the bot's repository, handling pagination."""
    releases = []
    page = 1
    while True:
        print(f"Fetching page {page} of bot releases...")
        command = [
            'gh', 'api',
            f"/repos/{bot_repo}/releases?per_page=100&page={page}"
        ]
        output = run_command(command)
        data = json.loads(output)
        if not data:
            break
        releases.extend(data)
        page += 1
    return releases

def main():
    """
    Gathers all valid releases from the bot's own repository and creates a
    definitive `releases.json` file to be used by downstream jobs.
    """
    config = load_config()
    bot_repo = config['github']['botRepo']
    apps_config = config['apps']
    app_map_by_id = {app['id']: app['displayName'] for app in apps_config}

    print(f"Fetching all releases for {bot_repo} to build authoritative release list.")
    all_releases = get_all_bot_releases(bot_repo)
    print(f"Found a total of {len(all_releases)} releases.")

    releases_data = {}
    # Regex to parse tags like 'bitlife-v3.20.1'
    tag_pattern = re.compile(r"([a-z_]+)-v([\d\.]+)")

    for release in all_releases:
        tag_name = release.get('tag_name', '')
        match = tag_pattern.match(tag_name)
        
        if not match:
            print(f"Skipping release with non-standard tag: {tag_name}")
            continue
            
        app_id = match.group(1)
        version = match.group(2)
        
        if app_id not in app_map_by_id:
            print(f"Skipping release for unrecognized app_id: {app_id}")
            continue

        # Find the asset download URL
        asset_name = config['github']['assetFileName']
        asset = next((a for a in release.get('assets', []) if a['name'] == asset_name), None)
        if not asset:
            print(f"::warning::Release {tag_name} is missing the asset '{asset_name}'. Skipping.")
            continue

        releases_data[app_id] = {
            "display_name": app_map_by_id[app_id],
            "version": version,
            "url": asset['browser_download_url']
        }

    if not releases_data:
        print("No valid, tagged releases with assets found. No data to post.")
        # We still write an empty JSON to signify the process ran correctly
        releases_data = {}

    output_dir = '../dist'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'releases.json')
    with open(output_path, 'w') as f:
        json.dump(releases_data, f, indent=2)

    print(f"Successfully created authoritative `releases.json` with {len(releases_data)} app(s).")
    
    # Set output for the workflow
    with open(os.environ.get('GITHUB_OUTPUT', ''), 'a') as f:
        # This output is now the primary signal for whether to post.
        # The old output from release_manager is no longer used.
        post_needed = "true" if releases_data else "false"
        print(f"new_releases_found={post_needed}", file=f)


if __name__ == "__main__":
    # This script needs subprocess, so import it here
    import subprocess
    main()
