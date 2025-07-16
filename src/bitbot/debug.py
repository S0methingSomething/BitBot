"""This module provides debugging utilities for the BitBot application."""

import logging

from .logging import get_logger


def enable_debug_mode() -> None:
    """Enable debug logging for the application."""
    get_logger("bitbot").setLevel(logging.DEBUG)
    logger = get_logger(__name__)
    logger.debug("Debug mode enabled.")
