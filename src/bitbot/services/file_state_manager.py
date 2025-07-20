"""A service for managing the bot's state."""

import json
from pathlib import Path

from ..data.models import BotState
from ..interfaces.state_protocol import StateManagerProtocol


class FileStateManager(StateManagerProtocol):
    """Manages the bot's state."""

    def __init__(self, state_path: Path) -> None:
        """Initializes the FileStateManager."""
        self.state_path = state_path

    async def load_state(self) -> BotState:
        """Loads the bot's state from a file."""
        if not self.state_path.exists():
            return BotState()
        with self.state_path.open("r") as f:
            state_data = json.load(f)
        return BotState(**state_data)

    async def save_state(self, state: BotState) -> None:
        """Saves the bot's state to a file."""
        with self.state_path.open("w") as f:
            json.dump(state.dict(), f, indent=2)
