"""Placeholder parsing utilities for BitBot templates."""

import re
from datetime import UTC, datetime
from typing import Any

from config_loader import load_config


def process_placeholders(
    template_content: str,
    context: dict[str, Any],
    config: Any = None,
) -> str:
    """Process placeholders in template content.

    Args:
        template_content: The template content with placeholders
        context: Dictionary of placeholder values
        config: Configuration object (optional)

    Returns:
        Processed template content with placeholders replaced
    """
    # Load config if not provided
    if config is None:
        config = load_config()

    # Remove tutorial/comment blocks if configured
    if hasattr(config, "skip_content") and config.skip_content.start_tag:
        template_content = re.sub(
            f"{re.escape(config.skip_content.start_tag)}.*?{re.escape(config.skip_content.end_tag)}",
            "",
            template_content,
            flags=re.DOTALL,
        )

    # Process all placeholders
    processed_content = template_content

    # Replace double curly brace placeholders
    for key, value in context.items():
        processed_content = processed_content.replace(f"{{{{{key}}}}}", str(value))

    # Also replace single brace placeholders that might be left over
    for key, value in context.items():
        processed_content = processed_content.replace(f"{{{key}}}", str(value))

    return processed_content.strip()


def _generate_changelog(
    config: Any, added: dict[str, Any], updated: dict[str, Any], removed: dict[str, Any]
) -> str:
    """Generate changelog content."""
    # Import locally to avoid circular imports
    from post_to_reddit import _format_changelog_section  # noqa: PLC0415

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


def _generate_available_list(config: Any, all_releases: dict[str, Any]) -> str:
    """Generate available list content."""
    formats = config.reddit.formats.table
    asset_name = config.github.asset_file_name
    lines = [formats.header, formats.divider]
    sorted_apps = sorted(all_releases.items(), key=lambda item: item[1]["display_name"])
    for _, info in sorted_apps:
        if latest := info.get("latest_release"):
            lines.append(
                formats.line.format(
                    display_name=info["display_name"],
                    asset_name=asset_name,
                    version=latest["version"],
                )
            )
    return "\n".join(lines)


def _generate_base_post_placeholders(config: Any, page_url: str) -> dict[str, Any]:
    """Generate base placeholders for Reddit post templates.

    Args:
        config: Configuration object
        page_url: URL to the landing page

    Returns:
        Dictionary of base placeholder values
    """
    return {
        "initial_status": config.feedback.status_line_format.format(
            status=config.feedback.labels.unknown,
        ),
        "download_portal_url": page_url,
        "bot_name": config.reddit.bot_name,
        "creator_username": config.reddit.creator,
        "subreddit": config.reddit.subreddit,
        "post_mode": config.reddit.post_mode,
        "bot_repo": config.github.bot_repo,
        "source_repo": config.github.source_repo,
        "asset_name": config.github.asset_file_name,
        "pages_url": getattr(config.github, "pages_url", "") or "",
        "version": "",  # Will be set based on releases
        "status": config.feedback.labels.unknown,
        "date": datetime.now(UTC).strftime("%Y-%m-%d"),
    }


def _add_version_info(placeholders: dict[str, Any], all_releases: dict[str, Any]) -> None:
    """Add version information to placeholders.

    Args:
        placeholders: Dictionary of placeholders to update
        all_releases: Dictionary of all releases
    """
    # Add version information if we have releases
    if all_releases:
        # Get the first app's version as the main version
        for app_data in all_releases.values():
            if "latest_release" in app_data and "version" in app_data["latest_release"]:
                placeholders["version"] = app_data["latest_release"]["version"]
                break


def _add_cloudflare_url(placeholders: dict[str, Any], config: Any) -> None:
    """Add Cloudflare Pages URL to placeholders if configured.

    Args:
        placeholders: Dictionary of placeholders to update
        config: Configuration object
    """
    # Add Cloudflare Pages URL if configured
    if hasattr(config, "deployment") and config.deployment:
        cloudflare_config = getattr(config.deployment, "cloudflare", None)
        if cloudflare_config and hasattr(cloudflare_config, "project_name") and hasattr(cloudflare_config, "account_id"):
            placeholders["cloudflare_url"] = f"https://{cloudflare_config.project_name}.{cloudflare_config.account_id}.pages.dev/"


def _add_direct_download_urls(placeholders: dict[str, Any], all_releases: dict[str, Any]) -> None:
    """Add direct download URLs for each app to placeholders.

    Args:
        placeholders: Dictionary of placeholders to update
        all_releases: Dictionary of all releases
    """
    # Add direct download URLs for each app
    for app_id, app_data in all_releases.items():
        if "latest_release" in app_data and "download_url" in app_data["latest_release"]:
            placeholders[f"direct_download_url_{app_id}"] = app_data["latest_release"]["download_url"]


def generate_post_placeholders(
    changelog_data: dict[str, Any],
    all_releases: dict[str, Any],
    page_url: str,
    config: Any,
) -> dict[str, Any]:
    """Generate placeholders for Reddit post templates.

    Args:
        changelog_data: Dictionary containing added, updated, removed data
        all_releases: Dictionary of all releases
        page_url: URL to the landing page
        config: Configuration object

    Returns:
        Dictionary of placeholder values
    """
    # Generate dynamic content
    changelog = _generate_changelog(
        config,
        changelog_data.get("added", {}),
        changelog_data.get("updated", {}),
        changelog_data.get("removed", {}),
    )

    available_list = _generate_available_list(config, all_releases)

    # Base placeholders
    placeholders = _generate_base_post_placeholders(config, page_url)
    placeholders["changelog"] = changelog
    placeholders["available_list"] = available_list

    # Add additional information
    _add_version_info(placeholders, all_releases)
    _add_cloudflare_url(placeholders, config)
    _add_direct_download_urls(placeholders, all_releases)

    return placeholders


def _add_page_cloudflare_url(placeholders: dict[str, Any], config: Any) -> None:
    """Add Cloudflare Pages URL to page placeholders if configured.

    Args:
        placeholders: Dictionary of placeholders to update
        config: Configuration object
    """
    # Add Cloudflare Pages URL if configured
    if hasattr(config, "deployment") and config.deployment:
        cloudflare_config = getattr(config.deployment, "cloudflare", None)
        if cloudflare_config and hasattr(cloudflare_config, "project_name") and hasattr(cloudflare_config, "account_id"):
            placeholders["cloudflare_url"] = f"https://{cloudflare_config.project_name}.{cloudflare_config.account_id}.pages.dev/"


def _add_page_direct_download_urls(placeholders: dict[str, Any], page_data: dict[str, Any]) -> None:
    """Add direct download URLs for each app to page placeholders.

    Args:
        placeholders: Dictionary of placeholders to update
        page_data: Data for the landing page
    """
    # Add direct download URLs for each app
    for app_id, app_data in page_data.items():
        if "latest_release" in app_data and "download_url" in app_data["latest_release"]:
            placeholders[f"direct_download_url_{app_id}"] = app_data["latest_release"]["download_url"]


def generate_page_placeholders(
    page_data: dict[str, Any],
    config: Any,
) -> dict[str, Any]:
    """Generate placeholders for landing page templates.

    Args:
        page_data: Data for the landing page
        config: Configuration object

    Returns:
        Dictionary of placeholder values
    """
    placeholders = {
        "bot_repo": config.github.bot_repo,
        "asset_name": config.github.asset_file_name,
        "date": datetime.now(UTC).strftime("%Y-%m-%d"),
    }

    # Add additional information
    _add_page_cloudflare_url(placeholders, config)

    # Add app-specific data if available
    if page_data:
        _add_page_direct_download_urls(placeholders, page_data)

    return placeholders
