"""Dependency injection container for BitBot."""

from typing import Any, Protocol

import praw
from beartype import beartype

from config_models import Config


class ConfigService(Protocol):
    """Protocol for configuration service."""

    def get_config(self) -> Config:
        """Load configuration."""
        ...


class StateService(Protocol):
    """Protocol for state management service."""

    def load_bot_state(self) -> dict[str, Any]:
        """Load bot state."""
        ...

    def save_bot_state(self, data: dict[str, Any]) -> None:
        """Save bot state."""
        ...

    def load_release_state(self) -> list[int]:
        """Load release state."""
        ...

    def save_release_state(self, data: list[int]) -> None:
        """Save release state."""
        ...


class RedditService(Protocol):
    """Protocol for Reddit service."""

    def get_client(self) -> praw.Reddit:
        """Get Reddit client."""
        ...


class Container:
    """Simple dependency injection container."""

    def __init__(self) -> None:
        """Initialize container."""
        self._services: dict[str, Any] = {}

    @beartype
    # Any: Generic container accepts any service type
    def register(self, name: str, service: Any) -> None:
        """Register a service."""
        self._services[name] = service

    @beartype
    # Any: Returns service of unknown type, caller must cast
    def get(self, name: str) -> Any:
        """Get a service."""
        if name not in self._services:
            msg = f"Service '{name}' not registered"
            raise KeyError(msg)
        return self._services[name]

    @beartype
    def has(self, name: str) -> bool:
        """Check if service is registered."""
        return name in self._services


# Global container instance
_container: Container | None = None


@beartype
def get_container() -> Container:
    """Get the global container instance."""
    global _container
    if _container is None:
        _container = Container()
    return _container


@beartype
def reset_container() -> None:
    """Reset the global container (for testing)."""
    global _container
    _container = None
