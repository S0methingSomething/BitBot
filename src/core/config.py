"""Configuration management for BitBot."""

import sys
from pathlib import Path
from typing import Any

import deal
import toml
from beartype import BeartypeConf, BeartypeStrategy, beartype

import paths

# Strict beartype configuration
BEARTYPE_STRICT = BeartypeConf(strategy=BeartypeStrategy.On)


@deal.post(lambda result: len(result) > 0, message="Config must not be empty")  # type: ignore[misc]
@deal.post(lambda result: "github" in result, message="Config must have 'github' key")  # type: ignore[misc]
@deal.post(lambda result: "reddit" in result, message="Config must have 'reddit' key")  # type: ignore[misc]
@beartype(conf=BEARTYPE_STRICT)  # type: ignore[misc]
def load_config() -> dict[str, Any]:
    """Loads the main configuration file (config.toml)."""
    try:
        with Path(paths.CONFIG_FILE).open() as f:
            return toml.load(f)  # type: ignore[no-any-return]
    except FileNotFoundError:
        sys.exit(1)
    except Exception:  # noqa: BLE001
        sys.exit(1)
