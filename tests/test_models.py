"""Tests for Pydantic models."""

import pytest
from pydantic import ValidationError

from bitbot.models import App, ParsedRelease


def test_app_validation():
    """Test App model validation."""
    app = App(id="test_app", displayName="Test App")
    assert app.id == "test_app"
    assert app.display_name == "Test App"


def test_app_identifiers():
    """Test App identifiers property."""
    app = App(id="TestApp", displayName="Test Application")
    ids = app.identifiers
    assert "TestApp" in ids
    assert "testapp" in ids
    assert "Test Application" in ids
    assert "test application" in ids


def test_app_rejects_empty_id():
    """Test App rejects empty id."""
    with pytest.raises(ValidationError):
        App(id="", displayName="Test")


def test_app_rejects_empty_display_name():
    """Test App rejects empty display_name."""
    with pytest.raises(ValidationError):
        App(id="test", displayName="")


def test_parsed_release_complete():
    """Test ParsedRelease is_complete property."""
    release = ParsedRelease(app_id="test", version="1.0.0")
    assert release.is_complete is True


def test_parsed_release_incomplete():
    """Test ParsedRelease is_complete when missing fields."""
    release = ParsedRelease(app_id="test")
    assert release.is_complete is False

    release = ParsedRelease(version="1.0.0")
    assert release.is_complete is False

    release = ParsedRelease()
    assert release.is_complete is False


def test_parsed_release_optional_fields():
    """Test ParsedRelease optional fields."""
    release = ParsedRelease(app_id="test", version="1.0.0", asset_name="file.apk", sha256="abc123")
    assert release.asset_name == "file.apk"
    assert release.sha256 == "abc123"
