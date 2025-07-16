"""This module defines custom exceptions for the BitBot application."""


class BitBotError(Exception):
    """Base class for all BitBot exceptions."""


class ConfigError(BitBotError):
    """Raised when there is an error in the configuration file."""


class StateError(BitBotError):
    """Raised when there is an error with the bot's state file."""


class RedditError(BitBotError):
    """Raised when there is an error interacting with the Reddit API."""


class GitHubError(BitBotError):
    """Raised when there is an error interacting with the GitHub API."""
