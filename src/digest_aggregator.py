"""Digest aggregator for BitBot - collects releases over time for weekly digest posts."""

from datetime import UTC, datetime
from typing import Any, cast

from io_handler import IOHandler
from logging_config import get_logger

logger = get_logger(__name__)


def load_digest_history() -> dict[str, Any]:
    """Load the digest history from file."""
    history = IOHandler.load_digest_history()
    return cast(dict[str, Any], history)


def save_digest_history(history: dict[str, Any]) -> None:
    """Save the digest history to file."""
    IOHandler.save_digest_history(history)


def add_release_to_digest(release_info: dict[str, Any]) -> None:
    """Add a release to the digest history."""
    history = load_digest_history()

    # Ensure we have a current cycle
    now = datetime.now(UTC)
    current_cycle = history.get("current_cycle", {})

    # If no cycle exists or its a new cycle, start a new one
    if not current_cycle:
        current_cycle = {"start_date": now.isoformat(), "releases": []}

    # Add the release to the current cycle
    current_cycle["releases"].append(
        {"timestamp": now.isoformat(), "release": release_info}
    )

    history["current_cycle"] = current_cycle
    save_digest_history(history)
    logger.info("Added release to digest history")


def get_current_cycle_releases() -> list[dict[str, Any]]:
    """Get all releases from the current cycle."""
    history = load_digest_history()
    current_cycle = history.get("current_cycle", {})
    releases = current_cycle.get("releases", [])
    if isinstance(releases, list):
        return releases
    return []


def should_create_new_digest_cycle(config: Any) -> bool:
    """Determine if we should create a new digest cycle."""
    if not getattr(config.digest, "enabled", False):
        return False

    history = load_digest_history()
    current_cycle = history.get("current_cycle", {})

    if not current_cycle:
        return True  # No cycle yet, create one

    try:
        start_date = datetime.fromisoformat(current_cycle["start_date"])
        now = datetime.now(UTC)
        cycle_days = getattr(config.digest, "cycle_days", 7)

        # Check if enough days have passed
        days_passed = (now - start_date).days
        return days_passed >= cycle_days
    except (KeyError, ValueError) as e:
        logger.warning(f"Error checking digest cycle: {e}")
        return True  # Create new cycle on error


def start_new_digest_cycle() -> dict[str, Any]:
    """Start a new digest cycle and return the previous cycle data."""
    history = load_digest_history()
    previous_cycle = history.get("current_cycle", {})

    # Start new cycle
    now = datetime.now(UTC)
    history["current_cycle"] = {"start_date": now.isoformat(), "releases": []}

    # Save previous cycle if it had releases
    if previous_cycle and previous_cycle.get("releases"):
        cycle_id = now.strftime("%Y-%m-%d")
        history[f"cycle_{cycle_id}"] = previous_cycle

    save_digest_history(history)
    logger.info("Started new digest cycle")
    if isinstance(previous_cycle, dict):
        return previous_cycle
    return {}


def format_digest_changelog(releases: list[dict[str, Any]], config: Any) -> str:  # noqa: ARG001
    """Format the digest changelog from collected releases."""
    if not releases:
        return "No updates in this cycle."

    # Group releases by app
    app_changes = {}
    for release_entry in releases:
        release_data = release_entry.get("release", {})
        for app_id, app_info in release_data.items():
            if app_id not in app_changes:
                app_changes[app_id] = {
                    "display_name": app_info.get("display_name", app_id),
                    "versions": [],
                }
            app_changes[app_id]["versions"].append(
                {
                    "version": app_info.get("version", "unknown"),
                    "timestamp": release_entry.get("timestamp", ""),
                }
            )

    # Format the changelog
    lines = ["## Weekly Digest Changelog"]
    for app_info in app_changes.values():
        lines.append(f"### {app_info['display_name']}")
        for version_info in app_info["versions"]:
            timestamp = version_info.get("timestamp", "")[:10]  # Just the date part
            lines.append(f"* v{version_info['version']} - {timestamp}")
        lines.append("")  # Blank line between apps

    return "\n".join(lines).strip()
