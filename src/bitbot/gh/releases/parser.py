"""GitHub release description parsing."""

from typing import Any, TypedDict, cast

from beartype import beartype


class ParsedRelease(TypedDict):
    """Parsed release information."""

    app_id: str
    display_name: str
    version: str
    asset_name: str


@beartype
def parse_release_description(
    description: str, apps_config: list[dict[str, Any]]
) -> list[ParsedRelease]:
    """Parses a release description with a structured key-value format."""
    found_releases: list[ParsedRelease] = []
    current_release: dict[str, Any] = {}
    app_id_map = {app["displayName"].lower(): app["id"] for app in apps_config}

    for raw_line in description.splitlines():
        line = raw_line.strip()
        if not line:
            if current_release:
                found_releases.append(cast("ParsedRelease", current_release))
            current_release = {}
            continue

        try:
            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()

            if key == "app":
                if current_release:
                    found_releases.append(cast("ParsedRelease", current_release))
                app_id = app_id_map.get(value.lower())
                current_release = {"app_id": app_id, "display_name": value} if app_id else {}
            elif current_release:
                if key == "version":
                    current_release["version"] = value
                elif key == "asset_name":
                    current_release["asset_name"] = value
        except ValueError:
            continue

    if current_release:
        found_releases.append(cast("ParsedRelease", current_release))

    return found_releases
