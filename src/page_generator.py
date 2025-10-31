"""Generate static HTML landing page from release data."""

import json
import re
import sys
from pathlib import Path
from typing import Any

import deal
from beartype import beartype


@deal.pre(lambda template_content, _d, _c: len(template_content) > 0)  # type: ignore[misc]
@deal.pre(lambda _t, data, _c: isinstance(data, dict))  # type: ignore[misc]
@deal.pre(lambda _t, _d, config: isinstance(config, dict))  # type: ignore[misc]
@deal.post(lambda result: len(result) > 0)  # type: ignore[misc]
@beartype
def _render_template(template_content: str, data: dict[str, Any], config: dict[str, Any]) -> str:
    """Renders a template with a clean data structure.

    Supports nested loops and conditional blocks.
    """
    app_loop_pattern = re.compile(r"<!-- BEGIN-APP-LOOP -->(.*?)<!-- END-APP-LOOP -->", re.DOTALL)
    app_template_match = app_loop_pattern.search(template_content)

    if not app_template_match:
        return "<!-- APP-LOOP not found in template -->"

    app_template = app_template_match.group(1)
    all_app_html = []

    sorted_app_ids = sorted(data.keys(), key=lambda k: data[k]["display_name"])

    for app_id in sorted_app_ids:
        app_data = data[app_id]
        app_html = app_template

        # --- Conditional Block: Check for latest_release ---
        conditional_pattern = re.compile(
            r"<!-- IF RELEASES EXIST -->(.*?)<!-- ELSE -->(.*?)<!-- END IF -->", re.DOTALL
        )
        conditional_match = conditional_pattern.search(app_html)

        if conditional_match:
            if_template = conditional_match.group(1)
            else_template = conditional_match.group(2)

            if app_data.get("latest_release"):
                app_html = conditional_pattern.sub(if_template, app_html)
            else:
                app_html = conditional_pattern.sub(else_template, app_html)

        # --- App & Latest Release Placeholders ---
        app_html = app_html.replace("{{app.display_name}}", app_data["display_name"])
        if app_data.get("latest_release"):
            latest = app_data["latest_release"]
            app_html = app_html.replace(
                "{{app.latest_release.version}}", latest.get("version", "N/A")
            )
            app_html = app_html.replace(
                "{{app.latest_release.published_at}}", latest.get("published_at", "")
            )
            app_html = app_html.replace(
                "{{app.latest_release.download_url}}", latest.get("download_url", "#")
            )

        # --- Inner Loop: Previous Releases ---
        release_loop_pattern = re.compile(
            r"<!-- BEGIN-RELEASE-LOOP -->(.*?)<!-- END-RELEASE-LOOP -->", re.DOTALL
        )
        release_template_match = release_loop_pattern.search(app_html)

        if release_template_match:
            release_template = release_template_match.group(1)
            all_releases_html = []

            for release in app_data.get("previous_releases", []):
                release_html = release_template
                release_html = release_html.replace(
                    "{{release.version}}", release.get("version", "N/A")
                )
                release_html = release_html.replace(
                    "{{release.download_url}}", release.get("download_url", "#")
                )
                release_html = release_html.replace(
                    "{{release.published_at}}", release.get("published_at", "")
                )
                all_releases_html.append(release_html)

            app_html = release_loop_pattern.sub("".join(all_releases_html), app_html)

        all_app_html.append(app_html)

    final_html = app_loop_pattern.sub("".join(all_app_html), template_content)
    return final_html.replace("{{bot_repo}}", config["github"]["botRepo"])


@beartype  # type: ignore[misc]
def main() -> None:
    """Generate the landing page HTML from releases data."""
    config = load_config()
    if not Path(paths.RELEASES_JSON_FILE).exists():
        sys.exit(1)
    with Path(paths.RELEASES_JSON_FILE).open() as f:
        releases_data = json.load(f)
    custom_template_name = config["reddit"]["templates"].get("custom_landing")
    template_path = (
        paths.get_template_path(custom_template_name)
        if custom_template_name and Path(paths.get_template_path(custom_template_name)).exists()
        else paths.DEFAULT_LANDING_PAGE
    )
    with Path(template_path).open() as f:
        template_content = f.read()
    final_html = _render_template(template_content, releases_data, config)
    Path(paths.DIST_DIR).mkdir(parents=True, exist_ok=True)
    output_path = Path(paths.DIST_DIR) / "index.html"
    output_path.write_text(final_html)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))
    import paths
    from core.config import load_config

    main()
