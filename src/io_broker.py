"""IO broker for BitBot - centralizes all file operations."""
import json
from pathlib import Path
from typing import Any

import paths
from logging_config import get_logger

logger = get_logger(__name__)


class IOBroker:
    """Centralized IO broker for BitBot - handles all file operations."""

    def __init__(self) -> None:
        """Initialize IO broker with all file paths."""
        # Configuration files
        self.config_file = Path(paths.CONFIG_FILE)

        # State files
        self.bot_state_file = Path(paths.BOT_STATE_FILE)
        self.release_state_file = Path(paths.RELEASE_STATE_FILE)

        # Data files
        self.releases_json_file = Path(paths.RELEASES_JSON_FILE)
        self.digest_file = Path(paths.DIST_DIR) / "data" / "digest_history.json"

        # Distribution files
        self.dist_dir = Path(paths.DIST_DIR)

        # Template directory
        self.templates_dir = Path(paths.TEMPLATES_DIR)

        # Ensure directories exist
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Ensure all necessary directories exist."""
        dirs = [self.dist_dir, self.dist_dir / "data", self.templates_dir]
        for directory in dirs:
            directory.mkdir(exist_ok=True, parents=True)

    # --- JSON File Operations ---

    def load_json_file(self, file_path: str | Path) -> dict[str, Any]:
        """Load data from a JSON file."""
        try:
            path = Path(file_path)
            if path.exists():
                data = json.loads(path.read_text())
                if isinstance(data, dict):
                    return data
            return {}
        except (json.JSONDecodeError, OSError) as e:
            logger.warning(f"Could not load data from {file_path}: {e}")
            return {}

    def save_json_file(self, data: Any, file_path: str | Path) -> None:
        """Save data to a JSON file."""
        try:
            path = Path(file_path)
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_text(json.dumps(data, indent=2, default=str))
        except OSError as e:
            logger.error(f"Could not save data to {file_path}: {e}")

    # --- Text File Operations ---

    def read_text_file(self, file_path: str | Path) -> str:
        """Read text from a file."""
        try:
            return Path(file_path).read_text()
        except OSError as e:
            logger.warning(f"Could not read text from {file_path}: {e}")
            return ""

    def write_text_file(self, content: str, file_path: str | Path) -> None:
        """Write text to a file."""
        try:
            path = Path(file_path)
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_text(content)
        except OSError as e:
            logger.error(f"Could not write text to {file_path}: {e}")

    # --- Binary File Operations ---

    def read_binary_file(self, file_path: str | Path) -> bytes:
        """Read binary data from a file."""
        try:
            return Path(file_path).read_bytes()
        except OSError as e:
            logger.warning(f"Could not read binary data from {file_path}: {e}")
            return b""

    def write_binary_file(self, data: bytes, file_path: str | Path) -> None:
        """Write binary data to a file."""
        try:
            path = Path(file_path)
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_bytes(data)
        except OSError as e:
            logger.error(f"Could not write binary data to {file_path}: {e}")

    # --- Specific File Operations ---

    def load_bot_state(self) -> dict[str, Any]:
        """Load the bot's state, ensuring the nested structure exists."""
        try:
            data = self.load_json_file(self.bot_state_file)
            if isinstance(data, dict):
                state: dict[str, Any] = data
            else:
                state = {}
        except (FileNotFoundError, json.JSONDecodeError):
            state = {}

        # Ensure nested structure for robustness
        state.setdefault("online", {}).setdefault("last_posted_versions", {})
        state.setdefault("offline", {}).setdefault("last_generated_versions", {})
        return state

    def save_bot_state(self, data: dict[str, Any]) -> None:
        """Save the bot's monitoring state."""
        self.save_json_file(data, self.bot_state_file)

    def load_release_state(self) -> list[int]:
        """Load the list of processed source release IDs."""
        try:
            data = self.load_json_file(self.release_state_file)
            if isinstance(data, list):
                return data
            return []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_release_state(self, data: list[int]) -> None:
        """Save the list of processed source release IDs."""
        self.save_json_file(data, self.release_state_file)

    def load_releases_data(self) -> dict[str, Any]:
        """Load releases data."""
        return self.load_json_file(self.releases_json_file)

    def save_releases_data(self, data: dict[str, Any]) -> None:
        """Save releases data."""
        self.save_json_file(data, self.releases_json_file)

    def load_digest_history(self) -> dict[str, Any]:
        """Load the digest history from file."""
        return self.load_json_file(self.digest_file)

    def save_digest_history(self, history: dict[str, Any]) -> None:
        """Save the digest history to file."""
        self.save_json_file(history, self.digest_file)

    # --- Convenience Methods ---

    def append_to_file(self, content: str, file_path: str | Path) -> None:
        """Append content to a file."""
        try:
            path = Path(file_path)
            path.parent.mkdir(exist_ok=True, parents=True)
            with path.open("a") as f:
                f.write(content)
        except OSError as e:
            logger.error(f"Could not append to {file_path}: {e}")

    def file_exists(self, file_path: str | Path) -> bool:
        """Check if a file exists."""
        return Path(file_path).exists()

    def delete_file(self, file_path: str | Path) -> bool:
        """Delete a file."""
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
                return True
            return False
        except OSError as e:
            logger.warning(f"Could not delete {file_path}: {e}")
            return False


# Global instance for convenience
io_broker = IOBroker()
