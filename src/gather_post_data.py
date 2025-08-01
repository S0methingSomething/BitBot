import os
import sys
import json
from github import Github, GithubException
from helpers import load_config, parse_release_notes

def main():
    config = load_config()
    g = Github(os.getenv("GITHUB_TOKEN"))
    bot_repo_name = config['github']['botRepo']
    source_repo_name = config['github']['sourceRepo']
    
    try:
        bot_repo = g.get_repo(bot_repo_name)
        source_repo = g.get_repo(source_repo_name)
    except GithubException as e:
        print(f"::error::Failed to get repositories: {e}")
        sys.exit(1)

    print(f"Fetching all releases from bot repository: {bot_repo_name}")
    bot_releases = bot_repo.get_releases()
    
    all_apps_data = {}

    # 1. Build the base history from the bot's own releases
    for release in bot_releases:
        parsed_info = parse_release_notes(release.body, release.tag_name, config)
        if not parsed_info:
            print(f"::warning::Could not parse release notes for tag {release.tag_name}. Skipping.")
            continue
        
        app_id = parsed_info['app_id']
        
        if app_id not in all_apps_data:
            all_apps_data[app_id] = {
                "display_name": parsed_info['display_name'],
                "releases": []
            }
            
        # Find the asset for this release
        download_url = None
        for asset in release.get_assets():
            if asset.name == config['github']['assetFileName']:
                download_url = asset.browser_download_url
                break
        
        if not download_url:
            print(f"::warning::No matching asset found for release {release.tag_name}. Skipping.")
            continue

        all_apps_data[app_id]['releases'].append({
            "version": parsed_info['version'],
            "download_url": download_url,
            "published_at": release.published_at.isoformat(),
            "release_notes": release.body,
            "release_url": release.html_url
        })

    print(f"Found {len(all_apps_data)} apps with release history in the bot repo.")

    # 2. Augment with any newer releases from the source repo
    print(f"Fetching releases from source repository: {source_repo_name} to check for newer versions.")
    source_releases = source_repo.get_releases()
    
    for release in source_releases:
        parsed_info = parse_release_notes(release.body, config)
        if not parsed_info:
            continue
            
        app_id = parsed_info['app_id']
        
        # Check if this release is newer than what we have
        if app_id in all_apps_data:
            bot_versions = {r['version'] for r in all_apps_data[app_id]['releases']}
            if parsed_info['version'] not in bot_versions:
                 print(f"Found new version {parsed_info['version']} for {app_id} in source repo that is not in bot repo. This will be handled by release_manager.py, not here.")

    # 3. Sort all release lists by version (descending)
    from packaging.version import parse as parse_version
    for app_id in all_apps_data:
        all_apps_data[app_id]['releases'].sort(key=lambda r: parse_version(r['version']), reverse=True)

    # 4. Save the rich data structure
    output_dir = os.path.dirname(paths.RELEASES_JSON_FILE)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    with open(paths.RELEASES_JSON_FILE, 'w') as f:
        json.dump(all_apps_data, f, indent=4)

    print(f"Successfully generated rich release data at {paths.RELEASES_JSON_FILE}")

if __name__ == "__main__":
    # Add the project root to the Python path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    import paths
    main()