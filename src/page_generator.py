import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

import paths
from helpers import load_config
from logging_config import get_logger

logging = get_logger(__name__)


def _render_release_loop(template: str, releases: List[Dict[str, Any]]) -> str:
    """Renders the inner loop for previous releases."""
    release_loop_pattern = re.compile(r"<!-- BEGIN-RELEASE-LOOP -->(.*?)<!-- END-RELEASE-LOOP -->", re.DOTALL)
    match = release_loop_pattern.search(template)
    if not match:
        return template

    release_template = match.group(1)
    all_releases_html = []
    for release in releases:
        release_html = release_template.replace("{{release.version}}", release.get("version", "N/A"))
        release_html = release_html.replace("{{release.download_url}}", release.get("download_url", "#"))
        release_html = release_html.replace("{{release.published_at}}", release.get("published_at", ""))
        all_releases_html.append(release_html)
    return release_loop_pattern.sub("".join(all_releases_html), template)

def _render_app_template(app_template: str, app_data: Dict[str, Any]) -> str:
    """Renders a single app's data into the template."""
    app_html = app_template
    conditional_pattern = re.compile(r"<!-- IF RELEASES EXIST -->(.*?)<!-- ELSE -->(.*?)<!-- END IF -->", re.DOTALL)
    if match := conditional_pattern.search(app_html):
        if_template, else_template = match.groups()
        app_html = conditional_pattern.sub(if_template if app_data.get("latest_release") else else_template, app_html)

    app_html = app_html.replace("{{app.display_name}}", app_data["display_name"])
    if latest := app_data.get("latest_release"):
        app_html = app_html.replace("{{app.latest_release.version}}", latest.get("version", "N/A"))
        app_html = app_html.replace("{{app.latest_release.published_at}}", latest.get("published_at", ""))
        app_html = app_html.replace("{{app.latest_release.download_url}}", latest.get("download_url", "#"))

    return _render_release_loop(app_html, app_data.get("previous_releases", []))

def _render_template(template_content: str, data: Dict[str, Any], config: Dict[str, Any]) -> str:
    """
    Renders a template with a clean data structure, supporting nested loops and
    conditional blocks.
    """
    app_loop_pattern = re.compile(r"<!-- BEGIN-APP-LOOP -->(.*?)<!-- END-APP-LOOP -->", re.DOTALL)
    app_template_match = app_loop_pattern.search(template_content)

    if not app_template_match:
        return "<!-- APP-LOOP not found in template -->"

    app_template = app_template_match.group(1)
    all_app_html = []
    sorted_app_ids = sorted(data.keys(), key=lambda k: data[k]["display_name"])

    for app_id in sorted_app_ids:
        all_app_html.append(_render_app_template(app_template, data[app_id]))

    final_html = app_loop_pattern.sub("".join(all_app_html), template_content)
    return final_html.replace("{{bot_repo}}", config["github"]["botRepo"])

def main() -> None:
    config = load_config()
    releases_json_path = Path(paths.RELEASES_JSON_FILE)
    if not releases_json_path.exists():
        logging.error(f"Release data file not found at '{releases_json_path}'. Cannot generate page.")
        sys.exit(1)

    releases_data = json.loads(releases_json_path.read_text())
    custom_template_name = config["reddit"]["templates"].get("custom_landing")
    template_path = Path(paths.TEMPLATES_DIR) / (custom_template_name or "default_landing_page.html")
    if not template_path.exists():
        template_path = Path(paths.DEFAULT_LANDING_PAGE)

    logging.info(f"Using template: {template_path}")
    template_content = template_path.read_text()
    final_html = _render_template(template_content, releases_data, config)

    dist_dir = Path(paths.DIST_DIR)
    dist_dir.mkdir(exist_ok=True)
    output_path = dist_dir / "index.html"
    output_path.write_text(final_html)
    logging.info(f"Successfully generated landing page at: {output_path}")

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    main()
