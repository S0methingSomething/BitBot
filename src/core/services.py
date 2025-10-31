"""Concrete service implementations."""

from typing import Any

import praw
from beartype import beartype

from core.config import load_config as _load_config
from core.state import (
    load_bot_state as _load_bot_state,
    load_release_state as _load_release_state,
    save_bot_state as _save_bot_state,
    save_release_state as _save_release_state,
)
from reddit.client import init_reddit as _init_reddit


class DefaultConfigService:
    """Default configuration service implementation."""
    
    @beartype  # type: ignore[misc]
    def get_config(self) -> dict[str, Any]:
        """Load configuration."""
        return _load_config()  # type: ignore[no-any-return]


class DefaultStateService:
    """Default state management service implementation."""
    
    @beartype  # type: ignore[misc]
    def load_bot_state(self) -> dict[str, Any]:
        """Load bot state."""
        return _load_bot_state()  # type: ignore[no-any-return]
    
    @beartype  # type: ignore[misc]
    def save_bot_state(self, data: dict[str, Any]) -> None:
        """Save bot state."""
        _save_bot_state(data)
    
    @beartype  # type: ignore[misc]
    def load_release_state(self) -> list[int]:
        """Load release state."""
        return _load_release_state()  # type: ignore[no-any-return]
    
    @beartype  # type: ignore[misc]
    def save_release_state(self, data: list[int]) -> None:
        """Save release state."""
        _save_release_state(data)


class DefaultRedditService:
    """Default Reddit service implementation."""
    
    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize with optional config."""
        self._config = config
        self._client: praw.Reddit | None = None
    
    @beartype  # type: ignore[misc]
    def get_client(self) -> praw.Reddit:
        """Get Reddit client (lazy initialization)."""
        if self._client is None:
            self._client = _init_reddit(self._config)
        return self._client
