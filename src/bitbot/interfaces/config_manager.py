"""Protocol for managing configuration."""

from typing import Protocol

from bitbot.data.models import Config


class ConfigManagerProtocol(Protocol):
    """Defines the interface for a configuration manager."""

    async def load_config(self) -> Config:
        """
        Loads the application configuration.

        Returns:
            Config: The loaded configuration object.
        """
        ...
