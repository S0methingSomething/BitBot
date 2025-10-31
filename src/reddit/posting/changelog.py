"""Reddit post changelog generation."""

from typing import Any

from beartype import beartype


@beartype  # type: ignore[misc]
def create_section(
    title: str,
    data: dict[str, Any],
    key_format: str,
    formats: dict[str, str],
    asset_name: str,
) -> str | None:
    """Create formatted section with title and data items."""
    lines = [f"### {title}"]
    for info in data.values():
        line_format = formats.get(key_format)
        if not line_format:
            return None

        if title == "Added":
            line = (
                line_format.replace("{{display_name}}", info["display_name"])
                .replace("{{asset_name}}", asset_name)
                .replace("{{version}}", info["version"])
                .replace("{{download_url}}", info["url"])
            )
        elif title == "Updated":
            line = (
                line_format.replace("{{display_name}}", info["new"]["display_name"])
                .replace("{{asset_name}}", asset_name)
                .replace("{{new_version}}", info["new"]["version"])
                .replace("{{old_version}}", info["old"])
                .replace("{{download_url}}", info["new"]["url"])
            )
        elif title == "Removed":
            line = (
                line_format.replace("{{display_name}}", info["display_name"])
                .replace("{{asset_name}}", asset_name)
                .replace("{{old_version}}", info["version"])
            )
        else:
            continue
        lines.append(line)

    return "\n".join(lines) if len(lines) > 1 else None


def generate_changelog(
    config: dict[str, Any],
    added: dict[str, Any],
    updated: dict[str, Any],
    removed: dict[str, Any],
) -> str:
    """Generate changelog section."""
    post_mode = config["reddit"].get("postMode", "landing_page")
    key_suffix = "landing" if post_mode == "landing_page" else "direct"
    asset_name: str = config["github"].get("assetFileName", "asset")
    formats: dict[str, str] = config["reddit"]["formats"]["changelog"]
    sections = []

    if added:
        section = create_section("Added", added, f"added_{key_suffix}", formats, asset_name)
        if section:
            sections.append(section)
    if updated:
        section = create_section("Updated", updated, f"updated_{key_suffix}", formats, asset_name)
        if section:
            sections.append(section)
    if removed:
        section = create_section("Removed", removed, f"removed_{key_suffix}", formats, asset_name)
        if section:
            sections.append(section)

    return "\n\n".join(sections) if sections else "No new updates in this version."
