"""IO handling for BitBot - centralizes local and online operations."""

from pathlib import Path
from typing import Any, cast

from io_broker import io_broker
from logging_config import get_logger

logger = get_logger(__name__)


class IOHandler:
    """Centralized IO handler for BitBot."""

    @staticmethod
    def load_bot_state() -> dict[str, Any]:
        """Load the bot's state, ensuring the nested structure exists."""
        return cast(dict[str, Any], io_broker.load_bot_state())

    @staticmethod
    def save_bot_state(data: dict[str, Any]) -> None:
        """Save the bot's monitoring state."""
        io_broker.save_bot_state(data)

    @staticmethod
    def load_release_state() -> list[int]:
        """Load the list of processed source release IDs."""
        return cast(list[int], io_broker.load_release_state())

    @staticmethod
    def save_release_state(data: list[int]) -> None:
        """Save the list of processed source release IDs."""
        io_broker.save_release_state(data)

    @staticmethod
    def load_releases_data() -> dict[str, Any]:
        """Load releases data."""
        return cast(dict[str, Any], io_broker.load_releases_data())

    @staticmethod
    def save_releases_data(data: dict[str, Any]) -> None:
        """Save releases data."""
        io_broker.save_releases_data(data)

    @staticmethod
    def load_digest_history() -> dict[str, Any]:
        """Load the digest history from file."""
        return cast(dict[str, Any], io_broker.load_digest_history())

    @staticmethod
    def save_digest_history(history: dict[str, Any]) -> None:
        """Save the digest history to file."""
        io_broker.save_digest_history(history)

    @staticmethod
    def load_json_file(file_path: Path) -> dict[str, Any]:
        """Load data from a JSON file."""
        return cast(dict[str, Any], io_broker.load_json_file(file_path))

    @staticmethod
    def save_json_file(data: Any, file_path: Path) -> None:
        """Save data to a JSON file."""
        io_broker.save_json_file(data, file_path)
