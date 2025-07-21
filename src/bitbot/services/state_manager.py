"""Service for managing bot state stored in a JSON file."""

import json

import aiofiles

from bitbot.data.models import BotState
from bitbot.interfaces.state_manager import StateManagerProtocol


class JsonStateManager(StateManagerProtocol):
    """Manages bot state stored in a JSON file."""

    def __init__(self, path: str) -> None:
        """
        Initializes the JsonStateManager.

        Args:
            path: The path to the state file.
        """
        self._path = path

    async def load_state(self) -> BotState:
        """
        Loads the bot's state from the JSON file.

        If the file doesn't exist, it returns a default BotState object.
        """
        try:
            async with aiofiles.open(self._path, "r") as f:
                content = await f.read()
                data = json.loads(content)
            return BotState(**data)
        except FileNotFoundError:
            return BotState()

    async def save_state(self, state: BotState) -> None:
        """Saves the bot's state to the JSON file."""
        async with aiofiles.open(self._path, "w") as f:
            await f.write(json.dumps(state.model_dump(), indent=4))
