"""Post body generation utilities for BitBot Reddit posts."""

from pathlib import Path
from typing import Any

import paths
from placeholder_parser import generate_post_placeholders, process_placeholders


def generate_post_body(
    config: Any,
    changelog_data: dict[str, Any],
    all_releases: dict[str, Any],
    page_url: str,
) -> str:
    """Generate the body of a Reddit post.

    Args:
        config: Configuration object
        changelog_data: Dictionary containing added, updated, removed data
        all_releases: Dictionary of all releases
        page_url: URL to the landing page

    Returns:
        Generated post body string
    """
    template_path = Path(paths.TEMPLATES_DIR) / config.reddit.templates.post
    raw_template = template_path.read_text()

    # Generate placeholders
    placeholders = generate_post_placeholders(
        changelog_data,
        all_releases,
        page_url,
        config,
    )

    # Process template with placeholders
    return str(process_placeholders(raw_template, placeholders, config))
