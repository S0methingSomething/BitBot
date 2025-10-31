"""GitHub release description parsing."""

from typing import Any

import deal
from beartype import beartype


@deal.pre(lambda description, apps_config: isinstance(apps_config, list))  # type: ignore[misc]
@deal.post(lambda result: isinstance(result, list))  # type: ignore[misc]
@beartype  # type: ignore[misc]
def parse_release_description(  # noqa: C901
    description: str, apps_config: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Parses a release description with a structured key-value format."""
    found_releases = []
    current_release: dict[str, Any] = {}
    app_id_map = {app["displayName"].lower(): app["id"] for app in apps_config}

    for raw_line in description.splitlines():
        line = raw_line.strip()
        if not line:
            if current_release:
                found_releases.append(current_release)
            current_release = {}
            continue

        try:
            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()

            if key == "app":
                if current_release:
                    found_releases.append(current_release)
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
        found_releases.append(current_release)

    return found_releases
