"""Structured error logger with Rich integration."""

import json
from enum import Enum
from pathlib import Path
from typing import Any

import deal
from beartype import beartype
from rich.console import Console

from bitbot.core.error_context import get_error_context
from bitbot.core.errors import BitBotError


class LogLevel(Enum):
    """Log levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ErrorLogger:
    """Structured error logger."""

    @beartype
    @beartype
    def __init__(
        self,
        console: Console | None = None,
        log_file: Path | None = None,
    ) -> None:
        """Initialize logger."""
        self.console = console or Console()
        self.log_file = log_file

    @beartype
    def log_error(
        self,
        error: BitBotError,
        level: LogLevel = LogLevel.ERROR,
        extra_context: dict[str, Any] | None = None,
    ) -> None:
        """Log error with context."""
        context = get_error_context()
        if extra_context:
            context.update(extra_context)

        error_dict = error.to_dict()
        error_dict["context"].update(context)
        error_dict["level"] = level.value

        # Console output
        color = self._get_color(level)
        self.console.print(f"[{color}]{level.value}:[/{color}] {error.message}")
        if context:
            self.console.print(f"[dim]Context: {context}[/dim]")

        # File output
        if self.log_file:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
            with self.log_file.open("a") as f:
                f.write(json.dumps(error_dict) + "\n")

    @deal.post(lambda result: len(result) > 0, message="Color string must be non-empty")
    @beartype
    def _get_color(self, level: LogLevel) -> str:
        """Get color for log level."""
        colors = {
            LogLevel.DEBUG: "blue",
            LogLevel.INFO: "green",
            LogLevel.WARNING: "yellow",
            LogLevel.ERROR: "red",
            LogLevel.CRITICAL: "bold red",
        }
        return colors[level]


# Global logger instance
_logger: ErrorLogger | None = None


@beartype
def get_logger(
    console: Console | None = None,
    log_file: Path | None = None,
) -> ErrorLogger:
    """Get or create the global logger instance."""
    global _logger
    if _logger is None:
        default_log_file = Path(".taskmaster/logs/bitbot.log") if log_file is None else log_file
        _logger = ErrorLogger(console=console, log_file=default_log_file)
    return _logger


def reset_logger() -> None:
    """Reset the global logger (for testing)."""
    global _logger
    _logger = None
