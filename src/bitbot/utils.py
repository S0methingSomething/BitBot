import logging
import sys


def log_and_exit(message: str, error: Exception | None = None) -> None:
    """Logs a critical message and exits the application."""
    if error:
        logging.critical(message, exc_info=True)
    else:
        logging.critical(message)
    sys.exit(1)
