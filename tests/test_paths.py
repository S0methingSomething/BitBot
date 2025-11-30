"""Tests for paths module."""

import pytest

from bitbot import paths


def test_get_template_path():
    """Test template path generation."""
    result = paths.get_template_path("test.html")
    assert "test.html" in str(result)
    assert len(str(result)) > 0


def test_get_template_path_empty_raises():
    """Test empty template name raises error."""
    with pytest.raises(Exception):  # icontract.ViolationError
        paths.get_template_path("")


def test_constants_exist():
    """Test all path constants are defined."""
    assert paths.ROOT_DIR
    assert paths.CONFIG_FILE
    assert paths.DATABASE_FILE
    assert paths.DIST_DIR
    assert paths.TEMPLATES_DIR
