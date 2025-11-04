"""Credential management for BitBot."""

import os

import deal
from beartype import beartype

from bitbot.config_models import Config


class Credentials:
    """Centralized credential management with type safety and error handling."""

    @staticmethod
    @deal.post(lambda result: len(result) > 0, message="GitHub token cannot be empty")
    @beartype
    def get_github_token() -> str:
        """Get GitHub token from environment."""
        token = os.getenv("GITHUB_TOKEN", "")
        if not token:
            msg = "GITHUB_TOKEN environment variable not set"
            raise ValueError(msg)
        return token

    @staticmethod
    @beartype
    def get_github_output() -> str:
        """Get GitHub Actions output file path (empty string is valid)."""
        return os.getenv("GITHUB_OUTPUT", "")

    @staticmethod
    @deal.post(lambda result: len(result) > 0, message="Reddit client ID cannot be empty")
    @beartype
    def get_reddit_client_id() -> str:
        """Get Reddit client ID from environment."""
        value = os.getenv("REDDIT_CLIENT_ID", "")
        if not value:
            msg = "REDDIT_CLIENT_ID environment variable not set"
            raise ValueError(msg)
        return value

    @staticmethod
    @deal.post(lambda result: len(result) > 0, message="Reddit client secret cannot be empty")
    @beartype
    def get_reddit_client_secret() -> str:
        """Get Reddit client secret from environment."""
        value = os.getenv("REDDIT_CLIENT_SECRET", "")
        if not value:
            msg = "REDDIT_CLIENT_SECRET environment variable not set"
            raise ValueError(msg)
        return value

    @staticmethod
    @deal.post(lambda result: len(result) > 0, message="Reddit user agent cannot be empty")
    @beartype
    def get_reddit_user_agent(config: Config | None = None) -> str:
        """Get Reddit user agent from config or environment."""
        if config:
            return config.reddit.user_agent
        value = os.getenv("REDDIT_USER_AGENT", "")
        if not value:
            msg = "REDDIT_USER_AGENT environment variable not set"
            raise ValueError(msg)
        return value

    @staticmethod
    @deal.post(lambda result: len(result) > 0, message="Reddit username cannot be empty")
    @beartype
    def get_reddit_username() -> str:
        """Get Reddit username from environment."""
        value = os.getenv("REDDIT_USERNAME", "")
        if not value:
            msg = "REDDIT_USERNAME environment variable not set"
            raise ValueError(msg)
        return value

    @staticmethod
    @deal.post(lambda result: len(result) > 0, message="Reddit password cannot be empty")
    @beartype
    def get_reddit_password() -> str:
        """Get Reddit password from environment."""
        value = os.getenv("REDDIT_PASSWORD", "")
        if not value:
            msg = "REDDIT_PASSWORD environment variable not set"
            raise ValueError(msg)
        return value
