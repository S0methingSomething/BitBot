"""GitHub release note parsing."""

import re
from typing import TypedDict

import deal
from beartype import beartype

from bitbot.config_models import Config


class ParsedRelease(TypedDict):
    """Parsed release information."""

    app_id: str
    display_name: str
    version: str
    asset_name: str


@deal.pre(lambda body, tag_name, title, config: body is not None)
@deal.pre(lambda body, tag_name, title, config: isinstance(config, Config))
@deal.post(lambda result: result is None or isinstance(result, dict))
@beartype
def parse_release_notes(
    body: str, tag_name: str, title: str, config: Config
) -> ParsedRelease | None:
    """Parses release information from its body, tag, or title to support all legacy formats."""
    app_map_by_id = {app["id"]: app["displayName"] for app in config.apps}

    # Priority 1: New Structured Format
    parsing_keys = config.parsing
    parsing_keys.get("app_key", "app")
    parsing_keys.get("version_key", "version")
    parsing_keys.get("asset_name_key", "asset_name")

    app_match = re.search(r"^{app_key}:\s*(\S+)", body, re.MULTILINE)
    version_match = re.search(r"^{version_key}:\s*([\d\.]+)", body, re.MULTILINE)
    asset_match = re.search(r"^{asset_name_key}:\s*(\S+)", body, re.MULTILINE)

    if app_match and version_match and asset_match:
        app_id = app_match.group(1)
        display_name = app_map_by_id.get(app_id)
        if display_name:
            return {
                "app_id": app_id,
                "display_name": display_name,
                "version": version_match.group(1),
                "asset_name": asset_match.group(1),
            }

    # Priority 2: Legacy Tag Format
    for app_id, display_name in app_map_by_id.items():
        if tag_name.lower().startswith(f"{app_id.lower()}-v"):
            version_part = tag_name.split("-v")
            if len(version_part) == 2:
                return {
                    "app_id": app_id,
                    "display_name": display_name,
                    "version": version_part[1],
                    "asset_name": config["github"]["assetFileName"],
                }

    # Priority 3: Title Format
    for app_id, display_name in app_map_by_id.items():
        match = re.search(rf"{re.escape(display_name)}.*?v([\d\.]+)", title, re.IGNORECASE)
        if match:
            return {
                "app_id": app_id,
                "display_name": display_name,
                "version": match.group(1),
                "asset_name": config["github"]["assetFileName"],
            }

    # Priority 4: Fallback
    if "bitlife" in app_map_by_id:
        match = re.search(r"(\d+\.\d+\.\d+)", tag_name)
        if match:
            return {
                "app_id": "bitlife",
                "display_name": "BitLife",
                "version": match.group(1),
                "asset_name": config["github"]["assetFileName"],
            }

    return None
