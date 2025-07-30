import os
import sys
import requests
from helpers import load_config

def get_all_bot_releases(bot_repo: str, token: str) -> list:
    """Fetches all releases from the bot's repository, handling pagination."""
    releases = []
    page = 1
    while True:
        print(f"Fetching page {page} of releases...")
        url = f"https://api.github.com/repos/{bot_repo}/releases?per_page=100&page={page}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if not data:
            break
        releases.extend(data)
        page += 1
    return releases

def main():
    """
    Finds legacy bot releases (e.g., 'bitlife-v1.2.3') and prepends '[OUTDATED]'
    to their titles if they don't already have it.
    """
    config = load_config()
    bot_repo = config['github']['botRepo']
    token = os.environ["GITHUB_TOKEN"]

    print(f"Fetching all releases for {bot_repo}...")
    all_releases = get_all_bot_releases(bot_repo, token)
    print(f"Found a total of {len(all_releases)} releases.")

    legacy_releases_to_update = []
    for release in all_releases:
        # A legacy release is defined by having a version in the tag like '-v1.2.3'
        is_legacy = "-v" in release.get('tag_name', '')
        is_outdated = release.get('name', '').startswith('[OUTDATED]')
        
        if is_legacy and not is_outdated:
            legacy_releases_to_update.append(release)

    if not legacy_releases_to_update:
        print("No legacy releases need to be updated. Exiting.")
        sys.exit(0)

    print(f"Found {len(legacy_releases_to_update)} legacy release(s) to mark as outdated.")
    
    updated_count = 0
    for release in legacy_releases_to_update:
        release_id = release['id']
        current_title = release['name']
        new_title = f"[OUTDATED] {current_title}"
        
        print(f"Updating release '{current_title}' (ID: {release_id})...")
        
        update_url = f"https://api.github.com/repos/{bot_repo}/releases/{release_id}"
        payload = {"name": new_title}
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }
        
        try:
            update_response = requests.patch(update_url, headers=headers, json=payload)
            update_response.raise_for_status()
            print(f"-> Successfully updated title to '{new_title}'.")
            updated_count += 1
        except requests.RequestException as e:
            print(f"::warning::Failed to update release {release_id}. Status: {update_response.status_code}, Body: {update_response.text}")

    print(f"\nMigration complete. Updated {updated_count} legacy release title(s).")

if __name__ == "__main__":
    main()
