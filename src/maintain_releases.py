import os
import sys
import requests
from helpers import load_config

def main():
    """
    Marks old GitHub releases with an [OUTDATED] prefix.
    """
    config = load_config()
    bot_repo = config['github']['botRepo']
    token = os.environ["GITHUB_TOKEN"]
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    releases_url = f"https://api.github.com/repos/{bot_repo}/releases"
    try:
        response = requests.get(releases_url, headers=headers)
        response.raise_for_status()
        releases = response.json()
    except requests.RequestException as e:
        print(f"::error::Could not fetch releases: {e}", file=sys.stderr)
        sys.exit(1)
    
    if not releases or len(releases) < 2:
        print("Not enough releases to mark any as outdated. Exiting.")
        sys.exit(0)
    
    latest_release_id = releases[0]['id']
    older_releases = releases[1:]
    
    print(f"Latest release is {releases[0]['tag_name']}. Checking {len(older_releases)} older release(s).")
    
    updated_count = 0
    for release in older_releases:
        release_id = release['id']
        current_title = release['name']
        
        if current_title.startswith('[OUTDATED] '):
            continue
        
        print(f"Updating release '{current_title}'...")
        
        new_title = f"[OUTDATED] {current_title}"
        update_url = f"https://api.github.com/repos/{bot_repo}/releases/{release_id}"
        payload = {"name": new_title}
        
        try:
            update_response = requests.patch(update_url, headers=headers, json=payload)
            update_response.raise_for_status()
            print(f"-> Successfully updated to '{new_title}'.")
            updated_count += 1
        except requests.RequestException as e:
            print(f"::warning::Failed to update release {release_id}. Status: {update_response.status_code}, Body: {update_response.text}")

    print(f"\nMaintenance complete. Updated {updated_count} release title(s).")

if __name__ == "__main__":
    main()
