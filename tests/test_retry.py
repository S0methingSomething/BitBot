"""Tests for retry decorator."""

from returns.result import Failure, Result, Success

from bitbot.core.errors import GitHubAPIError
from bitbot.core.retry import retry_on_err


def test_retry_on_err_success_first_attempt():
    """Test retry_on_err returns Success on first attempt."""
    call_count = 0

    @retry_on_err()
    def succeeds_immediately():
        nonlocal call_count
        call_count += 1
        return Success("success")

    result = succeeds_immediately()

    assert isinstance(result, Success)
    assert result.unwrap() == "success"
    assert call_count == 1


def test_retry_on_err_retries_on_failure():
    """Test retry_on_err retries when function returns Failure."""
    call_count = 0

    @retry_on_err(max_attempts=3)
    def fails_twice_then_succeeds():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            return Failure(GitHubAPIError(f"Attempt {call_count} failed"))
        return Success("success")

    result = fails_twice_then_succeeds()

    assert isinstance(result, Success)
    assert result.unwrap() == "success"
    assert call_count == 3


def test_retry_on_err_returns_final_failure():
    """Test retry_on_err returns final Failure after exhausting retries."""
    call_count = 0

    @retry_on_err(max_attempts=3)
    def always_fails():
        nonlocal call_count
        call_count += 1
        return Failure(GitHubAPIError(f"Attempt {call_count}"))

    result = always_fails()

    assert isinstance(result, Failure)
    assert "Attempt 3" in str(result.failure())
    assert call_count == 3


def test_retry_on_err_preserves_function_signature():
    """Test retry_on_err preserves function name and docstring."""

    @retry_on_err()
    def my_function(x: int, y: str) -> Result[str, GitHubAPIError]:
        """My docstring."""
        return Success(f"{x}-{y}")

    assert my_function.__name__ == "my_function"
    assert my_function.__doc__ == "My docstring."


def test_retry_on_err_with_arguments():
    """Test retry_on_err works with function arguments."""

    @retry_on_err()
    def function_with_args(a: int, b: str, c: bool = False):
        if c:
            return Success(f"{a}-{b}")
        return Failure(GitHubAPIError("Failed"))

    result_err = function_with_args(1, "test")
    assert isinstance(result_err, Failure)

    result_ok = function_with_args(1, "test", c=True)
    assert isinstance(result_ok, Success)
    assert result_ok.unwrap() == "1-test"


def test_retry_on_err_custom_attempts():
    """Test retry_on_err respects custom max_attempts."""
    call_count = 0

    @retry_on_err(max_attempts=5)
    def fails_always():
        nonlocal call_count
        call_count += 1
        return Failure(GitHubAPIError("fail"))

    result = fails_always()

    assert isinstance(result, Failure)
    assert call_count == 5


def test_retry_on_err_no_retry_on_success():
    """Test retry_on_err doesn't retry when function returns Success."""
    call_count = 0

    @retry_on_err(max_attempts=3)
    def succeeds():
        nonlocal call_count
        call_count += 1
        return Success("done")

    result = succeeds()

    assert isinstance(result, Success)
    assert call_count == 1
