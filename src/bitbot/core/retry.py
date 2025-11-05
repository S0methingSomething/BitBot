"""Retry decorator for Result-returning functions."""

import functools
import logging
from collections.abc import Callable
from typing import ParamSpec, TypeVar

from tenacity import retry, retry_if_result, stop_after_attempt, wait_exponential

P = ParamSpec("P")
R = TypeVar("R")


def retry_on_err(
    max_attempts: int = 3, min_wait: int = 1, max_wait: int = 10
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Retry decorator for functions returning Result types.

    Retries when function returns Err, stops after max_attempts.
    Returns the final Err if all attempts fail instead of raising RetryError.

    Args:
        max_attempts: Maximum number of retry attempts (default: 3)
        min_wait: Minimum wait time in seconds (default: 1)
        max_wait: Maximum wait time in seconds (default: 10)
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        logger = logging.getLogger(func.__module__)

        @retry(
            retry=retry_if_result(lambda r: r.is_err()),
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(multiplier=1, min=min_wait, max=max_wait),
            retry_error_callback=lambda retry_state: retry_state.outcome.result(),
            before_sleep=lambda retry_state: logger.warning(
                "Retry %d/%d for %s after error (wait %.1fs)",
                retry_state.attempt_number,
                max_attempts,
                func.__name__,
                retry_state.next_action.sleep if retry_state.next_action else 0,
            ),
        )
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            return func(*args, **kwargs)

        return wrapper

    return decorator
