"""Service for loading and providing application configuration."""

import toml

from ..models.config import Config
from .logging_service import LoggingService


class ConfigService:
    """A service for loading and providing application configuration."""

    def __init__(self, logging_service: LoggingService, config_path: str = "config.toml"):
        """Initialize the ConfigService.

        Args:
            logging_service: The logging service.
            config_path: The path to the configuration file.

        """
        self._logger = logging_service
        self._config_path = config_path
        self._config = self._load_config()

    def _load_config(self) -> Config:
        """Load the configuration from the TOML file and validate it.

        Returns:
            The validated configuration object.

        """
        try:
            with open(self._config_path) as f:
                data = toml.load(f)
                return Config.model_validate(data)
        except FileNotFoundError as e:
            self._logger.error(f"Configuration file not found at '{self._config_path}'.")
            raise e
        except Exception as e:
            self._logger.error(f"Failed to load or parse configuration: {e}")
            raise e

    def get_config(self) -> Config:
        """Return the loaded configuration.

        Returns:
            The configuration object.

        """
        return self._config
