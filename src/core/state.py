"""State management for BitBot."""

import json
from pathlib import Path
from typing import Any, cast

import deal
from beartype import beartype

import paths


@deal.post(lambda result: isinstance(result, dict))  # type: ignore[misc]
@deal.post(lambda result: "online" in result)  # type: ignore[misc]
@deal.post(lambda result: "offline" in result)  # type: ignore[misc]
@beartype  # type: ignore[misc]
def load_bot_state() -> dict[str, Any]:
    """Loads the bot's monitoring state from JSON."""
    try:
        with Path(paths.BOT_STATE_FILE).open() as f:
            state = cast("dict[str, Any]", json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        state = {}

    # Ensure nested structure
    if "online" not in state:
        state["online"] = {}
    if "last_posted_versions" not in state["online"]:
        state["online"]["last_posted_versions"] = {}
    if "offline" not in state:
        state["offline"] = {}
    if "last_generated_versions" not in state["offline"]:
        state["offline"]["last_generated_versions"] = {}

    return state


@deal.pre(lambda data: isinstance(data, dict))  # type: ignore[misc]
@deal.pre(lambda data: "online" in data or "offline" in data)  # type: ignore[misc]
@beartype  # type: ignore[misc]
def save_bot_state(data: dict[str, Any]) -> None:
    """Saves the bot's monitoring state."""
    with Path(paths.BOT_STATE_FILE).open("w") as f:
        json.dump(data, f, indent=2)


@deal.post(lambda result: isinstance(result, list))  # type: ignore[misc]
@beartype  # type: ignore[misc]
def load_release_state() -> list[int]:
    """Loads the list of processed source release IDs."""
    try:
        with Path(paths.RELEASE_STATE_FILE).open() as f:
            return cast("list[int]", json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return []


@deal.pre(lambda data: isinstance(data, list))  # type: ignore[misc]
@beartype  # type: ignore[misc]
def save_release_state(data: list[int]) -> None:
    """Saves the list of processed source release IDs."""
    with Path(paths.RELEASE_STATE_FILE).open("w") as f:
        json.dump(data, f, indent=2)
