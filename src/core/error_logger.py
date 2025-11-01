"""Structured error logger with Rich integration."""

import json
from enum import Enum
from pathlib import Path
from typing import Any

from beartype import beartype
from rich.console import Console

from core.error_context import get_error_context
from core.errors import BitBotError


class LogLevel(Enum):
    """Log levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ErrorLogger:
    """Structured error logger."""

    @beartype  # type: ignore[misc]
    @beartype  # type: ignore[misc]
    def __init__(
        self,
        console: Console | None = None,
        log_file: Path | None = None,
    ) -> None:
        """Initialize logger."""
        self.console = console or Console()
        self.log_file = log_file

    @beartype  # type: ignore[misc]
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

    @beartype  # type: ignore[misc]
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
