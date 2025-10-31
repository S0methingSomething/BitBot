"""Tests for paths module."""

import sys
from pathlib import Path

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import paths


def test_get_template_path():
    """Test template path generation."""
    result = paths.get_template_path("test.html")
    assert "test.html" in result
    assert len(result) > 0


def test_get_template_path_empty_raises():
    """Test empty template name raises error."""
    with pytest.raises(Exception):  # deal.PreContractError
        paths.get_template_path("")


def test_constants_exist():
    """Test all path constants are defined."""
    assert paths.ROOT_DIR
    assert paths.CONFIG_FILE
    assert paths.BOT_STATE_FILE
    assert paths.RELEASE_STATE_FILE
    assert paths.DIST_DIR
    assert paths.TEMPLATES_DIR
