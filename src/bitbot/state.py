from typing import Any, Dict

import toml

_state: Dict[str, Any] = {}


def load_state(state_path: str = "bot_state.toml") -> None:
    """Loads the bot's current monitoring state."""
    global _state
    try:
        with open(state_path, "r") as f:
            _state = toml.load(f)
    except FileNotFoundError:
        _state = {}


def get_state() -> Dict[str, Any]:
    """Returns the loaded state."""
    return _state


def save_state(state: Dict[str, Any], state_path: str = "bot_state.toml") -> None:
    """Saves the bot's monitoring state."""
    with open(state_path, "w") as f:
        toml.dump(_state, f)
