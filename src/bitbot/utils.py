"""This module contains utility functions for the BitBot application."""

import json
from pathlib import Path
from typing import Any, Dict, cast


def load_config() -> Dict[str, Any]:
    """Load the main configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path("config.json")
    with config_path.open("r") as f:
        return cast(Dict[str, Any], json.load(f))


def load_state() -> Dict[str, Any]:
    """Load the bot's current monitoring state.

    Returns:
        The state dictionary.
    """
    state_path = Path("bot_state.json")
    with state_path.open("r") as f:
        return cast(Dict[str, Any], json.load(f))


def save_state(data: Dict[str, Any]) -> None:
    """Save the bot's monitoring state.

    Args:
        data: The state dictionary to save.
    """
    state_path = Path("bot_state.json")
    with state_path.open("w") as f:
        json.dump(data, f, indent=2)