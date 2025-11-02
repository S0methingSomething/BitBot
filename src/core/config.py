"""Configuration management for BitBot."""

from pathlib import Path

import deal
import toml
from beartype import BeartypeConf, BeartypeStrategy, beartype
from pydantic import ValidationError

import paths
from config_models import Config
from core.errors import ConfigurationError
from core.result import Err, Ok, Result

# Strict beartype configuration
BEARTYPE_STRICT = BeartypeConf(strategy=BeartypeStrategy.On)


@deal.post(
    lambda result: result.is_err() or "github" in result.unwrap(),
    message="Config must contain 'github' section",
)
@deal.post(
    lambda result: result.is_err() or "reddit" in result.unwrap(),
    message="Config must contain 'reddit' section",
)
@beartype(conf=BEARTYPE_STRICT)
def load_config() -> Result[dict[str, dict], ConfigurationError]:
    """Loads the main configuration file (config.toml)."""
    try:
        with Path(paths.CONFIG_FILE).open() as f:
            data = toml.load(f)

        # Validate with Pydantic
        Config(**data)
        # Convert back to dict for backward compatibility
        return Ok(data)
    except FileNotFoundError:
        return Err(ConfigurationError(f"Config file not found: {paths.CONFIG_FILE}"))
    except toml.TomlDecodeError as e:
        return Err(ConfigurationError(f"Invalid TOML syntax: {e}"))
    except ValidationError as e:
        return Err(ConfigurationError(f"Invalid config structure: {e}"))
    except Exception as e:
        return Err(ConfigurationError(f"Failed to load config: {e}"))
