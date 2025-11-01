"""State management for BitBot."""

import json
from pathlib import Path
from typing import Any, cast

import deal
from beartype import beartype

import paths
from core.errors import StateError
from core.result import Err, Ok, Result


@beartype  # type: ignore[misc]
def load_bot_state() -> Result[dict[str, Any], StateError]:
    """Loads the bot's monitoring state from JSON."""
    try:
        with Path(paths.BOT_STATE_FILE).open() as f:
            state = cast("dict[str, Any]", json.load(f))
    except FileNotFoundError:
        state = {}
    except json.JSONDecodeError as e:
        return Err(StateError(f"Invalid JSON in bot state file: {e}"))
    except Exception as e:  # noqa: BLE001
        return Err(StateError(f"Failed to load bot state: {e}"))

    # Ensure nested structure
    if "online" not in state:
        state["online"] = {}
    if "last_posted_versions" not in state["online"]:
        state["online"]["last_posted_versions"] = {}
    if "offline" not in state:
        state["offline"] = {}
    if "last_generated_versions" not in state["offline"]:
        state["offline"]["last_generated_versions"] = {}

    return Ok(state)


@deal.pre(lambda data: isinstance(data, dict))  # type: ignore[misc]
@deal.pre(lambda data: "online" in data or "offline" in data)  # type: ignore[misc]
@beartype  # type: ignore[misc]
def save_bot_state(data: dict[str, Any]) -> Result[None, StateError]:
    """Saves the bot's monitoring state."""
    try:
        with Path(paths.BOT_STATE_FILE).open("w") as f:
            json.dump(data, f, indent=2)
        return Ok(None)
    except Exception as e:  # noqa: BLE001
        return Err(StateError(f"Failed to save bot state: {e}"))


@beartype  # type: ignore[misc]
def load_release_state() -> Result[list[int], StateError]:
    """Loads the list of processed source release IDs."""
    try:
        with Path(paths.RELEASE_STATE_FILE).open() as f:
            data = json.load(f)
            if not isinstance(data, list) or not all(isinstance(x, int) for x in data):
                return Err(StateError("Release state must be a list of integers"))
            return Ok(cast("list[int]", data))
    except FileNotFoundError:
        return Ok([])
    except json.JSONDecodeError as e:
        return Err(StateError(f"Invalid JSON in release state file: {e}"))
    except Exception as e:  # noqa: BLE001
        return Err(StateError(f"Failed to load release state: {e}"))


@deal.pre(lambda data: isinstance(data, list))  # type: ignore[misc]
@beartype  # type: ignore[misc]
def save_release_state(data: list[int]) -> Result[None, StateError]:
    """Saves the list of processed source release IDs."""
    try:
        with Path(paths.RELEASE_STATE_FILE).open("w") as f:
            json.dump(data, f, indent=2)
        return Ok(None)
    except Exception as e:  # noqa: BLE001
        return Err(StateError(f"Failed to save release state: {e}"))
