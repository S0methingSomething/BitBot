"""Title generation utilities for BitBot Reddit posts."""

from datetime import UTC, datetime
from typing import Any


def _format_title_for_added_apps(formats: Any, added_list: str) -> str:
    """Format title for added apps only."""
    template = formats.added_only
    return str(template.replace("{{added_list}}", added_list))


def _format_title_for_updated_apps(
    formats: Any, updated_list: str, num_updated: int
) -> str:
    """Format title for updated apps only."""
    if num_updated == 1:
        template = formats.updated_only_single
    else:
        template = formats.updated_only_multi
    return str(template.replace("{{updated_list}}", updated_list))


def _format_title_for_mixed_apps(
    formats: Any, added_list: str, updated_list: str, num_updated: int
) -> str:
    """Format title for mixed added and updated apps."""
    if num_updated == 1:
        template = formats.mixed_single_update
    else:
        template = formats.mixed_multi_update
    return str(template.replace("{{added_list}}", added_list).replace(
        "{{updated_list}}", updated_list
    ))


def _format_generic_title(formats: Any) -> str:
    """Format generic title."""
    template = formats.generic
    return str(template.replace("{{date}}", datetime.now(UTC).strftime("%Y-%m-%d")))


def generate_dynamic_title(
    config: Any,
    added: dict[str, Any],
    updated: dict[str, Any],
    fresh_start: bool = False,
) -> str:
    """Generate a dynamic title for a Reddit post.

    Args:
        config: Configuration object
        added: Dictionary of added apps
        updated: Dictionary of updated apps
        fresh_start: Whether this is a fresh start

    Returns:
        Generated title string
    """
    num_added, num_updated = len(added), len(updated)
    formats = config.reddit.formats.titles

    # Special handling for fresh start
    if fresh_start and num_added > 0 and num_updated == 0:
        # For fresh start with only added apps, use a startup title
        return "[BitBot] Startup - Initial Release"

    def create_app_list(apps: dict[str, Any]) -> str:
        return ", ".join(
            f"{info.get('display_name', 'Unknown')} v{info.get('version', '?.?.?')}"
            for _, info in apps.items()
        )

    added_list = create_app_list(added)
    updated_list = create_app_list(updated)

    # Determine which format to use based on the counts
    if num_added > 0 and num_updated == 0:
        return _format_title_for_added_apps(formats, added_list)

    if num_added == 0 and num_updated > 0:
        return _format_title_for_updated_apps(formats, updated_list, num_updated)

    if num_added > 0 and num_updated > 0:
        return _format_title_for_mixed_apps(
            formats, added_list, updated_list, num_updated
        )

    # Generic case
    return _format_generic_title(formats)
