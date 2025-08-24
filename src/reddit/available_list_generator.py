"""Available list generation utilities for BitBot Reddit posts."""

from typing import Any


def generate_available_list(config: Any, all_releases: dict[str, Any]) -> str:
    """Generate an available list for a Reddit post.

    Args:
        config: Configuration object
        all_releases: Dictionary of all releases

    Returns:
        Generated available list string
    """
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
