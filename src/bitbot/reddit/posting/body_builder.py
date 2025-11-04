"""Reddit post body generation."""

import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import deal
from beartype import beartype
from jinja2 import Environment, FileSystemLoader

from bitbot import paths
from bitbot.config_models import Config
from bitbot.reddit.posting.changelog import generate_changelog


@deal.pre(lambda config, _a: isinstance(config, Config))
@deal.pre(lambda _c, all_releases_data: isinstance(all_releases_data, dict))
@deal.post(lambda result: len(result) > 0)
@beartype
def generate_available_list(config: Config, all_releases_data: dict[str, Any]) -> str:
    """Generate available apps table."""
    formats: dict[str, str] = config.reddit.formats.table
    header = formats.get("header", "| App | Asset | Version |")
    divider = formats.get("divider", "|---|---|---:|")
    line_format = formats.get("line", "| {{display_name}} | {{asset_name}} | v{{version}} |")
    table_lines = [header, divider]
    asset_name: str = config.github.asset_file_name
    sorted_apps = sorted(all_releases_data.items(), key=lambda item: item[1]["display_name"])

    for _, release_info in sorted_apps:
        if release_info.get("latest_release"):
            line = (
                line_format.replace("{{display_name}}", release_info["display_name"])
                .replace("{{asset_name}}", asset_name)
                .replace("{{version}}", release_info["latest_release"]["version"])
            )
            table_lines.append(line)
    return "\n".join(table_lines)


@deal.pre(lambda config, _ch, _ar, _p: isinstance(config, Config))
@deal.pre(lambda _c, changelog_data, _ar, _p: isinstance(changelog_data, dict))
@deal.pre(lambda _c, _ch, all_releases_data, _p: isinstance(all_releases_data, dict))
@deal.pre(lambda _c, _ch, _ar, page_url: len(page_url) > 0)
@deal.post(lambda result: len(result) > 0)
@beartype
def generate_post_body(
    config: Config,
    changelog_data: dict[str, Any],
    all_releases_data: dict[str, Any],
    page_url: str,
) -> str:
    """Generate complete post body."""
    template_name = Path(config.reddit.templates.post).name
    template_path = Path(paths.TEMPLATES_DIR) / template_name

    # Load template content
    with template_path.open(encoding="utf-8") as f:
        template_content = f.read()

    # Remove tutorial block if present
    ignore_block: dict[str, str] = config.skip_content
    start_marker = ignore_block.get("startTag")
    end_marker = ignore_block.get("endTag")
    if start_marker and end_marker and start_marker in template_content:
        pattern = re.compile(f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
        template_content = re.sub(pattern, "", template_content)

    # Render with Jinja2 (autoescape=False is safe for Markdown, not HTML)
    env = Environment(
        loader=FileSystemLoader(paths.TEMPLATES_DIR),
        autoescape=False,  # noqa: S701
    )
    template = env.from_string(template_content)
    changelog = generate_changelog(config, **changelog_data)
    available_list = generate_available_list(config, all_releases_data)

    now = datetime.now(UTC)
    update_timestamp = now.strftime("%b %d, %Y - %I:%M %p UTC")
    app_count = sum(1 for data in all_releases_data.values() if data.get("latest_release"))

    post_body = template.render(
        changelog=changelog,
        available_list=available_list,
        bot_name=config.reddit.bot_name,
        bot_repo=config.github.bot_repo,
        asset_name=config.github.asset_file_name,
        creator_username=config.reddit.creator,
        download_portal_url=page_url,
        update_timestamp=update_timestamp,
        app_count=app_count,
    )

    return post_body.strip()
