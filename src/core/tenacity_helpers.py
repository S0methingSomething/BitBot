"""Tenacity helpers for Result-aware retries with logging."""

from typing import Any

import deal
from beartype import beartype
from tenacity import RetryCallState

from core.error_logger import LogLevel, get_logger
from core.errors import BitBotError, GitHubAPIError, RedditAPIError
from core.result import Err, Result


@deal.pre(lambda result: result is not None, message="Result cannot be None")
@beartype
# Any: Accepts any Result type for generic retry logic
def should_retry_api_error(result: Any) -> bool:
    """Check if Result contains retryable API error."""
    if not isinstance(result, Result):
        return False
    if not result.is_err():
        return False
    # Type narrowing: we know it's Err at this point
    if not isinstance(result, Err):
        return False
    return isinstance(result.error, GitHubAPIError | RedditAPIError)


@beartype
def log_retry_attempt(retry_state: RetryCallState) -> None:
    """Log retry attempts with context."""
    logger = get_logger()
    if retry_state.outcome and retry_state.outcome.failed:
        exception = retry_state.outcome.exception()
        if isinstance(exception, BitBotError):
            logger.log_error(
                exception,
                LogLevel.WARNING,
                {
                    "attempt": retry_state.attempt_number,
                    "wait": retry_state.next_action.sleep if retry_state.next_action else 0,
                },
            )
