"""A centralized logging service for the application."""

import functools
from typing import Any, Callable

from rich.console import Console


class LoggingService:
    """Provides a centralized console for logging."""

    def __init__(self) -> None:
        """Initialize the LoggingService."""
        self._console = Console(stderr=True)

    def log(self, message: str, style: str = "info") -> None:
        """Log a message to the console with a specific style.

        Args:
            message: The message to log.
            style: The rich style to apply (e.g., 'info', 'warning', 'error').

        """
        style_map = {
            "info": "green",
            "debug": "blue",
            "warning": "yellow",
            "error": "bold red",
        }
        self._console.log(message, style=style_map.get(style, "default"))

    def info(self, message: str) -> None:
        """Log an informational message."""
        self.log(f"[INFO] {message}", style="info")

    def debug(self, message: str) -> None:
        """Log a debug message."""
        self.log(f"[DEBUG] {message}", style="debug")

    def warning(self, message: str) -> None:
        """Log a warning message."""
        self.log(f"[WARNING] {message}", style="warning")

    def error(self, message: str) -> None:
        """Log an error message."""
        self.log(f"[ERROR] {message}", style="error")

    def trace(self, func: Callable) -> Callable:
        """Decorate a function to log its entry and exit."""

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            self.debug(f"Entering: {func.__name__}...")
            try:
                result = func(*args, **kwargs)
                self.debug(f"Exiting: {func.__name__}")
                return result
            except Exception as e:
                self.error(f"Exception in {func.__name__}: {e}")
                raise

        return wrapper


# A global instance for easy access if needed, though injection is preferred.
logger = LoggingService()
