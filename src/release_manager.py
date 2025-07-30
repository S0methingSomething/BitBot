import os
import re
import json
import subprocess
import toml
from typing import List, Dict, Optional, Tuple

# --- Configuration ---
CONFIG_FILE = 'config.toml'
DOWNLOAD_DIR = 'dist'

# --- Helper Functions ---

def run_command(command: List[str], check: bool = True) -> subprocess.CompletedProcess:
    """Runs a shell command and returns its result."""
    print(f"Executing: {' '.join(command)}")
    return subprocess.run(command, capture_output=True, text=True, check=check)

from helpers import load_config

def get_github_data(url: str) -> Dict | List:
    """Fetches data from the GitHub API using the gh cli."""
    command = ['gh', 'api', url]
    result = run_command(command)
    return json.loads(result.stdout)

# --- Core Logic ---

def get_source_releases(repo: str) -> List[Dict]:
    """Gets the last 30 releases from the source repository."""
    print(f"Fetching latest releases from source repo: {repo}")
    return get_github_data(f"/repos/{repo}/releases?per_page=30")

def parse_release_description(description: str, apps_config: List[Dict]) -> List[Dict]:
    """
    Parses a release description with a structured key-value format.
    Example:
    app: BitLife
    version: 3.20
    asset_name: MonetizationVars
    """
    found_releases = []
    current_release = {}
    app_id_map = {app['displayName'].lower(): app['id'] for app in apps_config}

    for line in description.splitlines():
        line = line.strip()
        if not line:
            if current_release:
                found_releases.append(current_release)
                current_release = {}
            continue

        try:
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()

            if key == 'app':
                if current_release: # Start of a new app block
                    found_releases.append(current_release)
                # Check if the app is one we manage
                app_id = app_id_map.get(value.lower())
                if app_id:
                    current_release = {'app_id': app_id, 'display_name': value}
                else:
                    current_release = {} # Not a recognized app, reset
            elif current_release: # Only process version/asset if we are in a valid app block
                if key == 'version':
                    current_release['version'] = value
                elif key == 'asset_name':
                    current_release['asset_name'] = value
        except ValueError:
            continue
    
    if current_release:
        found_releases.append(current_release)

    print(f"Found {len(found_releases)} recognized app update(s) in description.")
    return found_releases

def check_if_bot_release_exists(bot_repo: str, tag: str) -> bool:
    """Checks if a release with the given tag exists in the bot repo."""
    try:
        run_command(['gh', 'release', 'view', tag, '--repo', bot_repo])
        print(f"Release '{tag}' already exists in {bot_repo}. Skipping.")
        return True
    except subprocess.CalledProcessError:
        print(f"Release '{tag}' does not exist in {bot_repo}. Proceeding.")
        return False

def download_asset(source_repo: str, release_id: int, asset_name: str) -> str:
    """Downloads a specific asset from a specific release."""
    print(f"Downloading asset '{asset_name}' from release ID {release_id}")
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    assets = get_github_data(f"/repos/{source_repo}/releases/{release_id}/assets")
    asset_id = next((asset['id'] for asset in assets if asset['name'] == asset_name), None)

    if not asset_id:
        raise FileNotFoundError(f"Asset '{asset_name}' not found in release {release_id}")

    download_url = f"https://api.github.com/repos/{source_repo}/releases/assets/{asset_id}"
    output_path = os.path.join(DOWNLOAD_DIR, f"original_{asset_name}")

    run_command([
        'curl', '-sL', '-J',
        '-H', 'Accept: application/octet-stream',
        '-H', f'Authorization: token {os.environ["GITHUB_TOKEN"]}',
        '-o', output_path,
        download_url
    ])
    return output_path

def patch_file(original_path: str, asset_name: str) -> str:
    """Patches the downloaded file using the new Python script."""
    patched_path = os.path.join(DOWNLOAD_DIR, asset_name)
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

# --- Main Execution ---

def main():
    config = load_config()
    source_repo = config['github']['sourceRepo']
    bot_repo = config['github']['botRepo']
    apps_config = config['apps']

    source_releases = get_source_releases(source_repo)
    processed_releases = {}
    primary_version_for_title = None
    version_for_fallback = None

    for release in source_releases:
        description = release.get('body', '')
        if not description:
            continue

        parsed_releases = parse_release_description(description, apps_config)
        if not parsed_releases:
            continue

        for parsed_info in parsed_releases:
            app_id = parsed_info.get('app_id')
            version = parsed_info.get('version')
            asset_name = parsed_info.get('asset_name')
            display_name = parsed_info.get('display_name')
            version_for_fallback = version # Keep track of the last seen version

            if not all([app_id, version, asset_name, display_name]):
                print(f"::warning::Skipping incomplete release info: {parsed_info}")
                continue

            bot_release_tag = f"{app_id}-v{version}"

            if not check_if_bot_release_exists(bot_repo, bot_release_tag):
                try:
                    original_file = download_asset(source_repo, release['id'], asset_name)
                    patched_file = patch_file(original_file, asset_name)
                    
                    release_title = f"{display_name} {asset_name} v{version}"
                    release_notes = f"Auto-patched {asset_name} for {display_name} from source release {release['tag_name']}."
                    create_bot_release(bot_repo, bot_release_tag, release_title, release_notes, patched_file)
                    
                    download_url = f"https://github.com/{bot_repo}/releases/download/{bot_release_tag}/{asset_name}"
                    processed_releases[app_id] = {
                        "display_name": display_name,
                        "version": version,
                        "url": download_url
                    }

                    if app_id == 'bitlife':
                        primary_version_for_title = version

                except Exception as e:
                    print(f"::error::Failed to process release {release['tag_name']} for app {app_id}. Reason: {e}")

    if not primary_version_for_title and processed_releases:
        primary_version_for_title = version_for_fallback
        print(f"::warning::BitLife version not found. Using fallback version '{version_for_fallback}' for Reddit title.")

    if processed_releases:
        print("New releases were created. Saving data and setting outputs.")
        
        # Save the detailed data to a JSON file for other jobs
        output_dir = './dist'
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, 'releases.json'), 'w') as f:
            json.dump(processed_releases, f, indent=2)

        # Keep the simple URL map for the direct_link mode for now
        urls_for_output = {app_id: data['url'] for app_id, data in processed_releases.items()}
        urls_json = json.dumps(urls_for_output)

        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            print(f"new_releases_found=true", file=f)
            print(f"version={primary_version_for_title}", file=f)
            print(f"urls={urls_json}", file=f)
    else:
        print("No new releases to post to Reddit.")
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            print(f"new_releases_found=false", file=f)

if __name__ == "__main__":
    main()
