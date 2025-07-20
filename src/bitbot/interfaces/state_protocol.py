"""Protocol for the state management service."""

from typing import Protocol

from ..data.models import BotState


class StateManagerProtocol(Protocol):
    """A protocol for managing the bot's state."""

    async def load_state(self) -> BotState:
        """Loads the bot's state from a file."""
        ...

    async def save_state(self, state: BotState) -> None:
        """Saves the bot's state to a file."""
        ...
