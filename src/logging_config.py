"""Unified logging configuration with rich support."""

import logging
import os
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme

# Custom theme for consistent styling
CUSTOM_THEME = Theme(
    {
        "info": "bold cyan",
        "warning": "bold yellow",
        "error": "bold red",
        "success": "bold green",
        "debug": "bold blue",
    }
)

# Global console instance
console = Console(theme=CUSTOM_THEME)


def get_logger(name: str) -> logging.Logger:
    """
    Sets up and returns a logger instance with rich formatting.

    Args:
        name: Logger name

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Prevent adding multiple handlers if logger already exists
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # Create rich handler with custom formatting
    rich_handler = logging.StreamHandler()
    rich_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(rich_handler)

    # Also add a file handler for persistent logging
    if log_file := os.environ.get("BITBOT_LOG_FILE"):
        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


def print_rich(message: str, style: str = "info", **kwargs: Any) -> None:
    """
    Print a message using rich console directly.

    Args:
        message: Message to print
        style: Style to use (info, warning, error, success, debug)
        **kwargs: Additional arguments to pass to console.print()
    """
    console.print(message, style=style, **kwargs)


def print_panel(
    message: str, title: str = "", style: str = "info", **kwargs: Any
) -> None:
    """
    Print a message in a panel using rich.

    Args:
        message: Message to print
        title: Panel title
        style: Style to use
        **kwargs: Additional arguments to pass to console.print()
    """
    panel = Panel(message, title=title, style=style)
    console.print(panel, **kwargs)


def print_table(data: list[dict[str, Any]], title: str = "", **kwargs: Any) -> None:
    """
    Print tabular data using rich.

    Args:
        data: List of dictionaries representing rows
        title: Table title
        **kwargs: Additional arguments to pass to console.print()
    """
    if not data:
        print_rich("No data to display", "warning")
        return

    table = Table(title=title, show_header=True, header_style="bold magenta")

    # Add columns based on keys in first row
    for key in data[0]:
        table.add_column(str(key), style="dim" if key.lower() in ["id", "time"] else "")

    # Add rows
    for row in data:
        table.add_row(*[str(v) for v in row.values()])

    console.print(table, **kwargs)
