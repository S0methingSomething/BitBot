"""Reddit post title generation."""

from datetime import UTC, datetime
from typing import Any

import deal
from beartype import beartype

from bitbot.config_models import Config


@deal.pre(lambda app_dict: isinstance(app_dict, dict))
@deal.post(lambda result: len(result) >= 0)
@beartype
def create_app_list(app_dict: dict[str, Any]) -> str:
    """Create formatted list of app names from dictionary."""
    parts = []
    for info in app_dict.values():
        display_name = info.get("display_name") or info.get("new", {}).get(
            "display_name", "Unknown App"
        )
        version = info.get("version") or info.get("new", {}).get("version", "?.?.?")
        parts.append(f"{display_name} v{version}")
    return ", ".join(parts)


@deal.pre(lambda config, added, updated: isinstance(config, Config))
@deal.pre(lambda config, added, updated: isinstance(added, dict))
@deal.pre(lambda config, added, updated: isinstance(updated, dict))
@deal.post(lambda result: len(result) > 0)
@beartype
def generate_dynamic_title(config: Config, added: dict[str, Any], updated: dict[str, Any]) -> str:
    """Generate dynamic title based on changes."""
    num_added = len(added)
    num_updated = len(updated)
    total_changes = num_added + num_updated
    formats: dict[str, str] = config.reddit.formats.titles

    added_list = create_app_list(added)
    updated_list = create_app_list(updated)
    title_key = None
    placeholders: dict[str, str] = {}

    if num_added > 0 and num_updated == 0:
        title_key = "added_only"
        placeholders = {"{{added_list}}": added_list}
    elif num_added == 0 and num_updated > 0:
        title_key = "updated_only_single" if num_updated == 1 else "updated_only_multi"
        placeholders = {"{{updated_list}}": updated_list}
    elif num_added > 0 and num_updated > 0:
        title_key = "mixed_single_update" if num_updated == 1 else "mixed_multi_update"
        placeholders = {"{{added_list}}": added_list, "{{updated_list}}": updated_list}

    max_changes = 3
    if total_changes > max_changes or title_key is None:
        title_key = "generic"
        placeholders = {"{{date}}": datetime.now(UTC).strftime("%Y-%m-%d")}

    title_format = formats.get(title_key, "[BitBot] Default Fallback Title")
    final_title = title_format
    for placeholder, value in placeholders.items():
        final_title = final_title.replace(placeholder, value)
    return final_title
