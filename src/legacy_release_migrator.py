import os
import sys
from github import Github, GithubException
from helpers import load_config, parse_release_notes

def migrate_releases():
    """
    Performs a one-time migration of all legacy releases to a new, structured
    format in the release body by leveraging the centralized parser.
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

    updated_count = 0
    skipped_count = 0
    failed_count = 0

    for release in releases:
        # 1. Check if the release is already in the new, fully structured format
        if "app:" in release.body and "version:" in release.body and "asset_name:" in release.body:
            skipped_count += 1
            continue

        print(f"\n--- Migrating legacy release: {release.tag_name} ---")
        
        # 2. Use the one true parser to derive the release info
        parsed_info = parse_release_notes(release.body, release.tag_name, release.title, config)
        
        if not parsed_info:
            print(f"::error::Could not parse info for tag {release.tag_name}. Cannot migrate.")
            failed_count += 1
            continue

        app_id = parsed_info['app_id']
        version = parsed_info['version']
        asset_name = parsed_info['asset_name']
        
        print(f"  Parsed Info: App='{app_id}', Version='{version}', Asset='{asset_name}'")

        # 3. Construct the new structured body
        new_body = f"""app: {app_id}
version: {version}
asset_name: {asset_name}
"""
        
        # 4. Update the release on GitHub
        try:
            print(f"  Updating release '{release.tag_name}' with new structured body.")
            release.update_release(name=release.title, message=new_body)
            updated_count += 1
        except GithubException as e:
            print(f"::error::Failed to update release {release.tag_name}: {e}")
            failed_count += 1

    print(f"\nMigration complete. Updated: {updated_count}, Skipped (already modern): {skipped_count}, Failed: {failed_count}.")
    if failed_count > 0:
        sys.exit(1)

if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    import paths
    migrate_releases()