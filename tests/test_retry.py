"""Tests for retry decorator."""

from unittest.mock import MagicMock

from bitbot.core.errors import GitHubAPIError
from bitbot.core.result import Err, Ok
from bitbot.core.retry import retry_on_err


def test_retry_on_err_success_first_attempt():
    """Test retry_on_err returns Ok on first attempt."""
    call_count = 0
    
    @retry_on_err()
    def succeeds_immediately():
        nonlocal call_count
        call_count += 1
        return Ok("success")
    
    result = succeeds_immediately()
    
    assert result.is_ok()
    assert result.unwrap() == "success"
    assert call_count == 1


def test_retry_on_err_retries_on_err():
    """Test retry_on_err retries when function returns Err."""
    call_count = 0
    
    @retry_on_err(max_attempts=3)
    def fails_twice_then_succeeds():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            return Err(GitHubAPIError(f"Attempt {call_count} failed"))
        return Ok("success")
    
    result = fails_twice_then_succeeds()
    
    assert result.is_ok()
    assert result.unwrap() == "success"
    assert call_count == 3


def test_retry_on_err_returns_final_err():
    """Test retry_on_err returns final Err after exhausting retries."""
    call_count = 0
    
    @retry_on_err(max_attempts=3)
    def always_fails():
        nonlocal call_count
        call_count += 1
        return Err(GitHubAPIError(f"Attempt {call_count}"))
    
    result = always_fails()
    
    assert result.is_err()
    assert "Attempt 3" in str(result.unwrap_err())
    assert call_count == 3


def test_retry_on_err_preserves_function_signature():
    """Test retry_on_err preserves function name and docstring."""
    @retry_on_err()
    def my_function(x: int, y: str) -> Ok[str] | Err[GitHubAPIError]:
        """My docstring."""
        return Ok(f"{x}-{y}")
    
    assert my_function.__name__ == "my_function"
    assert my_function.__doc__ == "My docstring."


def test_retry_on_err_with_arguments():
    """Test retry_on_err works with function arguments."""
    @retry_on_err()
    def function_with_args(a: int, b: str, c: bool = False):
        if c:
            return Ok(f"{a}-{b}")
        return Err(GitHubAPIError("Failed"))
    
    result_err = function_with_args(1, "test")
    assert result_err.is_err()
    
    result_ok = function_with_args(1, "test", c=True)
    assert result_ok.is_ok()
    assert result_ok.unwrap() == "1-test"


def test_retry_on_err_custom_attempts():
    """Test retry_on_err respects custom max_attempts."""
    call_count = 0
    
    @retry_on_err(max_attempts=5)
    def fails_always():
        nonlocal call_count
        call_count += 1
        return Err(GitHubAPIError("fail"))
    
    result = fails_always()
    
    assert result.is_err()
    assert call_count == 5


def test_retry_on_err_no_retry_on_ok():
    """Test retry_on_err doesn't retry when function returns Ok."""
    call_count = 0
    
    @retry_on_err(max_attempts=3)
    def succeeds():
        nonlocal call_count
        call_count += 1
        return Ok("done")
    
    result = succeeds()
    
    assert result.is_ok()
    assert call_count == 1
