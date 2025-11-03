"""Release management and GitHub operations."""

import deal
from beartype import beartype

from bitbot.core.config import load_config
from bitbot.core.state import load_release_state, save_release_state
from bitbot.gh.parser import parse_release_notes
from bitbot.gh.releases.creator import create_bot_release
from bitbot.gh.releases.downloader import download_asset
from bitbot.gh.releases.fetcher import check_if_bot_release_exists, get_source_releases
from bitbot.gh.releases.parser import parse_release_description
from bitbot.gh.releases.patcher import patch_file


@deal.post(lambda result: result is None)  # type: ignore[misc]
@beartype  # type: ignore[misc]
def main() -> None:
    """Process source releases and create patched bot releases."""
    config = load_config()
    source_repo = config["github"]["sourceRepo"]
    bot_repo = config["github"]["botRepo"]
    apps_config = config.get("apps", [])

    processed_release_ids = load_release_state()
    source_releases = get_source_releases(source_repo)

    for release in source_releases:
        release_id = release["id"]
        if release_id in processed_release_ids:
            continue

        tag_name = release["tag_name"]
        release_title = release.get("name", tag_name)
        release_body = release.get("body", "")

        # Try structured format first
        parsed_releases = parse_release_description(release_body, apps_config)

        if not parsed_releases:
            # Fallback to legacy parser
            parsed_info = parse_release_notes(release_body, tag_name, release_title, config)
            if parsed_info:
                parsed_releases = [parsed_info]

        if not parsed_releases:
            processed_release_ids.append(release_id)
            save_release_state(processed_release_ids)
            continue

        # Process each app in the release
        for app_info in parsed_releases:
            app_id = app_info.get("app_id")
            display_name = app_info.get("display_name")
            version = app_info.get("version")
            asset_name = app_info.get("asset_name", config["github"]["assetFileName"])

            if not all([app_id, display_name, version]):
                continue

            bot_tag = f"{app_id}-v{version}"

            if check_if_bot_release_exists(bot_repo, bot_tag):
                continue

            try:
                # Download, patch, and create release
                original_path = download_asset(source_repo, release_id, asset_name)
                patched_path = patch_file(original_path, asset_name)

                title_template = config["messages"]["releaseTitle"]
                notes_template = config["messages"]["releaseDescription"]

                title = title_template.replace("{{displayName}}", display_name).replace(
                    "{{version}}", version
                )
                notes = (
                    notes_template.replace("{{asset_name}}", asset_name)
                    .replace("{{displayName}}", display_name)
                    .replace("{{version}}", version)
                )

                create_bot_release(bot_repo, bot_tag, title, notes, patched_path)

            except Exception:  # noqa: BLE001
                continue

        processed_release_ids.append(release_id)
        save_release_state(processed_release_ids)


if __name__ == "__main__":
    main()
