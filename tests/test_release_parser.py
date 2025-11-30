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
