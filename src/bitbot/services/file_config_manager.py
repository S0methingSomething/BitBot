"""A service for managing the bot's configuration."""

from pathlib import Path

import toml

from ..data.models import Config
from ..interfaces.config_protocol import ConfigManagerProtocol


class FileConfigManager(ConfigManagerProtocol):
    """Manages the bot's configuration."""

    def __init__(self, config_path: Path) -> None:
        """Initializes the FileConfigManager."""
        self.config_path = config_path

    async def load_config(self) -> Config:
        """Loads the configuration from a file."""
        with self.config_path.open("r") as f:
            config_data = toml.load(f)
        return Config(**config_data)
