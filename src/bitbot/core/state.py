"""State management for BitBot."""

import json
from pathlib import Path

import deal
from beartype import beartype

from bitbot import paths
from bitbot.core.errors import StateError
from bitbot.core.result import Err, Ok, Result
from bitbot.models import BotState


@deal.post(lambda result: isinstance(result, Ok | Err))
@beartype
def load_bot_state() -> Result[BotState, StateError]:
    """Loads the bot's monitoring state from JSON."""
    try:
        with Path(paths.BOT_STATE_FILE).open() as f:
            data = json.load(f)
            state = BotState(**data)
    except FileNotFoundError:
        state = BotState()
    except json.JSONDecodeError as e:
        return Err(StateError(f"Invalid JSON in bot state file: {e}"))
    except (OSError, ValueError) as e:
        return Err(StateError(f"Failed to load bot state: {e}"))

    return Ok(state)


@deal.pre(lambda state: hasattr(state, "model_dump"))
@beartype
def save_bot_state(state: BotState) -> Result[None, StateError]:
    """Saves the bot's monitoring state."""
    try:
        state_file = Path(paths.BOT_STATE_FILE)
        temp_file = state_file.with_suffix(".tmp")
        with temp_file.open("w") as f:
            json.dump(state.model_dump(by_alias=True), f, indent=2)
        temp_file.replace(state_file)
        return Ok(None)
    except (OSError, ValueError) as e:
        return Err(StateError(f"Failed to save bot state: {e}"))


@deal.post(lambda result: isinstance(result, Ok | Err))
@beartype
def load_release_state() -> Result[list[int], StateError]:
    """Loads the list of processed source release IDs."""
    try:
        with Path(paths.RELEASE_STATE_FILE).open() as f:
            data = json.load(f)
            if not isinstance(data, list) or not all(isinstance(x, int) for x in data):
                return Err(StateError("Release state must be a list of integers"))
            # Type narrowed by isinstance checks above
            return Ok(data)  # type: ignore[return-value]
    except FileNotFoundError:
        return Ok([])
    except json.JSONDecodeError as e:
        return Err(StateError(f"Invalid JSON in release state file: {e}"))
    except (OSError, ValueError) as e:
        return Err(StateError(f"Failed to load release state: {e}"))


@deal.pre(lambda data: isinstance(data, list))
@beartype
def save_release_state(data: list[int]) -> Result[None, StateError]:
    """Saves the list of processed source release IDs."""
    try:
        state_file = Path(paths.RELEASE_STATE_FILE)
        temp_file = state_file.with_suffix(".tmp")
        with temp_file.open("w") as f:
            json.dump(data, f, indent=2)
        temp_file.replace(state_file)
        return Ok(None)
    except (OSError, ValueError) as e:
        return Err(StateError(f"Failed to save release state: {e}"))
