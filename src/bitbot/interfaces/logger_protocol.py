"""Protocol for the logging service."""

from typing import Protocol, TypeVar

T = TypeVar("T")


class LoggerProtocol(Protocol):
    """A protocol for a logging object."""

    def info(self, msg: str, *args: T, **kwargs: T) -> None:
        """Logs a message with the INFO level."""
        ...

    def warning(self, msg: str, *args: T, **kwargs: T) -> None:
        """Logs a message with the WARNING level."""
        ...

    def error(self, msg: str, *args: T, **kwargs: T) -> None:
        """Logs a message with the ERROR level."""
        ...

    def debug(self, msg: str, *args: T, **kwargs: T) -> None:
        """Logs a message with the DEBUG level."""
        ...
