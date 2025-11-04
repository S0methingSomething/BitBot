"""State management for BitBot."""

import json
from pathlib import Path

import deal
from beartype import beartype

from bitbot import paths
from bitbot.core.credentials import Credentials
from bitbot.core.errors import StateError
from bitbot.core.result import Err, Ok, Result
from bitbot.models import AccountState, BotState, GlobalState


@deal.post(lambda result: isinstance(result, Path), message="Must return valid Path")
@beartype
def get_account_state_file() -> Path:
    """Get path to account-specific state file based on Reddit username."""
    username = Credentials.get_reddit_username()
    return paths.ROOT_DIR / f"bot_state_{username}.json"


@deal.post(lambda result: isinstance(result, Ok | Err))
@beartype
def load_global_state() -> Result[GlobalState, StateError]:
    """Load global state (offline versions from bot's repo)."""
    try:
        with Path(paths.BOT_STATE_FILE).open() as f:
            data = json.load(f)

        # Backward compatibility: extract offline only if old format
        offline_data = {"offline": data.get("offline", {})} if "online" in data else data

        state = GlobalState(**offline_data)
    except FileNotFoundError:
        state = GlobalState()
    except json.JSONDecodeError as e:
        return Err(StateError(f"Invalid JSON in global state file: {e}"))
    except (OSError, ValueError) as e:
        return Err(StateError(f"Failed to load global state: {e}"))

    return Ok(state)


@deal.post(lambda result: isinstance(result, Ok | Err))
@beartype
def load_account_state() -> Result[AccountState, StateError]:
    """Load account-specific state (online versions, posts)."""
    try:
        account_file = get_account_state_file()
        with account_file.open() as f:
            data = json.load(f)
            state = AccountState(**data)
    except FileNotFoundError:
        # First time for this account - create empty state
        state = AccountState()
    except json.JSONDecodeError as e:
        return Err(StateError(f"Invalid JSON in account state file: {e}"))
    except (OSError, ValueError) as e:
        return Err(StateError(f"Failed to load account state: {e}"))

    return Ok(state)


@deal.pre(lambda state: hasattr(state, "model_dump"))
@beartype
def save_global_state(state: GlobalState) -> Result[None, StateError]:
    """Save global state (offline versions)."""
    try:
        state_file = Path(paths.BOT_STATE_FILE)
        temp_file = state_file.with_suffix(".tmp")
        with temp_file.open("w") as f:
            json.dump(state.model_dump(by_alias=True), f, indent=2)
        temp_file.replace(state_file)
        return Ok(None)
    except (OSError, ValueError) as e:
        return Err(StateError(f"Failed to save global state: {e}"))


@deal.pre(lambda state: hasattr(state, "model_dump"))
@beartype
def save_account_state(state: AccountState) -> Result[None, StateError]:
    """Save account-specific state (online versions, posts)."""
    try:
        account_file = get_account_state_file()
        temp_file = account_file.with_suffix(".tmp")
        with temp_file.open("w") as f:
            json.dump(state.model_dump(by_alias=True), f, indent=2)
        temp_file.replace(account_file)
        return Ok(None)
    except (OSError, ValueError) as e:
        return Err(StateError(f"Failed to save account state: {e}"))


# Backward compatibility functions
@deal.post(lambda result: isinstance(result, Ok | Err))
@beartype
def load_bot_state() -> Result[BotState, StateError]:
    """Load bot state (backward compatibility - loads account state)."""
    return load_account_state()


@deal.pre(lambda state: hasattr(state, "model_dump"))
@beartype
def save_bot_state(state: BotState) -> Result[None, StateError]:
    """Save bot state (backward compatibility - saves account state)."""
    return save_account_state(state)


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
