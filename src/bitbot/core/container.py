"""Dependency injection container for BitBot."""

from typing import Any, TypeVar

import deal
from beartype import beartype

from bitbot.core.config import load_config
from bitbot.core.errors import BitBotError
from bitbot.core.result import Ok, Result

T = TypeVar("T")


class Container:
    """Simple dependency injection container."""

    def __init__(self) -> None:
        """Initialize container."""
        self._services: dict[str, Any] = {}

    @deal.pre(lambda _self, name, _service: len(name) > 0)
    @deal.pre(lambda _self, _name, service: service is not None)
    @beartype
    # Any: Generic container accepts any service type
    def register(self, name: str, service: Any) -> None:
        """Register a service."""
        self._services[name] = service

    @deal.pre(lambda _self, name, _service_type=None: len(name) > 0)
    @deal.raises(KeyError, TypeError)
    @beartype
    # Any: Returns service of unknown type, caller must cast
    def get(self, name: str, service_type: type[T] | None = None) -> Any | T:
        """Get a service with optional type checking."""
        if name not in self._services:
            msg = f"Service '{name}' not registered"
            raise KeyError(msg)
        service = self._services[name]
        if service_type is not None and not isinstance(service, service_type):
            msg = f"Service '{name}' is not of type {service_type}"
            raise TypeError(msg)
        return service

    @beartype
    def has(self, name: str) -> bool:
        """Check if service is registered."""
        return name in self._services


# Global container instance
_container: Container | None = None


@deal.post(lambda result: result is not None)
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
