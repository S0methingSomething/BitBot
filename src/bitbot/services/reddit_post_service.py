"""Service for generating Reddit posts."""

from pathlib import Path

from ..models.changelog import Changelog
from ..models.config import Config
from ..models.reddit_post import RedditPost


class RedditPostService:
    """A service for generating Reddit posts."""

    def __init__(self, config: Config):
        """Initialize the RedditPostService."""
        self._config = config

    def _get_template_content(self, template_path: str) -> str:
        """Load the content of a template file."""
        return Path(template_path).read_text()

    def generate_post(self, changelog: Changelog) -> RedditPost:
        """Generate a Reddit post from a changelog."""
        post_template = self._get_template_content(self._config.reddit.templates.post)
        # This is a placeholder for the actual template rendering logic
        # For now, we'll just create a simple title and body
        title = self._generate_title(changelog)
        body = self._generate_body(changelog, post_template)
        return RedditPost(title=title, body=body)

    def _generate_title(self, changelog: Changelog) -> str:
        """Generate the title for a Reddit post."""
        # This is a simplified version of the title generation logic
        if changelog.added:
            return f"New releases available for {len(changelog.added)} apps"
        else:
            return "No new releases"

    def _generate_body(self, changelog: Changelog, template: str) -> str:
        """Generate the body of a Reddit post."""
        # This is a simplified version of the body generation logic
        added_lines = [f"* {entry.app_id} v{entry.version}" for entry in changelog.added]
        return template.replace("{{changelog}}", "\n".join(added_lines))
