import os
import sys
import json
import re
import requests
import subprocess
from pathlib import Path

# Define the project's root directory to reliably locate files.
# This goes up two levels from `src/bitbot/github.py` to the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

def run_command(command, check=True):
    """Helper to run shell commands and print their output for debugging."""
    print(f"Executing: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, command, result.stdout, result.stderr)
    return result

def set_github_output(name, value):
    """Writes an output to the GITHUB_OUTPUT file for use in later workflow steps."""
    with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
        print(f"{name}={value}", file=f)

def get_latest_bot_release(config, token):
    """Fetches the latest release from this bot's own GitHub repo."""
    bot_repo = config['github']['botRepo']
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    api_url = f"https://api.github.com/repos/{bot_repo}/releases/latest"
    
    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
        release_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"::error::Could not fetch latest release from {bot_repo}: {e}", file=sys.stderr)
        return None
    
    version = release_data.get('tag_name', '').lstrip('v')
    asset = next((a for a in release_data.get('assets', []) if a['name'] == config['github']['assetFileName']), None)
    
    if not version or not asset:
        print("::error::Could not find a valid version and asset in the latest bot release.", file=sys.stderr)
        return None
        
    return {"version": version, "url": asset['browser_download_url']}

def parse_version_from_title(title):
    """Extracts a version string (e.g., '4.2.0') from a post title."""
    match = re.search(r'v(\d+\.\d+\.\d+)', title)
    return match.group(1) if match else "0.0.0" # Fallback for malformed titles.

def create_release():
    """
    Orchestrates the entire release process: checking for new versions,
    processing assets, creating GitHub tags and releases.
    """
    with open(PROJECT_ROOT / 'config.json', 'r') as f:
        config = json.load(f)
    
    github_token = os.environ['GITHUB_TOKEN']
    source_repo = config['github']['sourceRepo']
    bot_repo = config['github']['botRepo']
    asset_name = config['github']['assetFileName']
    headers = {"Authorization": f"Bearer {github_token}", "Accept": "application/vnd.github+json"}

    if bot_repo != os.environ['GITHUB_REPOSITORY']:
        print(f"::error::Config error! 'github.botRepo' ('{bot_repo}') must match this repo ('{os.environ['GITHUB_REPOSITORY']}').")
        sys.exit(1)

    print(f"Fetching latest release from source repo: {source_repo}")
    source_api_url = f"https://api.github.com/repos/{source_repo}/releases/latest"
    response = requests.get(source_api_url, headers=headers)
    response.raise_for_status()
    source_release = response.json()
    
    version_match = re.search(r'v(\d+\.\d+\.\d+)', source_release['body'])
    if not version_match:
        print("::error::Could not parse version (e.g., v1.2.3) from source release body.")
        sys.exit(1)
    source_version = version_match.group(1)
    source_tag = f"v{source_version}"
    print(f"Found source version: {source_version}")

    print(f"Fetching latest release from this bot's repo: {bot_repo}")
    bot_api_url = f"https://api.github.com/repos/{bot_repo}/releases/latest"
    try:
        response = requests.get(bot_api_url, headers=headers)
        response.raise_for_status()
        bot_tag = response.json().get('tag_name', '')
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            bot_tag = ''
        else:
            raise
    
    print(f"Source tag: {source_tag}, Latest bot tag: {bot_tag}")
    if source_tag == bot_tag:
        print("No new version found. The bot is already up-to-date.")
        set_github_output("new_version_found", "false")
        return
    
    print(f"New version {source_tag} found. Starting the release process.")
    set_github_output("new_version_found", "true")
    set_github_output("version", source_version)
    
    print(f"Finding asset '{asset_name}' in the source release...")
    source_asset = next((a for a in source_release['assets'] if a['name'] == asset_name), None)
    if not source_asset:
        print(f"::error::Could not find asset named '{asset_name}' in source release.")
        sys.exit(1)
    
    dist_dir = PROJECT_ROOT / 'dist'
    dist_dir.mkdir(exist_ok=True)
    original_path = dist_dir / f"original_{asset_name}"
    patched_path = dist_dir / asset_name
    
    print(f"Downloading original asset to {original_path}...")
    with requests.get(source_asset['url'], headers={"Authorization": f"token {github_token}", "Accept": "application/octet-stream"}, stream=True) as r:
        r.raise_for_status()
        with open(original_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    
    node_script_path = PROJECT_ROOT / "scripts" / "process_vars.js"
    run_command(["node", str(node_script_path), str(original_path), str(patched_path)])

    run_command(["git", "config", "user.name", "github-actions[bot]"])
    run_command(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"])
    if run_command(["git", "ls-remote", "--tags", "origin", f"refs/tags/{source_tag}"], check=False).stdout:
        print(f"Tag {source_tag} exists remotely. Deleting and re-creating.")
        run_command(["git", "push", "--delete", "origin", source_tag], check=False)
    run_command(["git", "tag", "-f", "-a", source_tag, "-m", f"Release {source_tag}"])
    run_command(["git", "push", "origin", source_tag])

    release_title = config['messages']['releaseTitle'].replace('{{asset_name}}', asset_name).replace('{{version}}', source_version)
    release_body = config['messages']['releaseDescription'].replace('{{asset_name}}', asset_name)
    release_payload = {"tag_name": source_tag, "name": release_title, "body": release_body}
    
    print("Creating GitHub release...")
    create_url = f"https://api.github.com/repos/{bot_repo}/releases"
    response = requests.post(create_url, headers=headers, json=release_payload)
    response.raise_for_status()
    release_data = response.json()
    upload_url_template = release_data['upload_url'].split('{')[0]

    print(f"Uploading asset to release '{release_title}'...")
    upload_url = f"{upload_url_template}?name={asset_name}"
    with open(patched_path, 'rb') as f:
        asset_data = f.read()
    
    response = requests.post(upload_url, headers={"Authorization": f"Bearer {github_token}", "Content-Type": "application/octet-stream"}, data=asset_data)
    response.raise_for_status()
    
    direct_url = f"https://github.com/{bot_repo}/releases/download/{source_tag}/{asset_name}"
    set_github_output("direct_download_url", direct_url)
    print("\nRelease process completed successfully.")
