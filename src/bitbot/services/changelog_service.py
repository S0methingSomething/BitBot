"""Service for generating a changelog from a list of releases."""

from ..models.changelog import Changelog, ChangelogEntry
from ..models.config import Config
from .parsing_service import ParsingService


class ChangelogService:
    """A service for generating a changelog from a list of releases."""

    def __init__(self, parsing_service: ParsingService, config: Config):
        """Initialize the ChangelogService."""
        self._parsing_service = parsing_service
        self._config = config

    def generate_changelog(self, releases: list[dict]) -> Changelog:
        """Generate a changelog from a list of releases."""
        changelog = Changelog()
        for release in releases:
            parsed_info = self._parsing_service.parse_release_notes(release.get("body", ""), self._config)
            if not parsed_info:
                continue

            entry = ChangelogEntry(**parsed_info)
            # For now, we'll just assume all new releases are "added".
            # The logic for "updated" and "removed" will be added later.
            changelog.added.append(entry)

        return changelog
