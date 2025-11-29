"""Retry decorator for Result-returning functions."""

import functools
import logging
from collections.abc import Callable
from typing import ParamSpec, TypeVar

from beartype import beartype
from returns.result import Failure
from tenacity import retry, retry_if_result, stop_after_attempt, wait_exponential

P = ParamSpec("P")
R = TypeVar("R")


@beartype
def retry_on_err(
    max_attempts: int = 3, min_wait: int = 1, max_wait: int = 10
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Retry decorator for functions returning Result types.

    Retries when function returns Failure, stops after max_attempts.
    Returns the final Failure if all attempts fail instead of raising RetryError.

    Args:
        max_attempts: Maximum number of retry attempts (default: 3)
        min_wait: Minimum wait time in seconds (default: 1)
        max_wait: Maximum wait time in seconds (default: 10)

    Returns:
        Decorated function that retries on Failure results
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        """Decorator that adds retry logic to a function.

        Args:
            func: Function to decorate

        Returns:
            Decorated function with retry logic
        """
        logger = logging.getLogger(func.__module__)

        @retry(
            retry=retry_if_result(lambda r: isinstance(r, Failure)),
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(multiplier=1, min=min_wait, max=max_wait),
            retry_error_callback=lambda retry_state: retry_state.outcome.result()  # type: ignore[union-attr]
            if retry_state.outcome
            else None,
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
            """Wrapper function that executes the decorated function.

            Returns:
                Result from the decorated function
            """
            return func(*args, **kwargs)

        return wrapper

    return decorator
