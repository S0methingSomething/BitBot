import os
import sys
import json
import subprocess
from typing import List, Dict

from helpers import load_config, load_release_state, save_release_state, parse_release_notes, load_changelog, save_changelog
import paths

def run_command(command: List[str], check: bool = True) -> subprocess.CompletedProcess:
    """Runs a shell command and returns its result."""
    print(f"Executing: {' '.join(command)}")
    return subprocess.run(command, capture_output=True, text=True, check=check)

def get_github_data(url: str) -> Dict | List:
    """Fetches data from the GitHub API using the gh cli."""
    command = ['gh', 'api', url]
    result = run_command(command)
    return json.loads(result.stdout)

def get_source_releases(repo: str) -> List[Dict]:
    """Gets the last 30 releases from the source repository."""
    print(f"Fetching latest releases from source repo: {repo}")
    return get_github_data(f"/repos/{repo}/releases?per_page=30")

def check_if_bot_release_exists(bot_repo: str, tag: str) -> bool:
    """Checks if a release with the given tag exists in the bot repo."""
    try:
        run_command(['gh', 'release', 'view', tag, '--repo', bot_repo])
        print(f"Release '{tag}' already exists. Skipping.")
        return True
    except subprocess.CalledProcessError:
        return False

def download_asset(source_repo: str, release_id: int, asset_name: str) -> str:
    """Downloads a specific asset from a specific release."""
    print(f"Downloading asset '{asset_name}' from release ID {release_id}")
    
    assets = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    asset_id = next((asset['id'] for asset in assets if asset['name'] == asset_name), None)

    if not asset_id:
        raise FileNotFoundError(f"Asset '{asset_name}' not found in release {release_id}")

    download_url = f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    output_path = os.path.join(paths.DIST_DIR, f"original_{asset_name}")

    run_command([
        'curl', '-sL', '-J',
        '-H', 'Accept: application/octet-stream',
        '-H', f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
        '-o', output_path,
        download_url
    ])
    return output_path

def patch_file(original_path: str, asset_name: str) -> str:
    """Patches the downloaded file using the Python script."""
    patched_path = os.path.join(paths.DIST_DIR, asset_name)
    print(f"Patching '{original_path}' to '{patched_path}' with Python script.")
    run_command(['python', 'patch_file.py', original_path, patched_path])
    return patched_path

def create_bot_release(bot_repo: str, tag: str, title: str, notes: str, file_path: str):
    """Creates a new release in the bot repository."""
    print(f"Creating new release '{tag}' in {bot_repo}")
    run_command([
        'gh', 'release', 'create', tag,
        '--repo', bot_repo,
        '--title', title,
        '--notes', notes,
        file_path
    ])

def main():
    config = load_config()
    os.makedirs(paths.DIST_DIR, exist_ok=True)
    source_repo = config['github']['sourceRepo']
    bot_repo = config['github']['botRepo']
    
    processed_release_ids = load_release_state()
    all_source_releases = get_source_releases(source_repo)
    
    new_releases = [r for r in all_source_releases if r['id'] not in processed_release_ids]
    
    if not new_releases:
        print("No new source releases found to process.")
        with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
            print("new_releases_found=false", file=f)
        return

    print(f"Found {len(new_releases)} new source release(s) to process.")
    new_releases.sort(key=lambda r: r['created_at'])

    changelog = load_changelog()
    
    for release in new_releases:
        print(f"--- Processing source release: {release['tag_name']} ({release['id']}) ---")
        
        parsed_info = parse_release_notes(release.get('body', ''), release['tag_name'], release['name'], config)
        if not parsed_info:
            print("Could not parse release info. Skipping.")
            continue

        app_id = parsed_info.get('app_id')
        version = parsed_info.get('version')
        asset_name = parsed_info.get('asset_name')
        display_name = parsed_info.get('display_name')

        if not all([app_id, version, asset_name, display_name]):
            print(f"::warning::Skipping incomplete app info: {parsed_info}")
            continue

        bot_release_tag = f"{app_id}-v{version}"
        if check_if_bot_release_exists(bot_repo, bot_release_tag):
            continue

        try:
            original_file = download_asset(source_repo, release['id'], asset_name)
            patched_file = patch_file(original_file, asset_name)
            
            release_title = f"{display_name} {asset_name} v{version}"
            release_notes = f"app: {app_id}\nversion: {version}\nasset_name: {asset_name}"
            
            create_bot_release(bot_repo, bot_release_tag, release_title, release_notes, patched_file)
            
            download_url = f"https://github.com/{bot_repo}/releases/download/{bot_release_tag}/{asset_name}"
            
            # This is where we append to the changelog
            changelog.append({
                "type": "added", # This logic can be expanded to detect 'updated'
                "app_id": app_id,
                "display_name": display_name,
                "version": version,
                "url": download_url,
                "timestamp": release['created_at']
            })
            
            processed_release_ids.append(release['id'])
            
        except Exception as e:
            print(f"::error::Failed to process app {display_name} from release {release['tag_name']}. Reason: {e}")

    os.makedirs(paths.DIST_DIR, exist_ok=True)
    save_changelog(changelog)
    save_release_state(processed_release_ids)
    print("Release management complete. Changelog updated.")
    with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
        print("new_releases_found=true", file=f)

if __name__ == "__main__":
    main()
