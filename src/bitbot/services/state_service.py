"""Service for managing the application's state files."""

import json

from ..models.state import BotState, ReleaseState
from .logging_service import LoggingService


class StateService:
    """Handles reading and writing state files."""

    def __init__(
        self,
        logging_service: LoggingService,
        bot_state_path: str = "bot_state.json",
        release_state_path: str = "release_state.json",
    ):
        """Initializes the StateService.

        Args:
            logging_service: The logging service.
            bot_state_path: Path to the bot state file.
            release_state_path: Path to the release state file.

        """
        self._logger = logging_service
        self._bot_state_path = bot_state_path
        self._release_state_path = release_state_path

    def load_bot_state(self) -> BotState:
        """Loads the bot's state from a JSON file."""
        try:
            with open(self._bot_state_path) as f:
                data = json.load(f)
                return BotState.model_validate(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return BotState(
                activePostId=None,
                lastMajorPostTimestamp=None,
                lastCheckTimestamp=None,
                currentIntervalSeconds=None,
                lastCommentCount=None,
            )

    def save_bot_state(self, state: BotState) -> None:
        """Saves the bot's state to a JSON file."""
        with open(self._bot_state_path, "w") as f:
            f.write(state.model_dump_json(indent=2, by_alias=True))

    def load_release_state(self) -> ReleaseState:
        """Loads the release state from a JSON file."""
        try:
            with open(self._release_state_path) as f:
                data = json.load(f)
                return ReleaseState.model_validate(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return ReleaseState()

    def save_release_state(self, state: ReleaseState) -> None:
        """Saves the release state to a JSON file."""
        with open(self._release_state_path, "w") as f:
            f.write(state.model_dump_json())
