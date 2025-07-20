"""Custom exceptions for the bot."""


class BitBotError(Exception):
    """Base exception for the bot."""


class GitHubError(BitBotError):
    """An error occurred while interacting with the GitHub API."""


class RedditError(BitBotError):
    """An error occurred while interacting with the Reddit API."""


class ConfigurationError(BitBotError):
    """An error occurred with the bot's configuration."""

    def __init__(self, missing_keys: list[str]) -> None:
        """Initializes the ConfigurationError."""
        self.missing_keys = missing_keys
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        if len(self.missing_keys) == 1:
            return (
                f"Configuration Error: The required environment variable "
                f"'{self.missing_keys[0]}' is not set."
            )
        else:
            keys_str = "', '".join(self.missing_keys)
            return (
                f"Configuration Error: The following required environment variables "
                f"are not set: '{keys_str}'"
            )
