"""Service for managing configuration loaded from a file."""

import aiofiles
import toml

from bitbot.data.models import Config
from bitbot.interfaces.config_manager import ConfigManagerProtocol


class FileConfigManager(ConfigManagerProtocol):
    """Manages configuration loaded from a TOML file."""

    def __init__(self, path: str) -> None:
        """
        Initializes the FileConfigManager.

        Args:
            path: The path to the configuration file.
        """
        self._path = path

    async def load_config(self) -> Config:
        """
        Loads the application configuration from the TOML file.

        Returns:
            Config: The loaded configuration object.
        """
        async with aiofiles.open(self._path, "r") as f:
            content = await f.read()
            data = toml.loads(content)
        return Config(**data)
