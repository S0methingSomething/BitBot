"""Reddit post changelog generation."""

import icontract
from beartype import beartype

from bitbot.config_models import Config
from bitbot.types import ReleaseInfo, RemovedReleaseInfo, UpdatedReleaseInfo


@icontract.require(
    lambda title: len(title) > 0,
    description="Title cannot be empty",
)
@beartype
def create_section(
    title: str,
    data: dict[str, ReleaseInfo] | dict[str, UpdatedReleaseInfo] | dict[str, RemovedReleaseInfo],
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
            info_added: ReleaseInfo = info  # type: ignore[assignment]
            line = (
                line_format.replace("{{display_name}}", info_added["display_name"])
                .replace("{{asset_name}}", asset_name)
                .replace("{{version}}", info_added["version"])
                .replace("{{download_url}}", info_added["url"])
            )
        elif title == "Updated":
            info_updated: UpdatedReleaseInfo = info  # type: ignore[assignment]
            line = (
                line_format.replace("{{display_name}}", info_updated["new"]["display_name"])
                .replace("{{asset_name}}", asset_name)
                .replace("{{new_version}}", info_updated["new"]["version"])
                .replace("{{old_version}}", info_updated["old"])
                .replace("{{download_url}}", info_updated["new"]["url"])
            )
        elif title == "Removed":
            info_removed: RemovedReleaseInfo = info  # type: ignore[assignment]
            line = (
                line_format.replace("{{display_name}}", info_removed["display_name"])
                .replace("{{asset_name}}", asset_name)
                .replace("{{old_version}}", info_removed["version"])
            )
        else:
            continue
        lines.append(line)

    return "\n".join(lines) if len(lines) > 1 else None


@icontract.ensure(lambda result: len(result) > 0)
@beartype
def generate_changelog(
    config: Config,
    added: dict[str, ReleaseInfo],
    updated: dict[str, UpdatedReleaseInfo],
    removed: dict[str, RemovedReleaseInfo],
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
