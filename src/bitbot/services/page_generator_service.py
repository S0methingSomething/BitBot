"""Service for generating the HTML landing page."""

import re
from pathlib import Path

from ..models.config import Config
from ..models.page_data import AppData, PageData
from .logging_service import LoggingService


class PageGeneratorService:
    """A service for rendering the HTML landing page."""

    def __init__(self, config: Config, logger: LoggingService):
        """Initialize the PageGeneratorService."""
        self._config = config
        self._logger = logger

    def _get_template_content(self) -> str:
        """Load the content of the landing page template."""
        custom_template_path_str = self._config.reddit.templates.custom_landing
        if custom_template_path_str:
            custom_template_path = Path(custom_template_path_str)
            self._logger.info(f"Checking for custom template at: {custom_template_path.resolve()}")
            if custom_template_path.is_file():
                self._logger.info("Found custom template. Reading content.")
                return custom_template_path.read_text()
            else:
                self._logger.warning("Custom template not found at the specified path.")

        default_template_path = Path("templates/default_landing_page.html")
        self._logger.info(f"Using default template at: {default_template_path.resolve()}")
        return default_template_path.read_text()

    def generate_page(self, page_data: PageData) -> str:
        """Render the HTML for the landing page."""
        template_content = self._get_template_content()

        app_loop_pattern = re.compile(r"<!-- BEGIN-APP-LOOP -->(.*?)<!-- END-APP-LOOP -->", re.DOTALL)
        app_template_match = app_loop_pattern.search(template_content)

        if not app_template_match:
            return "<!-- APP-LOOP not found in template -->"

        app_template = app_template_match.group(1)
        all_app_html = []

        sorted_app_ids = sorted(page_data.apps.keys(), key=lambda k: page_data.apps[k].display_name)

        for app_id in sorted_app_ids:
            app_data = page_data.apps[app_id]
            app_html = self._render_app_template(app_template, app_data)
            all_app_html.append(app_html)

        final_html = app_loop_pattern.sub("".join(all_app_html), template_content)
        final_html = final_html.replace("{{bot_repo}}", self._config.github.bot_repo)
        return final_html

    def _render_app_template(self, app_template: str, app_data: AppData) -> str:
        """Render the HTML for a single app."""
        app_html = app_template

        # --- Conditional Block: Check for latest_release ---
        conditional_pattern = re.compile(r"<!-- IF RELEASES EXIST -->(.*?)<!-- ELSE -->(.*?)<!-- END IF -->", re.DOTALL)
        conditional_match = conditional_pattern.search(app_html)

        if conditional_match:
            if_template = conditional_match.group(1)
            else_template = conditional_match.group(2)
            app_html = conditional_pattern.sub(if_template if app_data.latest_release else else_template, app_html)

        # --- App & Latest Release Placeholders ---
        app_html = app_html.replace("{{app.display_name}}", app_data.display_name)
        if app_data.latest_release:
            latest = app_data.latest_release
            app_html = app_html.replace("{{app.latest_release.version}}", latest.version)
            app_html = app_html.replace("{{app.latest_release.published_at}}", latest.published_at)
            app_html = app_html.replace("{{app.latest_release.download_url}}", str(latest.download_url))

        # --- Inner Loop: Previous Releases ---
        release_loop_pattern = re.compile(r"<!-- BEGIN-RELEASE-LOOP -->(.*?)<!-- END-RELEASE-LOOP -->", re.DOTALL)
        release_template_match = release_loop_pattern.search(app_html)

        if release_template_match:
            release_template = release_template_match.group(1)
            all_releases_html = []
            for release in app_data.previous_releases:
                release_html = release_template
                release_html = release_html.replace("{{release.version}}", release.version)
                release_html = release_html.replace("{{release.download_url}}", str(release.download_url))
                release_html = release_html.replace("{{release.published_at}}", release.published_at)
                all_releases_html.append(release_html)
            app_html = release_loop_pattern.sub("".join(all_releases_html), app_html)

        return app_html
