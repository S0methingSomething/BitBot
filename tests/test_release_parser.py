"""Tests for unified release parser."""

import pytest

from bitbot.core.release_parser import parse_release_body, parse_release_body_strict


class TestParseReleaseBody:
    """Tests for parse_release_body."""

    def test_parses_all_fields(self):
        """Parse all fields from release body."""
        body = """app: BitLife
version: 3.21
asset_name: MonetizationVars
sha256: abc123def456"""
        parsed = parse_release_body(body)
        assert parsed.app_id == "BitLife"
        assert parsed.version == "3.21"
        assert parsed.asset_name == "MonetizationVars"
        assert parsed.sha256 == "abc123def456"

    def test_parses_partial_fields(self):
        """Parse partial fields."""
        body = "app: BitLife\nversion: 3.21"
        parsed = parse_release_body(body)
        assert parsed.app_id == "BitLife"
        assert parsed.version == "3.21"
        assert parsed.asset_name is None
        assert parsed.sha256 is None

    def test_handles_empty_body(self):
        """Empty body returns all None."""
        parsed = parse_release_body("")
        assert parsed.app_id is None
        assert parsed.version is None

    def test_handles_whitespace(self):
        """Handles whitespace around values."""
        body = "  app:  BitLife  \n  version:  3.21  "
        parsed = parse_release_body(body)
        assert parsed.app_id == "BitLife"
        assert parsed.version == "3.21"

    def test_handles_carriage_returns(self):
        """Handles Windows line endings."""
        body = "app: BitLife\r\nversion: 3.21\r\n"
        parsed = parse_release_body(body)
        assert parsed.app_id == "BitLife"
        assert parsed.version == "3.21"

    def test_ignores_unknown_keys(self):
        """Unknown keys are ignored."""
        body = "app: BitLife\nunknown: value\nversion: 3.21"
        parsed = parse_release_body(body)
        assert parsed.app_id == "BitLife"
        assert parsed.version == "3.21"

    def test_ignores_lines_without_colon(self):
        """Lines without colon are ignored."""
        body = "app: BitLife\nsome random text\nversion: 3.21"
        parsed = parse_release_body(body)
        assert parsed.app_id == "BitLife"
        assert parsed.version == "3.21"

    def test_is_complete_true(self):
        """is_complete returns True when app_id and version present."""
        parsed = parse_release_body("app: BitLife\nversion: 3.21")
        assert parsed.is_complete

    def test_is_complete_false_missing_app(self):
        """is_complete returns False when app_id missing."""
        parsed = parse_release_body("version: 3.21")
        assert not parsed.is_complete

    def test_is_complete_false_missing_version(self):
        """is_complete returns False when version missing."""
        parsed = parse_release_body("app: BitLife")
        assert not parsed.is_complete

    def test_case_insensitive_keys(self):
        """Keys are case-insensitive."""
        body = "APP: BitLife\nVERSION: 3.21\nAsset_Name: Test"
        parsed = parse_release_body(body)
        assert parsed.app_id == "BitLife"
        assert parsed.version == "3.21"
        assert parsed.asset_name == "Test"

    # BitBot-specific scenarios
    def test_real_bitlife_release(self):
        """Test parsing a real BitLife release format."""
        body = """app: bitlife
version: 3.21.1
asset_name: MonetizationVars
sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"""
        parsed = parse_release_body(body)
        assert parsed.app_id == "bitlife"
        assert parsed.version == "3.21.1"
        assert parsed.asset_name == "MonetizationVars"
        assert len(parsed.sha256) == 64  # SHA256 hex length

    def test_real_doglife_release(self):
        """Test parsing a DogLife release format."""
        body = """app: doglife
version: 1.8.0
asset_name: MonetizationVars"""
        parsed = parse_release_body(body)
        assert parsed.app_id == "doglife"
        assert parsed.version == "1.8.0"
        assert parsed.is_complete

    def test_release_with_markdown_noise(self):
        """Test parsing release body with markdown formatting."""
        body = """# Release Notes

app: bitlife
version: 3.21

## Changes
- Fixed bugs
- Added features"""
        parsed = parse_release_body(body)
        assert parsed.app_id == "bitlife"
        assert parsed.version == "3.21"

    def test_release_with_extra_colons_in_value(self):
        """Test value containing colons."""
        body = "app: bitlife\nversion: 3.21\nasset_name: file:name:test"
        parsed = parse_release_body(body)
        # partition splits on first colon, so value keeps remaining colons
        assert parsed.asset_name == "file:name:test"

    def test_semver_versions(self):
        """Test various semver version formats."""
        versions = ["1.0.0", "1.0", "1", "1.0.0-beta", "1.0.0+build123"]
        for ver in versions:
            parsed = parse_release_body(f"app: test\nversion: {ver}")
            assert parsed.version == ver

    def test_empty_value_ignored(self):
        """Test empty values are treated as None."""
        body = "app: bitlife\nversion:\nasset_name: test"
        parsed = parse_release_body(body)
        assert parsed.app_id == "bitlife"
        assert parsed.version is None  # Empty value
        assert parsed.asset_name == "test"

    def test_duplicate_keys_last_wins(self):
        """Test duplicate keys - last value wins."""
        body = "app: first\nversion: 1.0\napp: second"
        parsed = parse_release_body(body)
        assert parsed.app_id == "second"


class TestParseReleaseBodyStrict:
    """Tests for parse_release_body_strict."""

    def test_returns_parsed_when_complete(self):
        """Returns parsed release when complete."""
        body = "app: BitLife\nversion: 3.21"
        parsed = parse_release_body_strict(body)
        assert parsed.app_id == "BitLife"
        assert parsed.version == "3.21"

    def test_raises_when_missing_app(self):
        """Raises ValueError when app missing."""
        with pytest.raises(ValueError, match="app"):
            parse_release_body_strict("version: 3.21")

    def test_raises_when_missing_version(self):
        """Raises ValueError when version missing."""
        with pytest.raises(ValueError, match="version"):
            parse_release_body_strict("app: BitLife")

    def test_raises_when_both_missing(self):
        """Raises ValueError when both missing."""
        with pytest.raises(ValueError, match="app.*version|version.*app"):
            parse_release_body_strict("random text")

    def test_strict_with_optional_fields(self):
        """Strict mode allows missing optional fields."""
        body = "app: bitlife\nversion: 3.21"
        parsed = parse_release_body_strict(body)
        assert parsed.is_complete
        assert parsed.asset_name is None  # Optional, not required
        assert parsed.sha256 is None  # Optional, not required
