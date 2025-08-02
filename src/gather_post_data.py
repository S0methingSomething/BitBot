import os
import sys
import json
from github import Github, GithubException
from packaging.version import parse as parse_version
from helpers import load_config, parse_release_notes

def main():
    config = load_config()
    g = Github(os.getenv("GITHUB_TOKEN"))
    bot_repo_name = config['github']['botRepo']
    
    try:
        bot_repo = g.get_repo(bot_repo_name)
        print(f"Fetching all releases from bot repository: {bot_repo_name}")
        bot_releases = bot_repo.get_releases()
    except GithubException as e:
        print(f"::error::Failed to get repositories: {e}")
        sys.exit(1)

    # --- Data Aggregation and Cleaning Pipeline ---
    
    # 1. Aggregate all releases, grouping them by app and version
    aggregated_data = {}
    for release in bot_releases:
        parsed_info = parse_release_notes(release.body, release.tag_name, release.title, config)
        if not parsed_info:
            print(f"::warning::Could not parse release tag {release.tag_name}. Skipping.")
            continue
        
        app_id = parsed_info['app_id']
        version = parsed_info['version']
        
        if app_id not in aggregated_data:
            aggregated_data[app_id] = {
                "display_name": parsed_info['display_name'],
                "releases_by_version": {}
            }
        
        if version not in aggregated_data[app_id]['releases_by_version']:
            aggregated_data[app_id]['releases_by_version'][version] = []

        download_url = None
        for asset in release.get_assets():
            if asset.name == parsed_info.get('asset_name'):
                download_url = asset.browser_download_url
                break
        
        if not download_url:
            print(f"::warning::No matching asset found for release {release.tag_name}. Skipping.")
            continue

        aggregated_data[app_id]['releases_by_version'][version].append({
            "version": version,
            "download_url": download_url,
            "published_at": release.published_at.isoformat(),
            "release_notes": release.body,
            "release_url": release.html_url,
            "tag_name": release.tag_name
        })

    # 2. De-duplicate and structure the final data
    final_data = {}
    for app_id, app_info in aggregated_data.items():
        clean_releases = []
        for version, release_group in app_info['releases_by_version'].items():
            if len(release_group) == 1:
                clean_releases.append(release_group[0])
            else:
                print(f"Found {len(release_group)} releases for {app_id} v{version}. Selecting the best one.")
                best_release = None
                for r in release_group:
                    if r['tag_name'].startswith(f"{app_id}-v"):
                        best_release = r
                        break
                if not best_release:
                    best_release = sorted(release_group, key=lambda x: x['published_at'], reverse=True)[0]
                clean_releases.append(best_release)

        # 3. Sort all releases by version to find the latest
        clean_releases.sort(key=lambda r: parse_version(r['version']), reverse=True)
        
        # 4. Create the final data structure with latest_release and previous_releases
        if clean_releases:
            final_data[app_id] = {
                "display_name": app_info['display_name'],
                "latest_release": clean_releases[0],
                "previous_releases": clean_releases[1:]
            }
        else:
             final_data[app_id] = {
                "display_name": app_info['display_name'],
                "latest_release": None,
                "previous_releases": []
            }

    # 5. Save the new, intelligent data structure
    os.makedirs(paths.DIST_DIR, exist_ok=True)
    with open(paths.RELEASES_JSON_FILE, 'w') as f:
        json.dump(final_data, f, indent=4)

    print(f"Successfully generated clean, structured release data at {paths.RELEASES_JSON_FILE}")

if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    import paths
    main()
