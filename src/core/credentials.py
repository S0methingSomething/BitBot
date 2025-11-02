"""Credential management for BitBot."""

import os
from typing import Any

import deal
from beartype import beartype


class Credentials:
    """Centralized credential management with type safety and error handling."""

    @staticmethod
    @deal.post(lambda result: len(result) > 0)
    @beartype
    def get_github_token() -> str:
        """Get GitHub token from environment."""
        token = os.getenv("GITHUB_TOKEN", "")
        if not token:
            msg = "GITHUB_TOKEN environment variable not set"
            raise ValueError(msg)
        return token

    @staticmethod
    @deal.post(lambda result: isinstance(result, str))
    @beartype
    def get_github_output() -> str:
        """Get GitHub Actions output file path."""
        return os.getenv("GITHUB_OUTPUT", "")

    @staticmethod
    @deal.post(lambda result: len(result) > 0)
    @beartype
    def get_reddit_client_id() -> str:
        """Get Reddit client ID from environment."""
        return os.environ["REDDIT_CLIENT_ID"]

    @staticmethod
    @deal.post(lambda result: len(result) > 0)
    @beartype
    def get_reddit_client_secret() -> str:
        """Get Reddit client secret from environment."""
        return os.environ["REDDIT_CLIENT_SECRET"]

    @staticmethod
    @deal.post(lambda result: len(result) > 0)
    @beartype
    def get_reddit_user_agent(config: dict[str, Any] | None = None) -> str:
        """Get Reddit user agent from config or environment."""
        if config and "reddit" in config and "userAgent" in config["reddit"]:
            return config["reddit"]["userAgent"]
        return os.environ["REDDIT_USER_AGENT"]

    @staticmethod
    @deal.post(lambda result: len(result) > 0)
    @beartype
    def get_reddit_username() -> str:
        """Get Reddit username from environment."""
        return os.environ["REDDIT_USERNAME"]

    @staticmethod
    @deal.post(lambda result: len(result) > 0)
    @beartype
    def get_reddit_password() -> str:
        """Get Reddit password from environment."""
        return os.environ["REDDIT_PASSWORD"]
