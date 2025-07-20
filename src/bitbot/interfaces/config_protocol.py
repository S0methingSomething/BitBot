"""Protocol for the configuration management service."""

from typing import Protocol

from ..data.models import Config


class ConfigManagerProtocol(Protocol):
    """A protocol for managing the bot's configuration."""

    async def load_config(self) -> Config:
        """Loads the configuration from a file."""
        ...
