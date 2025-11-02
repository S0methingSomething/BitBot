"""Reddit post content parsing."""

import re

import deal
import praw.models
from beartype import beartype

from config_models import Config


@deal.pre(lambda post, config: post is not None)
@deal.pre(lambda post, config: isinstance(config, Config))
@deal.post(lambda result: isinstance(result, dict))
@beartype
def parse_versions_from_post(post: praw.models.Submission, config: Config) -> dict[str, str]:
    """Parses the versions of all apps from a Reddit post.

    Supports both legacy and new post formats.
    """
    versions = {}
    apps_config = config.model_dump().get("apps", [])
    app_map_by_display_name = {app["displayName"].lower(): app["id"] for app in apps_config}

    # New Format: Parse Changelog from Body
    changelog_match = re.search(r"## Changelog\n(.+)", post.selftext, re.DOTALL)
    if changelog_match:
        changelog_text = changelog_match.group(1)
        for line in changelog_text.splitlines():
            for display_name, app_id in app_map_by_display_name.items():
                version_match = re.search(
                    rf"{re.escape(display_name)}.*?to version ([\d\.]+)", line, re.IGNORECASE
                )
                if version_match:
                    versions[app_id] = version_match.group(1)
                    break

    # Legacy Format: Parse from Title
    if not versions:
        for display_name, app_id in app_map_by_display_name.items():
            version_match = re.search(
                rf"for {re.escape(display_name)} v([\d\.]+)", post.title, re.IGNORECASE
            )
            if version_match:
                versions[app_id] = version_match.group(1)
                break

    return versions
