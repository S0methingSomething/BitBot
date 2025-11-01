"""Retry decorator with exponential backoff."""

import time
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from beartype import beartype

from core.errors import BitBotError

T = TypeVar("T")


@beartype  # type: ignore[misc]
def retry(
    max_attempts: int = 3,
    backoff: str = "exponential",
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    on: list[type[BitBotError]] | None = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Retry decorator with configurable backoff strategy."""
    retry_on = on or [BitBotError]

    @beartype  # type: ignore[misc]
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        @beartype  # type: ignore[misc]
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception: Exception | None = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if not any(isinstance(e, error_type) for error_type in retry_on):
                        raise

                    last_exception = e

                    if attempt < max_attempts - 1:
                        if backoff == "exponential":
                            delay = min(base_delay * (2**attempt), max_delay)
                        else:  # linear
                            delay = min(base_delay * (attempt + 1), max_delay)

                        time.sleep(delay)

            if last_exception:
                raise last_exception
            msg = "Retry failed without exception"
            raise RuntimeError(msg)

        return wrapper

    return decorator
