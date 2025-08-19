import os
import sys
from pathlib import Path
from typing import Any, Dict

from github import Github, GithubException

from helpers import load_config, parse_release_notes
from logging_config import get_logger

logging = get_logger(__name__)


def _process_release(release: Any, config: Dict[str, Any]) -> str:
    """Processes a single release for migration."""
    if "app:" in release.body and "version:" in release.body and "asset_name:" in release.body:
        return "skipped"

    logging.info(f"--- Migrating legacy release: {release.tag_name} ---")
    parsed_info = parse_release_notes(release.body, release.tag_name, release.title, config)

    if not parsed_info:
        logging.error(f"Could not parse info for tag {release.tag_name}. Cannot migrate.")
        return "failed"

    app_id = parsed_info["app_id"]
    version = parsed_info["version"]
    asset_name = parsed_info["asset_name"]
    logging.info(f"  Parsed Info: App='{app_id}', Version='{version}', Asset='{asset_name}'")

    new_body = f"app: {app_id}\nversion: {version}\nasset_name: {asset_name}\n"

    try:
        logging.info(f"  Updating release '{release.tag_name}' with new structured body.")
        release.update_release(name=release.title, message=new_body)
        return "updated"
    except GithubException as e:
        logging.error(f"Failed to update release {release.tag_name}: {e}")
        return "failed"

def migrate_releases() -> None:
    """
    Performs a one-time migration of all legacy releases to a new, structured
    format in the release body by leveraging the centralized parser.
    """
    config = load_config()
    g = Github(os.getenv("GITHUB_TOKEN"))
    bot_repo_name = config["github"]["botRepo"]

    try:
        repo = g.get_repo(bot_repo_name)
        releases = repo.get_releases()
        logging.info(f"Found {releases.totalCount} releases in {bot_repo_name}. Analyzing for migration...")
    except GithubException as e:
        logging.error(f"Failed to get repository or releases: {e}")
        sys.exit(1)

    results = {"updated": 0, "skipped": 0, "failed": 0}
    for release in releases:
        status = _process_release(release, config)
        results[status] += 1

    logging.info(f"Migration complete. Updated: {results['updated']}, Skipped: {results['skipped']}, Failed: {results['failed']}.")
    if results["failed"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    migrate_releases()
