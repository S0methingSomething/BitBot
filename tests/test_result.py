"""Tests for Result type."""

import pytest

from bitbot.core.result import Err, Ok


def test_ok_unwrap():
    """Test Ok.unwrap() returns value."""
    result = Ok(42)
    assert result.unwrap() == 42


def test_ok_is_ok():
    """Test Ok.is_ok() returns True."""
    result = Ok("success")
    assert result.is_ok() is True
    assert result.is_err() is False


def test_err_unwrap_raises():
    """Test Err.unwrap() raises RuntimeError."""
    result = Err("error message")
    with pytest.raises(RuntimeError, match="error message"):
        result.unwrap()


def test_err_is_err():
    """Test Err.is_err() returns True."""
    result = Err("failure")
    assert result.is_err() is True
    assert result.is_ok() is False


def test_ok_map():
    """Test Ok.map() transforms value."""
    result = Ok(5)
    mapped = result.map(lambda x: x * 2)
    assert mapped.unwrap() == 10


def test_err_map_unchanged():
    """Test Err.map() returns unchanged Err."""
    result = Err("error")
    mapped = result.map(lambda x: x * 2)
    assert mapped.is_err()
    assert mapped.unwrap_err() == "error"


def test_ok_and_then():
    """Test Ok.and_then() chains operations."""
    result = Ok(5)
    chained = result.and_then(lambda x: Ok(x * 2))
    assert chained.unwrap() == 10


def test_err_and_then_unchanged():
    """Test Err.and_then() returns unchanged Err."""
    result = Err("error")
    chained = result.and_then(lambda x: Ok(x * 2))
    assert chained.is_err()
    assert chained.unwrap_err() == "error"


def test_ok_unwrap_or():
    """Test Ok.unwrap_or() returns value."""
    result = Ok(42)
    assert result.unwrap_or(0) == 42


def test_err_unwrap_or():
    """Test Err.unwrap_or() returns default."""
    result = Err("error")
    assert result.unwrap_or(0) == 0


def test_ok_map_err_unchanged():
    """Test Ok.map_err() returns unchanged Ok."""
    result = Ok(5)
    mapped = result.map_err(lambda e: f"transformed: {e}")
    assert mapped.is_ok()
    assert mapped.unwrap() == 5


def test_err_map_err_transforms():
    """Test Err.map_err() transforms error."""
    result = Err("original")
    mapped = result.map_err(lambda e: f"transformed: {e}")
    assert mapped.is_err()
    assert mapped.unwrap_err() == "transformed: original"


def test_err_unwrap_err():
    """Test Err.unwrap_err() returns error value."""
    result = Err("my error")
    assert result.unwrap_err() == "my error"


def test_and_then_chain_to_err():
    """Test and_then can chain to Err."""
    result = Ok(5)
    chained = result.and_then(lambda x: Err("failed") if x > 3 else Ok(x))
    assert chained.is_err()
    assert chained.unwrap_err() == "failed"


def test_multiple_map_chain():
    """Test multiple map operations chain correctly."""
    result = Ok(2)
    chained = result.map(lambda x: x * 2).map(lambda x: x + 1).map(lambda x: x * 3)
    assert chained.unwrap() == 15  # ((2*2)+1)*3


def test_map_with_type_change():
    """Test map can change value type."""
    result = Ok(42)
    mapped = result.map(str)
    assert mapped.unwrap() == "42"
    assert isinstance(mapped.unwrap(), str)
