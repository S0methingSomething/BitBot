import os
import re
import json
import subprocess
from typing import List, Dict, Optional, Tuple

# --- Configuration ---
CONFIG_FILE = 'config.json'
PROCESS_VARS_SCRIPT = 'process_vars.js'
DOWNLOAD_DIR = './dist'

# --- Helper Functions ---

def run_command(command: List[str], check: bool = True) -> subprocess.CompletedProcess:
    """Runs a shell command and returns its result."""
    print(f"Executing: {' '.join(command)}")
    return subprocess.run(command, capture_output=True, text=True, check=check)

def load_config() -> Dict:
    """Loads the configuration file."""
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

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

def parse_release_description(description: str, apps_config: List[Dict]) -> Optional[Tuple[str, str]]:
    """
    Parses a release description to find the app name and version.
    Example: "MonetizationVars for BitLife v3.19.4"
    """
    for app in apps_config:
        display_name = app['displayName']
        # Regex to find "for <AppName> v<version>"
        match = re.search(f"for {re.escape(display_name)} v([\\d\\.]+)", description, re.IGNORECASE)
        if match:
            version = match.group(1)
            print(f"Found app '{display_name}' with version '{version}' in description.")
            return (app['id'], version)
    return None

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
    """Patches the downloaded file using the Node.js script."""
    patched_path = os.path.join(DOWNLOAD_DIR, asset_name)
    print(f"Patching '{original_path}' to '{patched_path}'")
    run_command(['node', PROCESS_VARS_SCRIPT, original_path, patched_path])
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
    asset_name = config['github']['assetFileName']
    apps_config = config['apps']

    source_releases = get_source_releases(source_repo)
    new_releases_for_reddit = {}
    primary_version_for_title = None

    for release in source_releases:
        description = release.get('body', '')
        if not description:
            continue

        parsed_info = parse_release_description(description, apps_config)
        if not parsed_info:
            continue

        app_id, version = parsed_info
        app_config = next((app for app in apps_config if app['id'] == app_id), None)
        if not app_config:
            continue

        # Construct the tag for the BitBot release
        bot_release_tag = f"{app_id}-v{version}"

        if not check_if_bot_release_exists(bot_repo, bot_release_tag):
            try:
                # 1. Download
                original_file = download_asset(source_repo, release['id'], asset_name)
                
                # 2. Patch
                patched_file = patch_file(original_file, asset_name)

                # 3. Create Release
                release_title = f"{app_config['displayName']} {asset_name} v{version}"
                release_notes = f"Auto-patched {asset_name} for {app_config['displayName']} from source release {release['tag_name']}."
                create_bot_release(bot_repo, bot_release_tag, release_title, release_notes, patched_file)
                
                # 4. Store info for Reddit post
                download_url = f"https://github.com/{bot_repo}/releases/download/{bot_release_tag}/{asset_name}"
                new_releases_for_reddit[app_id] = download_url

                # Set the primary version for the Reddit post title (Option A)
                if app_id == 'bitlife':
                    primary_version_for_title = version

            except Exception as e:
                print(f"::error::Failed to process release {release['tag_name']} for app {app_id}. Reason: {e}")

    # If no primary version was found but other apps were updated, use the latest version found.
    if not primary_version_for_title and new_releases_for_reddit:
        # Fallback logic: find the version from the last processed app
        # This part is tricky and depends on desired behavior. A simple fallback:
        last_processed_tag = f"{app_id}-v{version}" # from the last loop
        primary_version_for_title = version
        print(f"::warning::BitLife version not found. Using fallback version '{version}' for Reddit title.")


    # Output for the next GitHub Actions step
    if new_releases_for_reddit:
        print("New releases were created. Setting outputs for Reddit job.")
        urls_json = json.dumps(new_releases_for_reddit)
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
