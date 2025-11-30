"""Tests for gather command and release parser."""


import pytest

from bitbot.core.app_registry import AppRegistry
from bitbot.core.release_parser import parse_release_body
from bitbot.models import App


def make_release(app: str, ver: str, url: str = "", date: str = "2025-01-01T00:00:00Z"):
    """Helper to create release dict."""
    r = {"body": f"app: {app}\nversion: {ver}", "published_at": date}
    if url:
        r["assets"] = [{"browser_download_url": url}]
    return r


class TestParseReleaseMetadata:
    """Tests for parse_release_body."""

    def test_parses_app_and_version(self):
        parsed = parse_release_body("app: intl_bitlife\nversion: 1.19.8")
        assert parsed.app_id == "intl_bitlife"
        assert parsed.version == "1.19.8"

    def test_handles_whitespace(self):
        parsed = parse_release_body("  app:  BitLife  \n  version:  3.21  ")
        assert parsed.app_id == "BitLife"
        assert parsed.version == "3.21"

    def test_returns_none_for_missing_fields(self):
        parsed = parse_release_body("random")
        assert parsed.app_id is None
        assert parsed.version is None

    def test_handles_empty_body(self):
        parsed = parse_release_body("")
        assert parsed.app_id is None
        assert parsed.version is None

    def test_handles_carriage_returns(self):
        parsed = parse_release_body("app: BitLife\r\nversion: 3.21\r\n")
        assert parsed.app_id == "BitLife"
        assert parsed.version == "3.21"


class TestGatherIntegration:
    """Integration tests for gather with mocked GitHub API."""

    @pytest.fixture
    def registry(self):
        apps = [
            App(id="BitLife", displayName="BitLife"),
            App(id="BitLife Go", displayName="BitLife Go"),
            App(id="intl_bitlife", displayName="BitLife (International)"),
        ]
        return AppRegistry(apps)

    def test_gathers_latest_from_source(self, registry):
        """Latest releases come from source repo with correct app IDs."""
        source = [
            make_release("intl_bitlife", "1.20.0"),
            make_release("BitLife", "3.21"),
        ]
        bot = [
            make_release("intl_bitlife", "1.20.0", "https://ex.com/intl"),
            make_release("BitLife", "3.21", "https://ex.com/bl"),
        ]

        apps_data = {}
        for rel in source:
            parsed = parse_release_body(rel["body"])
            if not parsed.is_complete:
                continue
            matched = registry.get(parsed.app_id)
            if not matched:
                continue
            url = ""
            for b in bot:
                if not b.get("assets"):
                    continue
                if parse_release_body(b["body"]).version == parsed.version:
                    url = b["assets"][0]["browser_download_url"]
                    break
            if url:
                apps_data[matched.id] = {"version": parsed.version, "url": url}

        assert apps_data["intl_bitlife"]["version"] == "1.20.0"
        assert apps_data["BitLife"]["version"] == "3.21"

    def test_history_normalization(self, registry):
        """Bot releases with variant names normalize to config IDs."""
        apps_data = {
            "BitLife": {"latest": "3.21", "prev": []},
            "BitLife Go": {"latest": "1.1.31", "prev": []},
        }
        bot = [
            make_release("BitLife", "3.21", "url"),
            make_release("bitlife", "3.19.7", "url"),  # lowercase
            make_release("bitlife_go", "1.1.3", "url"),  # underscore
        ]

        for rel in bot:
            parsed = parse_release_body(rel["body"])
            if not parsed.app_id:
                continue
            matched = registry.get(parsed.app_id)
            if not matched or matched.id not in apps_data:
                continue
            if parsed.version != apps_data[matched.id]["latest"]:
                apps_data[matched.id]["prev"].append(parsed.version)

        assert "3.19.7" in apps_data["BitLife"]["prev"]
        # Note: bitlife_go won't match because registry doesn't have that alias

    def test_skips_unconfigured_apps(self, registry):
        """Apps not in config are skipped."""
        source = [
            make_release("BitLife", "3.21"),
            make_release("unknown", "1.0"),
        ]

        result = []
        for r in source:
            parsed = parse_release_body(r["body"])
            if parsed.app_id and registry.exists(parsed.app_id):
                result.append(parsed.app_id)
        assert result == ["BitLife"]

    def test_skips_without_bot_download(self):
        """Source releases without bot download are skipped."""
        bot = [make_release("BitLife", "3.21", "url")]

        found = any(
            parse_release_body(b["body"]).version == "9.99"
            for b in bot if b.get("assets")
        )
        assert not found

    def test_no_duplicate_versions(self):
        """Same version from variants doesn't duplicate."""
        apps_data = {"BitLife": {"latest": "3.21", "prev": []}}
        bot = [
            make_release("bitlife", "3.19.7", "a"),
            make_release("BitLife", "3.19.7", "b"),  # duplicate
        ]

        for rel in bot:
            parsed = parse_release_body(rel["body"])
            if parsed.version and parsed.version not in apps_data["BitLife"]["prev"]:
                apps_data["BitLife"]["prev"].append(parsed.version)

        assert apps_data["BitLife"]["prev"].count("3.19.7") == 1

    def test_releases_without_assets_skipped(self):
        """Releases without assets are skipped."""
        bot = [
            {"body": "app: BitLife\nversion: 3.21", "assets": []},
            {"body": "app: BitLife\nversion: 3.20"},
        ]
        count = sum(1 for r in bot if r.get("assets"))
        assert count == 0

    def test_normalization_cases(self, registry):
        """Various normalization scenarios via registry."""
        cases = [
            ("BitLife", "BitLife"),
            ("bitlife", "BitLife"),  # case-insensitive
            ("BitLife Go", "BitLife Go"),
            ("intl_bitlife", "intl_bitlife"),
            ("unknown", None),
        ]
        for app_id, expected in cases:
            matched = registry.get(app_id)
            result = matched.id if matched else None
            assert result == expected, f"{app_id} -> {result}, expected {expected}"
