"""A factory for creating services."""

from pathlib import Path
from typing import Any, Dict

from .data.models import Settings
from .services.file_config_manager import FileConfigManager
from .services.file_state_manager import FileStateManager
from .services.file_template_manager import FileTemplateManager
from .services.github_manager import GitHubManager
from .services.praw_manager import PrawManager


def create_services(settings: Settings) -> Dict[str, Any]:
    """Creates the services for the bot."""
    return {
        "config_manager": FileConfigManager(Path("config.toml")),
        "state_manager": FileStateManager(Path("data/bot_state.json")),
        "template_manager": FileTemplateManager(Path("templates")),
        "github_manager": GitHubManager(settings.GITHUB_TOKEN),
        "reddit_manager": PrawManager(
            client_id=settings.REDDIT_CLIENT_ID,
            client_secret=settings.REDDIT_CLIENT_SECRET,
            user_agent=settings.REDDIT_USER_AGENT,
            username=settings.REDDIT_USERNAME,
            password=settings.REDDIT_PASSWORD,
        ),
    }