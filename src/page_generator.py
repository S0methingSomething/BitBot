import json
import re
import sys
from pathlib import Path
from typing import Any

import paths
from config_loader import load_config
from deployment import DeploymentFactory
from dry_run import is_dry_run
from logging_config import get_logger
from placeholder_parser import generate_page_placeholders, process_placeholders

logging = get_logger(__name__)


def _render_release_loop(template: str, releases: list[dict[str, Any]]) -> str:
    """Renders the inner loop for previous releases."""
    release_loop_pattern = re.compile(
        r"<!-- BEGIN-RELEASE-LOOP -->(.*?)<!-- END-RELEASE-LOOP -->", re.DOTALL
    )
    match = release_loop_pattern.search(template)
    if not match:
        return template

    release_template = match.group(1)
    all_releases_html = []
    for release in releases:
        release_html = release_template.replace(
            "{{release.version}}", release.get("version", "N/A")
        )
        release_html = release_html.replace(
            "{{release.download_url}}", release.get("download_url", "#")
        )
        release_html = release_html.replace(
            "{{release.published_at}}", release.get("published_at", "")
        )
        all_releases_html.append(release_html)
    return release_loop_pattern.sub("".join(all_releases_html), template)


def _render_app_template(app_template: str, app_data: dict[str, Any]) -> str:
    """Renders a single app's data into the template."""
    app_html = app_template
    conditional_pattern = re.compile(
        r"<!-- IF RELEASES EXIST -->(.*?)<!-- ELSE -->(.*?)<!-- END IF -->", re.DOTALL
    )
    if match := conditional_pattern.search(app_html):
        if_template, else_template = match.groups()
        app_html = conditional_pattern.sub(
            if_template if app_data.get("latest_release") else else_template, app_html
        )

    app_html = app_html.replace("{{app.display_name}}", app_data["display_name"])
    if latest := app_data.get("latest_release"):
        app_html = app_html.replace(
            "{{app.latest_release.version}}", latest.get("version", "N/A")
        )
        app_html = app_html.replace(
            "{{app.latest_release.published_at}}", latest.get("published_at", "")
        )
        app_html = app_html.replace(
            "{{app.latest_release.download_url}}", latest.get("download_url", "#")
        )

    return _render_release_loop(app_html, app_data.get("previous_releases", []))


def _render_template(template_content: str, data: dict[str, Any], config: Any) -> str:
    """
    Renders a template with a clean data structure, supporting nested loops and
    conditional blocks.
    """
    # Generate placeholders
    placeholders = generate_page_placeholders(data, config)

    # Process template with placeholders
    processed_template = process_placeholders(template_content, placeholders, config)

    # Handle app loops (existing logic)
    app_loop_pattern = re.compile(
        r"<!-- BEGIN-APP-LOOP -->(.*?)<!-- END-APP-LOOP -->", re.DOTALL
    )
    app_template_match = app_loop_pattern.search(processed_template)

    if not app_template_match:
        return "<!-- APP-LOOP not found in template -->"

    app_template = app_template_match.group(1)
    all_app_html = []
    sorted_app_ids = sorted(data.keys(), key=lambda k: data[k]["display_name"])

    all_app_html = [
        _render_app_template(app_template, data[app_id]) for app_id in sorted_app_ids
    ]

    return app_loop_pattern.sub("".join(all_app_html), processed_template)


def _handle_deployments(
    deployment_config: Any, dist_dir: Path, full_config: Any  # noqa: ARG001
) -> None:
    """Handle deployments to configured providers."""
    if not hasattr(deployment_config, "providers"):
        return

    providers = getattr(deployment_config, "providers", [])
    for provider_name in providers:
        try:
            # Get provider-specific config
            provider_config = getattr(deployment_config, provider_name, None)
            if not provider_config:
                logging.warning(f"No configuration found for provider: {provider_name}")
                continue

            # Create deployment service
            deployment_service = DeploymentFactory.create_deployment_service(
                provider_name, provider_config
            )

            # Deploy
            logging.info(f"Deploying to {deployment_service.name}...")
            result = deployment_service.deploy(dist_dir)

            if result["success"]:
                logging.info(f"✅ Successfully deployed to {deployment_service.name}")
                logging.info(f"   URL: {result['url']}")
            else:
                logging.error(f"❌ Failed to deploy to {deployment_service.name}")
                logging.error(f"   Error: {result.get('error', 'Unknown error')}")

        except Exception as e:
            logging.error(f"❌ Error deploying to {provider_name}: {e!s}")


def main() -> None:
    """Main function to generate the landing page."""
    config = load_config()
    releases_json_path = Path(paths.RELEASES_JSON_FILE)
    if not releases_json_path.exists():
        logging.error(
            f"Release data file not found at '{releases_json_path}'. Cannot generate page."
        )
        sys.exit(1)

    releases_data = json.loads(releases_json_path.read_text())
    custom_template_name = config.reddit.templates.custom_landing
    template_path = Path(paths.TEMPLATES_DIR) / (
        custom_template_name or "default_landing_page.html"
    )
    if not template_path.exists():
        template_path = Path(paths.DEFAULT_LANDING_PAGE)

    logging.info(f"Using template: {template_path}")
    template_content = template_path.read_text()
    final_html = _render_template(template_content, releases_data, config)

    if is_dry_run():
        logging.info("DRY_RUN: Would generate landing page")
        logging.info(f"  Template: {template_path}")
        logging.info(f"  Output (first 200 chars): {final_html[:200]}...")
        return

    dist_dir = Path(paths.DIST_DIR)
    dist_dir.mkdir(exist_ok=True)
    output_path = dist_dir / "index.html"
    output_path.write_text(final_html)
    logging.info(f"Successfully generated landing page at: {output_path}")

    # Handle deployments if configured
    if hasattr(config, "deployment"):
        _handle_deployments(config.deployment, dist_dir, config)

    # Handle deployments if configured
    if hasattr(config, "deployment"):
        _handle_deployments(config.deployment, dist_dir, config)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    main()
