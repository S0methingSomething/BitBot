"""Reddit post body generation."""

import re
from pathlib import Path
from typing import Any

import deal
from beartype import beartype

import paths
from reddit.posting.changelog import generate_changelog


@deal.pre(lambda config, _a: isinstance(config, dict))  # type: ignore[misc]
@deal.pre(lambda _c, all_releases_data: isinstance(all_releases_data, dict))  # type: ignore[misc]
@deal.post(lambda result: len(result) > 0)  # type: ignore[misc]
@beartype
def generate_available_list(config: dict[str, Any], all_releases_data: dict[str, Any]) -> str:
    """Generate available apps table."""
    formats: dict[str, str] = config["reddit"]["formats"]["table"]
    header = formats.get("header", "| App | Asset | Version |")
    divider = formats.get("divider", "|---|---|---:|")
    line_format = formats.get("line", "| {{display_name}} | {{asset_name}} | v{{version}} |")
    table_lines = [header, divider]
    asset_name: str = config["github"].get("assetFileName", "asset")
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


@deal.pre(lambda config, _ch, _ar, _p: isinstance(config, dict))  # type: ignore[misc]
@deal.pre(lambda _c, changelog_data, _ar, _p: isinstance(changelog_data, dict))  # type: ignore[misc]
@deal.pre(lambda _c, _ch, all_releases_data, _p: isinstance(all_releases_data, dict))  # type: ignore[misc]
@deal.pre(lambda _c, _ch, _ar, page_url: len(page_url) > 0)  # type: ignore[misc]
@deal.post(lambda result: len(result) > 0)  # type: ignore[misc]
@beartype
def generate_post_body(
    config: dict[str, Any],
    changelog_data: dict[str, Any],
    all_releases_data: dict[str, Any],
    page_url: str,
) -> str:
    """Generate complete post body."""
    template_name = Path(config["reddit"]["templates"]["post"]).name
    template_path = paths.get_template_path(template_name)
    with Path(template_path).open(encoding="utf-8") as f:
        raw_template = f.read()

    ignore_block: dict[str, str] = config.get("skipContent", {})
    start_marker = ignore_block.get("startTag")
    end_marker = ignore_block.get("endTag")
    if start_marker and end_marker and start_marker in raw_template:
        pattern = re.compile(f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
        clean_template = re.sub(pattern, "", raw_template)
    else:
        clean_template = raw_template

    post_body_template = clean_template.strip()
    changelog = generate_changelog(config, **changelog_data)
    available_list = generate_available_list(config, all_releases_data)
    initial_status_line = config["feedback"]["statusLineFormat"].replace(
        "{{status}}", config["feedback"]["labels"]["unknown"]
    )

    placeholders = {
        "{{changelog}}": changelog,
        "{{available_list}}": available_list,
        "{{bot_name}}": config["reddit"]["botName"],
        "{{bot_repo}}": config["github"]["botRepo"],
        "{{asset_name}}": config["github"]["assetFileName"],
        "{{creator_username}}": config["reddit"]["creator"],
        "{{initial_status}}": initial_status_line,
        "{{download_portal_url}}": page_url,
    }

    post_body = post_body_template
    for placeholder, value in placeholders.items():
        post_body = post_body.replace(placeholder, str(value))
    return post_body
