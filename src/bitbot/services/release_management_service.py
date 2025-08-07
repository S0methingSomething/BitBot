"""Service for managing the release process."""

from ..services.config_service import ConfigService
from ..services.file_patcher_service import FilePatcherService
from ..services.github_service import GitHubService
from ..services.logging_service import LoggingService
from ..services.parsing_service import ParsingService
from ..services.state_service import StateService


class ReleaseManagementService:
    """Orchestrates the entire release management process."""

    def __init__(
        self,
        logging_service: LoggingService,
        config_service: ConfigService,
        github_service: GitHubService,
        state_service: StateService,
        parsing_service: ParsingService,
        file_patcher_service: FilePatcherService,
    ):
        """Initialize the ReleaseManagementService."""
        self._logger = logging_service
        self._config = config_service.get_config()
        self._github = github_service
        self._state = state_service
        self._parsing = parsing_service
        self._patcher = file_patcher_service

    def process_new_releases(self) -> None:
        """Check for and process new releases."""
        self._logger.debug("Entering: process_new_releases...")
        self._logger.info("Starting release management process...")
        source_releases = self._github.get_source_releases()
        release_state = self._state.load_release_state()

        new_releases = [r for r in source_releases if r["id"] not in release_state]

        if not new_releases:
            self._logger.info("No new source releases found to process.")
            self._logger.debug("Exiting: process_new_releases")
            return

        self._logger.info(f"Found {len(new_releases)} new source release(s) to process.")
        new_releases.sort(key=lambda r: r["created_at"])

        for release in new_releases:
            self._process_release(release)
            release_state.append(release["id"])

        self._state.save_release_state(release_state)
        self._logger.info("Release management complete.")
        self._logger.debug("Exiting: process_new_releases")

    def _process_release(self, release: dict) -> None:
        """Process a single source release."""
        self._logger.info(f"--- Processing source release: {release['tag_name']} ({release['id']}) ---")
        parsed_info = self._parsing.parse_release_notes(release.get("body", ""), self._config)

        if not parsed_info:
            self._logger.warning("Could not parse release info. Skipping.")
            return

        app_id = parsed_info.get("app_id")
        version = parsed_info.get("version")
        asset_name = parsed_info.get("asset_name")

        if not all([app_id, version, asset_name]):
            self._logger.warning(f"Skipping incomplete app info: {parsed_info}")
            return

        bot_release_tag = f"{app_id}-v{version}"
        if self._github.check_release_exists(bot_release_tag):
            self._logger.info(f"Release '{bot_release_tag}' already exists. Skipping.")
            return

        # This is where the download, patch, and upload logic will go.
        # For now, we'll just print a success message.
        self._logger.info(f"Successfully processed release {release['id']}")
