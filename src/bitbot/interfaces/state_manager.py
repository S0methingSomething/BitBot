"""Protocol for managing bot state."""

from typing import Protocol

from bitbot.data.models import BotState


class StateManagerProtocol(Protocol):
    """Defines the interface for a state manager."""

    async def load_state(self) -> BotState:
        """
        Loads the bot's state.

        Returns:
            BotState: The loaded state object.
        """
        ...

    async def save_state(self, state: BotState) -> None:
        """
        Saves the bot's state.

        Args:
            state: The state object to save.
        """
        ...
