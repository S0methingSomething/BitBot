"""Configuration management for BitBot."""

from pathlib import Path

import toml
from beartype import beartype
from pydantic import ValidationError

from bitbot import paths
from bitbot.config_models import Config
from bitbot.core.errors import ConfigurationError
from bitbot.core.result import Err, Ok, Result


@beartype
def load_config() -> Result[Config, ConfigurationError]:
    """Loads the main configuration file (config.toml)."""
    try:
        with Path(paths.CONFIG_FILE).open() as f:
            data = toml.load(f)

        # Validate with Pydantic and return model
        config = Config(**data)
        return Ok(config)
    except FileNotFoundError:
        return Err(ConfigurationError(f"Config file not found: {paths.CONFIG_FILE}"))
    except toml.TomlDecodeError as e:
        return Err(ConfigurationError(f"Invalid TOML syntax: {e}"))
    except ValidationError as e:
        return Err(ConfigurationError(f"Invalid config structure: {e}"))
    except (OSError, ValueError) as e:
        return Err(ConfigurationError(f"Failed to load config: {e}"))
