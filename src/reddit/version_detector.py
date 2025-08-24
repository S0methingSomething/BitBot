"""Version change detection utilities for BitBot Reddit posts."""

from typing import Any

from packaging.version import parse as parse_version

from config_loader import load_config


def _process_added_or_updated_apps(
    all_versions: dict[str, Any],
    versions_to_check: dict[str, str],
    added: dict[str, Any],
    updated: dict[str, Any],
    new_versions: dict[str, str],
) -> None:
    """Process added or updated apps."""
    for app_id, data in all_versions.items():
        if not (latest := data.get("latest_release")):
            continue
        current_v = versions_to_check.get(app_id, "0.0.0")
        if parse_version(latest["version"]) > parse_version(current_v):
            new_versions[app_id] = latest["version"]
            if current_v == "0.0.0":
                added[app_id] = {
                    "display_name": data["display_name"],
                    "version": latest["version"],
                    "url": latest["download_url"],
                }
            else:
                updated[app_id] = {
                    "new": {
                        "display_name": data["display_name"],
                        "version": latest["version"],
                        "url": latest["download_url"],
                    },
                    "old": current_v,
                }
        elif parse_version(latest["version"]) < parse_version(current_v):
            # Handle version rollback
            updated[app_id] = {
                "new": {
                    "display_name": data["display_name"],
                    "version": latest["version"],
                    "url": latest["download_url"],
                },
                "old": current_v,
            }


def _process_removed_apps(
    versions_to_check: dict[str, str],
    all_versions: dict[str, Any],
    removed: dict[str, Any],
    config: Any,
) -> None:
    """Process removed apps."""
    for app_id, current_v in versions_to_check.items():
        if app_id not in all_versions and current_v != "0.0.0":
            # Find the app display name from config
            display_name = app_id  # Default to app_id
            for app in config.apps:
                if app.id == app_id:
                    display_name = app.display_name
                    break
            removed[app_id] = {"display_name": display_name, "version": current_v}


def get_version_changes(
    all_versions: dict[str, Any], versions_to_check: dict[str, str]
) -> dict[str, Any]:
    """Compares current versions with the latest versions and returns the changes.

    Args:
        all_versions: Dictionary of all versions
        versions_to_check: Dictionary of versions to check against

    Returns:
        Dictionary containing added, updated, removed apps and new versions
    """
    added: dict[str, Any] = {}
    updated: dict[str, Any] = {}
    removed: dict[str, Any] = {}
    new_versions = versions_to_check.copy()

    # Load config to get app display names
    config = load_config()

    # Check for added or updated apps
    _process_added_or_updated_apps(
        all_versions, versions_to_check, added, updated, new_versions
    )

    # Check for removed apps (apps that were in versions_to_check but not in all_versions)
    _process_removed_apps(versions_to_check, all_versions, removed, config)

    return {
        "added": added,
        "updated": updated,
        "removed": removed,
        "new_versions": new_versions,
    }
