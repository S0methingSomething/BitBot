"""Configuration management for BitBot."""

from pathlib import Path
from typing import Any, cast

import deal
import toml
from beartype import BeartypeConf, BeartypeStrategy, beartype

import paths
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
def load_config() -> Result[dict[str, Any], ConfigurationError]:
    """Loads the main configuration file (config.toml)."""
    try:
        with Path(paths.CONFIG_FILE).open() as f:
            config = cast("dict[str, Any]", toml.load(f))

        # Validate required keys
        if not config:
            return Err(ConfigurationError("Config file is empty"))
        if "github" not in config:
            return Err(ConfigurationError("Config missing 'github' key"))
        if "reddit" not in config:
            return Err(ConfigurationError("Config missing 'reddit' key"))

        return Ok(config)
    except FileNotFoundError:
        return Err(ConfigurationError(f"Config file not found: {paths.CONFIG_FILE}"))
    except toml.TomlDecodeError as e:
        return Err(ConfigurationError(f"Invalid TOML syntax: {e}"))
    except Exception as e:
        return Err(ConfigurationError(f"Failed to load config: {e}"))
