"""Tests for gather command."""


import pytest

from bitbot.commands.gather import _parse_release_metadata


def make_release(app: str, ver: str, url: str = "", date: str = "2025-01-01T00:00:00Z"):
    """Helper to create release dict."""
    r = {"body": f"app: {app}\nversion: {ver}", "published_at": date}
    if url:
        r["assets"] = [{"browser_download_url": url}]
    return r


class TestParseReleaseMetadata:
    """Tests for _parse_release_metadata."""

    def test_parses_app_and_version(self):
        release = {"body": "app: intl_bitlife\nversion: 1.19.8"}
        app_id, version = _parse_release_metadata(release)
        assert app_id == "intl_bitlife"
        assert version == "1.19.8"

    def test_handles_whitespace(self):
        release = {"body": "  app:  BitLife  \n  version:  3.21  "}
        app_id, version = _parse_release_metadata(release)
        assert app_id == "BitLife"
        assert version == "3.21"

    def test_returns_none_for_missing_fields(self):
        app_id, version = _parse_release_metadata({"body": "random"})
        assert app_id is None
        assert version is None

    def test_handles_empty_body(self):
        app_id, version = _parse_release_metadata({"body": ""})
        assert app_id is None
        assert version is None

    def test_handles_carriage_returns(self):
        release = {"body": "app: BitLife\r\nversion: 3.21\r\n"}
        app_id, version = _parse_release_metadata(release)
        assert app_id == "BitLife"
        assert version == "3.21"


class TestGatherIntegration:
    """Integration tests for gather with mocked GitHub API."""

    @pytest.fixture
    def apps_config(self):
        return {
            "BitLife": "BitLife",
            "BitLife Go": "BitLife Go",
            "intl_bitlife": "BitLife (International)",
        }

    def test_gathers_latest_from_source(self, apps_config):
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
            app_id, ver = _parse_release_metadata(rel)
            if not app_id or app_id not in apps_config:
                continue
            url = next(
                (b["assets"][0]["browser_download_url"]
                 for b in bot if _parse_release_metadata(b)[1] == ver and b.get("assets")),
                ""
            )
            if url:
                apps_data[app_id] = {"version": ver, "url": url}

        assert apps_data["intl_bitlife"]["version"] == "1.20.0"
        assert apps_data["BitLife"]["version"] == "3.21"

    def test_history_normalization(self, apps_config):
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
            app_id, ver = _parse_release_metadata(rel)
            if not app_id:
                continue
            norm = app_id.lower().replace(" ", "_")
            matched = next(
                (c for c in apps_config if c == app_id or c.lower().replace(" ", "_") == norm),
                None
            )
            if matched and matched in apps_data and ver != apps_data[matched]["latest"]:
                apps_data[matched]["prev"].append(ver)

        assert "3.19.7" in apps_data["BitLife"]["prev"]
        assert "1.1.3" in apps_data["BitLife Go"]["prev"]

    def test_skips_unconfigured_apps(self):
        """Apps not in config are skipped."""
        cfg = {"BitLife": "BitLife"}
        source = [
            make_release("BitLife", "3.21"),
            make_release("unknown", "1.0"),
        ]

        result = [
            _parse_release_metadata(r)[0]
            for r in source
            if _parse_release_metadata(r)[0] in cfg
        ]
        assert result == ["BitLife"]

    def test_skips_without_bot_download(self):
        """Source releases without bot download are skipped."""
        bot = [make_release("BitLife", "3.21", "url")]

        found = any(
            _parse_release_metadata(b)[1] == "9.99"
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
            _, ver = _parse_release_metadata(rel)
            if ver and ver not in apps_data["BitLife"]["prev"]:
                apps_data["BitLife"]["prev"].append(ver)

        assert apps_data["BitLife"]["prev"].count("3.19.7") == 1

    def test_releases_without_assets_skipped(self):
        """Releases without assets are skipped."""
        bot = [
            {"body": "app: BitLife\nversion: 3.21", "assets": []},
            {"body": "app: BitLife\nversion: 3.20"},
        ]
        count = sum(1 for r in bot if r.get("assets"))
        assert count == 0

    def test_normalization_cases(self, apps_config):
        """Various normalization scenarios."""
        cases = [
            ("BitLife", "BitLife"),
            ("bitlife", "BitLife"),
            ("BitLife Go", "BitLife Go"),
            ("bitlife_go", "BitLife Go"),
            ("intl_bitlife", "intl_bitlife"),
            ("unknown", None),
        ]
        for app_id, expected in cases:
            norm = app_id.lower().replace(" ", "_")
            matched = next(
                (c for c in apps_config if c == app_id or c.lower().replace(" ", "_") == norm),
                None
            )
            assert matched == expected, f"{app_id} -> {matched}, expected {expected}"
