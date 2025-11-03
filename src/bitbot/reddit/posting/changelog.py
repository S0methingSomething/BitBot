"""Reddit post changelog generation."""

from typing import Any

import deal
from beartype import beartype

from bitbot.config_models import Config


@deal.pre(lambda title, _d, _k, _f, _a: len(title) > 0)
@deal.pre(lambda _t, data, _k, _f, _a: isinstance(data, dict))
@beartype
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


@deal.pre(lambda config, added, updated, removed: isinstance(config, Config))
@deal.pre(lambda config, added, updated, removed: isinstance(added, dict))
@deal.pre(lambda config, added, updated, removed: isinstance(updated, dict))
@deal.pre(lambda config, added, updated, removed: isinstance(removed, dict))
@deal.post(lambda result: len(result) > 0)
@beartype
def generate_changelog(
    config: Config,
    added: dict[str, Any],
    updated: dict[str, Any],
    removed: dict[str, Any],
) -> str:
    """Generate changelog section."""
    download_mode = config.reddit.download_mode
    key_suffix = "landing" if download_mode == "landing_page" else "direct"
    asset_name: str = config.github.asset_file_name
    formats: dict[str, str] = config.reddit.formats.changelog
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
