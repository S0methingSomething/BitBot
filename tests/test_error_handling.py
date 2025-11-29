"""Tests for error handling modules."""

from io import StringIO

from rich.console import Console

from bitbot.core.error_context import error_context, get_error_context
from bitbot.core.error_logger import ErrorLogger, LogLevel
from bitbot.core.errors import BitBotError, ConfigurationError, GitHubAPIError, RedditAPIError


# error_context tests
def test_error_context_empty():
    """Test get_error_context returns empty dict when no context."""
    ctx = get_error_context()
    assert ctx == {}


def test_error_context_single():
    """Test single error context."""
    with error_context(operation="test", value=123):
        ctx = get_error_context()
        assert ctx["operation"] == "test"
        assert ctx["value"] == 123


def test_error_context_nested():
    """Test nested error contexts merge."""
    with error_context(outer="a"), error_context(inner="b"):
        ctx = get_error_context()
        assert ctx["outer"] == "a"
        assert ctx["inner"] == "b"


def test_error_context_cleanup():
    """Test context is cleaned up after exit."""
    with error_context(temp="value"):
        pass
    ctx = get_error_context()
    assert "temp" not in ctx


# BitBotError tests
def test_bitbot_error_basic():
    """Test BitBotError creation."""
    error = BitBotError("Test error")
    assert error.message == "Test error"
    assert error.context == {}
    assert error.timestamp is not None


def test_bitbot_error_with_context():
    """Test BitBotError with context."""
    error = BitBotError("Error", context={"key": "value"})
    assert error.context["key"] == "value"


def test_bitbot_error_to_dict():
    """Test BitBotError serialization."""
    error = BitBotError("Test", context={"a": 1})
    d = error.to_dict()
    assert d["type"] == "BitBotError"
    assert d["message"] == "Test"
    assert d["context"]["a"] == 1
    assert "timestamp" in d


def test_bitbot_error_str():
    """Test BitBotError string representation."""
    error = BitBotError("Test error", context={"key": "val"})
    s = str(error)
    assert "BitBotError" in s
    assert "Test error" in s


def test_error_subclasses():
    """Test error subclasses."""
    assert issubclass(ConfigurationError, BitBotError)
    assert issubclass(GitHubAPIError, BitBotError)
    assert issubclass(RedditAPIError, BitBotError)


# ErrorLogger tests
def test_error_logger_logs_to_console():
    """Test ErrorLogger outputs to console."""
    output = StringIO()
    console = Console(file=output, force_terminal=True)
    logger = ErrorLogger(console=console)

    error = BitBotError("Test error message")
    logger.log_error(error)

    output_text = output.getvalue()
    assert "Test error message" in output_text


def test_error_logger_levels():
    """Test ErrorLogger handles different levels."""
    output = StringIO()
    console = Console(file=output, force_terminal=True)
    logger = ErrorLogger(console=console)

    levels = [LogLevel.DEBUG, LogLevel.INFO, LogLevel.WARNING, LogLevel.ERROR, LogLevel.CRITICAL]
    for level in levels:
        error = BitBotError(f"Error at {level.value}")
        logger.log_error(error, level=level)

    output_text = output.getvalue()
    assert "ERROR" in output_text or "error" in output_text.lower()


def test_error_logger_with_extra_context():
    """Test ErrorLogger with extra context."""
    output = StringIO()
    console = Console(file=output, force_terminal=True)
    logger = ErrorLogger(console=console)

    error = BitBotError("Error")
    logger.log_error(error, extra_context={"extra": "data"})

    # Should not raise
    assert True
