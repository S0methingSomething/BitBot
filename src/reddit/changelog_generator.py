"""Changelog generation utilities for BitBot Reddit posts."""

from typing import Any


def _format_added_changelog_line(
    line_format: str, info: dict[str, Any], asset_name: str
) -> str:
    """Format a single added line in the changelog."""
    return line_format.format(
        display_name=info["display_name"],
        asset_name=asset_name,
        version=info["version"],
        download_url=info["url"],
    )


def _format_updated_changelog_line(
    line_format: str, info: dict[str, Any], asset_name: str
) -> str:
    """Format a single updated line in the changelog."""
    return line_format.format(
        display_name=info["new"]["display_name"],
        asset_name=asset_name,
        new_version=info["new"]["version"],
        old_version=info["old"],
        download_url=info["new"]["url"],
    )


def _format_removed_changelog_line(
    line_format: str, info: dict[str, Any], asset_name: str
) -> str:
    """Format a single removed line in the changelog."""
    return line_format.format(
        display_name=info["display_name"],
        asset_name=asset_name,
        old_version=info["version"],
    )


def _format_changelog_line(
    line_format: str, info: dict[str, Any], asset_name: str, change_type: str
) -> str:
    """Formats a single line in the changelog."""
    if change_type == "Added":
        return _format_added_changelog_line(line_format, info, asset_name)
    if change_type == "Updated":
        return _format_updated_changelog_line(line_format, info, asset_name)
    if change_type == "Removed":
        return _format_removed_changelog_line(line_format, info, asset_name)
    return ""


def _format_changelog_section(
    title: str, data: dict[str, Any], formats: Any, asset_name: str, key_suffix: str
) -> str:
    """Format a single changelog section."""
    if not data:
        return ""

    lines = [f"### {title}"]
    key_format = f"{title.lower()}_{key_suffix}"
    if hasattr(formats, key_format):
        line_format = getattr(formats, key_format)
        lines.extend(
            _format_changelog_line(line_format, info, asset_name, title)
            for info in data.values()
        )
    if len(lines) > 1:
        return "\n".join(lines)
    return ""


def generate_changelog(
    config: Any, added: dict[str, Any], updated: dict[str, Any], removed: dict[str, Any]
) -> str:
    """Generate a changelog for a Reddit post.

    Args:
        config: Configuration object
        added: Dictionary of added apps
        updated: Dictionary of updated apps
        removed: Dictionary of removed apps

    Returns:
        Generated changelog string
    """
    post_mode = config.reddit.post_mode
    key_suffix = "landing" if post_mode == "landing_page" else "direct"
    asset_name = config.github.asset_file_name
    formats = config.reddit.formats.changelog
    sections = []

    # Format each section
    for title, data in [("Added", added), ("Updated", updated), ("Removed", removed)]:
        section = _format_changelog_section(
            title, data, formats, asset_name, key_suffix
        )
        if section:
            sections.append(section)

    return "\n\n".join(sections) or "No new updates in this version."
