"""Dependency injection container for BitBot."""

from typing import Any

from beartype import beartype

from bitbot.core.config import load_config
from bitbot.core.errors import BitBotError
from bitbot.core.result import Ok, Result


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


@beartype
def setup_container() -> Result[Container, BitBotError]:
    """Initialize container with all services."""
    container = get_container()

    # Load and register config
    config_result = load_config()
    if config_result.is_err():
        return config_result.map_err(lambda e: e)  # type: ignore[return-value]

    container.register("config", config_result.unwrap())

    return Ok(container)
