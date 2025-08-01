import os
import sys
import re
from github import Github, GithubException
from helpers import load_config

def migrate_releases():
    """
    Performs a one-time migration of all legacy releases to a new, structured
    format in the release body.
    """
    config = load_config()
    g = Github(os.getenv("GITHUB_TOKEN"))
    bot_repo_name = config['github']['botRepo']
    
    try:
        repo = g.get_repo(bot_repo_name)
        releases = repo.get_releases()
        print(f"Found {releases.totalCount} releases in {bot_repo_name}. Analyzing for migration...")
    except GithubException as e:
        print(f"::error::Failed to get repository or releases: {e}")
        sys.exit(1)

    app_map_by_id = {app['id']: app for app in config.get('apps', [])}
    updated_count = 0
    skipped_count = 0

    for release in releases:
        # 1. Check if the release is already in the new format
        if "app:" in release.body and "version:" in release.body:
            skipped_count += 1
            continue

        print(f"\n--- Migrating legacy release: {release.tag_name} ---")
        
        # 2. Intelligently parse the legacy tag and title
        app_id = None
        version = None
        
        # Try parsing from tag first (e.g., "bitlife-v3.19.5")
        for configured_app_id in app_map_by_id.keys():
            if release.tag_name.lower().startswith(f"{configured_app_id.lower()}-v"):
                app_id = configured_app_id
                version_parts = release.tag_name.split('-v')
                if len(version_parts) > 1:
                    version = version_parts[1]
                break
        
        # If tag parsing failed, try parsing from the title (e.g., "BitLife MonetizationVars v3.19.5")
        if not app_id or not version:
            for configured_app_id, app_details in app_map_by_id.items():
                display_name = app_details['displayName']
                match = re.search(f"{re.escape(display_name)}.*?v([\\d\\.]+)", release.title, re.IGNORECASE)
                if match:
                    app_id = configured_app_id
                    version = match.group(1)
                    break

        # 3. Apply fallback logic if parsing failed
        if not app_id:
            app_id = "bitlife" # Fallback app_id
            print(f"::warning::Could not determine app from tag/title. Falling back to '{app_id}'.")

        if not version:
            # Fallback to parsing version from title like "MonetizationVars 3.19.4"
            match = re.search(r'(\d+\.\d+\.\d+)', release.title)
            if match:
                version = match.group(1)
            else:
                print(f"::error::Could not determine version for tag {release.tag_name}. Cannot migrate.")
                continue

        asset_name = config['github'].get('assetFileName', 'MonetizationVars') # Fallback asset_name

        print(f"  Parsed Info: App='{app_id}', Version='{version}', Asset='{asset_name}'")

        # 4. Construct the new structured body
        new_body = f"""app: {app_id}
version: {version}
asset_name: {asset_name}
"""
        
        # 5. Update the release on GitHub
        try:
            print(f"  Updating release '{release.tag_name}' with new structured body.")
            release.update_release(name=release.title, message=new_body, prerelease=release.prerelease, draft=release.draft)
            updated_count += 1
        except GithubException as e:
            print(f"::error::Failed to update release {release.tag_name}: {e}")

    print(f"\nMigration complete. Updated: {updated_count}, Skipped (already modern): {skipped_count}.")

if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    import paths
    migrate_releases()