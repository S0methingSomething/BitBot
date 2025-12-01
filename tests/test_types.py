"""Tests for BitBot type definitions."""

from bitbot.types import (
    AppReleaseData,
    Changelog,
    LatestRelease,
    ReleaseInfo,
    ReleasesData,
    RemovedReleaseInfo,
    UpdatedReleaseInfo,
)


class TestReleaseInfo:
    """Tests for ReleaseInfo TypedDict."""

    def test_create_release_info(self):
        """Test creating a ReleaseInfo."""
        info: ReleaseInfo = {
            "display_name": "BitLife",
            "version": "1.0.0",
            "url": "https://example.com/download",
        }
        assert info["display_name"] == "BitLife"
        assert info["version"] == "1.0.0"
        assert info["url"] == "https://example.com/download"


class TestUpdatedReleaseInfo:
    """Tests for UpdatedReleaseInfo TypedDict."""

    def test_create_updated_release_info(self):
        """Test creating an UpdatedReleaseInfo."""
        new_info: ReleaseInfo = {
            "display_name": "BitLife",
            "version": "2.0.0",
            "url": "https://example.com/v2",
        }
        updated: UpdatedReleaseInfo = {"new": new_info, "old": "1.0.0"}
        assert updated["new"]["version"] == "2.0.0"
        assert updated["old"] == "1.0.0"


class TestChangelog:
    """Tests for Changelog TypedDict."""

    def test_empty_changelog(self):
        """Test creating an empty changelog."""
        changelog: Changelog = {"added": {}, "updated": {}, "removed": {}}
        assert len(changelog["added"]) == 0
        assert len(changelog["updated"]) == 0
        assert len(changelog["removed"]) == 0

    def test_changelog_with_added(self):
        """Test changelog with added releases."""
        changelog: Changelog = {
            "added": {
                "bitlife": {
                    "display_name": "BitLife",
                    "version": "1.0.0",
                    "url": "https://example.com",
                }
            },
            "updated": {},
            "removed": {},
        }
        assert "bitlife" in changelog["added"]
        assert changelog["added"]["bitlife"]["version"] == "1.0.0"

    def test_changelog_with_updated(self):
        """Test changelog with updated releases."""
        changelog: Changelog = {
            "added": {},
            "updated": {
                "bitlife": {
                    "new": {
                        "display_name": "BitLife",
                        "version": "2.0.0",
                        "url": "https://example.com/v2",
                    },
                    "old": "1.0.0",
                }
            },
            "removed": {},
        }
        assert changelog["updated"]["bitlife"]["old"] == "1.0.0"
        assert changelog["updated"]["bitlife"]["new"]["version"] == "2.0.0"

    def test_changelog_with_removed(self):
        """Test changelog with removed releases."""
        removed: RemovedReleaseInfo = {"display_name": "OldApp", "version": "1.0.0"}
        changelog: Changelog = {
            "added": {},
            "updated": {},
            "removed": {"oldapp": removed},
        }
        assert changelog["removed"]["oldapp"]["display_name"] == "OldApp"


class TestReleasesData:
    """Tests for ReleasesData type alias."""

    def test_releases_data_structure(self):
        """Test the full releases data structure."""
        latest: LatestRelease = {"version": "1.0.0", "download_url": "https://example.com"}
        app_data: AppReleaseData = {
            "display_name": "BitLife",
            "latest_release": latest,
            "previous_releases": [{"version": "0.9.0", "download_url": "https://example.com/old"}],
        }
        data: ReleasesData = {"bitlife": app_data}

        assert data["bitlife"]["display_name"] == "BitLife"
        assert data["bitlife"]["latest_release"]["version"] == "1.0.0"
        assert len(data["bitlife"]["previous_releases"]) == 1
