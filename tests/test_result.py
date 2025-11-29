"""Tests for Result type (using returns library)."""

import pytest
from returns.result import Failure, Success


def test_success_unwrap():
    """Test Success.unwrap() returns value."""
    result = Success(42)
    assert result.unwrap() == 42


def test_success_is_success():
    """Test Success is instance of Success."""
    result = Success("success")
    assert isinstance(result, Success)
    assert not isinstance(result, Failure)


def test_failure_unwrap_raises():
    """Test Failure.unwrap() raises UnwrapFailedError."""
    from returns.primitives.exceptions import UnwrapFailedError

    result = Failure("error message")
    with pytest.raises(UnwrapFailedError):
        result.unwrap()


def test_failure_is_failure():
    """Test Failure is instance of Failure."""
    result = Failure("failure")
    assert isinstance(result, Failure)
    assert not isinstance(result, Success)


def test_success_map():
    """Test Success.map() transforms value."""
    result = Success(5)
    mapped = result.map(lambda x: x * 2)
    assert mapped.unwrap() == 10


def test_failure_map_unchanged():
    """Test Failure.map() returns unchanged Failure."""
    result = Failure("error")
    mapped = result.map(lambda x: x * 2)
    assert isinstance(mapped, Failure)
    assert mapped.failure() == "error"


def test_success_bind():
    """Test Success.bind() chains operations."""
    result = Success(5)
    chained = result.bind(lambda x: Success(x * 2))
    assert chained.unwrap() == 10


def test_failure_bind_unchanged():
    """Test Failure.bind() returns unchanged Failure."""
    result = Failure("error")
    chained = result.bind(lambda x: Success(x * 2))
    assert isinstance(chained, Failure)
    assert chained.failure() == "error"


def test_success_value_or():
    """Test Success.value_or() returns value."""
    result = Success(42)
    assert result.value_or(0) == 42


def test_failure_value_or():
    """Test Failure.value_or() returns default."""
    result = Failure("error")
    assert result.value_or(0) == 0


def test_success_alt_unchanged():
    """Test Success.alt() returns unchanged Success."""
    result = Success(5)
    mapped = result.alt(lambda e: f"transformed: {e}")
    assert isinstance(mapped, Success)
    assert mapped.unwrap() == 5


def test_failure_alt_transforms():
    """Test Failure.alt() transforms error."""
    result = Failure("original")
    mapped = result.alt(lambda e: f"transformed: {e}")
    assert isinstance(mapped, Failure)
    assert mapped.failure() == "transformed: original"


def test_failure_failure():
    """Test Failure.failure() returns error value."""
    result = Failure("my error")
    assert result.failure() == "my error"


def test_bind_chain_to_failure():
    """Test bind can chain to Failure."""
    result = Success(5)
    chained = result.bind(lambda x: Failure("failed") if x > 3 else Success(x))
    assert isinstance(chained, Failure)
    assert chained.failure() == "failed"


def test_multiple_map_chain():
    """Test multiple map operations chain correctly."""
    result = Success(2)
    chained = result.map(lambda x: x * 2).map(lambda x: x + 1).map(lambda x: x * 3)
    assert chained.unwrap() == 15  # ((2*2)+1)*3


def test_map_with_type_change():
    """Test map can change value type."""
    result = Success(42)
    mapped = result.map(str)
    assert mapped.unwrap() == "42"
    assert isinstance(mapped.unwrap(), str)
