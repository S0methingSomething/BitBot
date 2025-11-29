"""Tests for GitHub release note parsing."""

from bitbot.gh.parser import parse_release_notes


def test_parse_structured_format(config_single_app):
    """Test parsing new structured format."""
    body = "app: bitlife\nversion: 1.2.3\nasset_name: MonetizationVars"

    result = parse_release_notes(body, "v1.2.3", "Release", config_single_app)

    assert result is not None
    assert result["app_id"] == "bitlife"
    assert result["display_name"] == "BitLife"
    assert result["version"] == "1.2.3"
    assert result["asset_name"] == "MonetizationVars"


def test_parse_legacy_tag_format(config_single_app):
    """Test parsing legacy tag format (appid-vX.X.X)."""
    result = parse_release_notes("", "bitlife-v2.0.0", "Some Title", config_single_app)

    assert result is not None
    assert result["app_id"] == "bitlife"
    assert result["version"] == "2.0.0"


def test_parse_title_format(config_single_app):
    """Test parsing from title."""
    result = parse_release_notes("", "some-tag", "BitLife v3.0.0 Release", config_single_app)

    assert result is not None
    assert result["app_id"] == "bitlife"
    assert result["version"] == "3.0.0"


def test_parse_fallback_version_from_tag(config_single_app):
    """Test fallback to extracting version from tag."""
    result = parse_release_notes("", "release-4.5.6", "Unknown", config_single_app)

    assert result is not None
    assert result["version"] == "4.5.6"


def test_parse_no_match_returns_none(config_single_app):
    """Test returns None when no format matches."""
    result = parse_release_notes("random text", "no-version", "No Match", config_single_app)

    assert result is None


def test_parse_with_multiple_apps(config):
    """Test parsing with multiple configured apps."""
    body = "app: doglife\nversion: 2.0.0\nasset_name: Asset"

    result = parse_release_notes(body, "v2.0.0", "Release", config)

    assert result is not None
    assert result["app_id"] == "doglife"
    assert result["display_name"] == "DogLife"
