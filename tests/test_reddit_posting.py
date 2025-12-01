"""Tests for Reddit posting modules."""

from bitbot.reddit.posting.changelog import generate_changelog
from bitbot.reddit.posting.poster import count_outbound_links
from bitbot.reddit.posting.title_generator import create_app_list, generate_dynamic_title


# count_outbound_links tests
class TestCountOutboundLinks:
    """Tests for link counting."""

    def test_no_links(self):
        """Test counting links in text with no links."""
        assert count_outbound_links("No links here") == 0

    def test_single_https(self):
        """Test counting single HTTPS link."""
        assert count_outbound_links("Check https://example.com") == 1

    def test_single_http(self):
        """Test counting single HTTP link."""
        assert count_outbound_links("Check http://example.com") == 1

    def test_multiple_links(self):
        """Test counting multiple links."""
        text = "Visit https://a.com and https://b.com or http://c.com"
        assert count_outbound_links(text) == 3

    def test_duplicates_counted_once(self):
        """Test duplicate links counted once."""
        text = "https://example.com and https://example.com again"
        assert count_outbound_links(text) == 1

    def test_github_release_links(self):
        """Test GitHub release download links."""
        text = """
        Download: https://github.com/owner/repo/releases/download/v1.0/asset.zip
        Also: https://github.com/owner/repo/releases/tag/v1.0
        """
        assert count_outbound_links(text) == 2

    def test_reddit_markdown_links(self):
        """Test Reddit markdown formatted links."""
        text = "[Download](https://example.com/file.zip) and [Info](https://docs.example.com)"
        assert count_outbound_links(text) == 2

    def test_links_with_query_params(self):
        """Test links with query parameters."""
        text = "https://example.com/download?version=1.0&platform=ios"
        assert count_outbound_links(text) == 1


# create_app_list tests
class TestCreateAppList:
    """Tests for app list creation."""

    def test_single_app(self):
        """Test creating app list with single app."""
        apps = {"bitlife": {"display_name": "BitLife", "version": "3.21.0", "url": "http://x.com"}}
        result = create_app_list(apps)
        assert result == "BitLife v3.21.0"

    def test_multiple_apps(self):
        """Test creating app list with multiple apps."""
        apps = {
            "bitlife": {"display_name": "BitLife", "version": "3.21.0", "url": "http://x.com"},
            "doglife": {"display_name": "DogLife", "version": "1.8.0", "url": "http://x.com"},
        }
        result = create_app_list(apps)
        assert "BitLife v3.21.0" in result
        assert "DogLife v1.8.0" in result
        assert ", " in result  # Comma separated

    def test_updated_app_nested_structure(self):
        """Test creating app list with nested 'new' structure for updates."""
        apps = {
            "bitlife": {
                "new": {"display_name": "BitLife", "version": "3.22.0", "url": "http://x.com"},
                "old": "3.21.0",
            }
        }
        result = create_app_list(apps)
        assert result == "BitLife v3.22.0"

    def test_empty_dict(self):
        """Test empty app dict."""
        result = create_app_list({})
        assert result == ""


# generate_dynamic_title tests
class TestGenerateDynamicTitle:
    """Tests for dynamic title generation."""

    def test_added_only_single(self, config):
        """Test title for single added app."""
        added = {"bitlife": {"display_name": "BitLife", "version": "3.21.0", "url": "http://x.com"}}
        result = generate_dynamic_title(config, added, {})
        assert "[BitBot]" in result
        assert "BitLife v3.21.0" in result

    def test_added_only_multiple(self, config):
        """Test title for multiple added apps."""
        added = {
            "bitlife": {"display_name": "BitLife", "version": "3.21.0", "url": "http://x.com"},
            "doglife": {"display_name": "DogLife", "version": "1.8.0", "url": "http://x.com"},
        }
        result = generate_dynamic_title(config, added, {})
        assert "[BitBot]" in result

    def test_updated_single(self, config):
        """Test title for single update."""
        updated = {
            "bitlife": {
                "new": {"display_name": "BitLife", "version": "3.22.0", "url": "http://x.com"},
                "old": "3.21.0",
            }
        }
        result = generate_dynamic_title(config, {}, updated)
        assert "Update" in result

    def test_updated_multiple(self, config):
        """Test title for multiple updates."""
        updated = {
            "bitlife": {
                "new": {"display_name": "BitLife", "version": "3.22.0", "url": "http://x.com"},
                "old": "3.21.0",
            },
            "doglife": {
                "new": {"display_name": "DogLife", "version": "1.9.0", "url": "http://x.com"},
                "old": "1.8.0",
            },
        }
        result = generate_dynamic_title(config, {}, updated)
        assert "[BitBot]" in result

    def test_mixed_added_and_updated(self, config):
        """Test title with both added and updated apps."""
        added = {"catlife": {"display_name": "CatLife", "version": "1.0.0", "url": "http://x.com"}}
        updated = {
            "bitlife": {
                "new": {"display_name": "BitLife", "version": "3.22.0", "url": "http://x.com"},
                "old": "3.21.0",
            }
        }
        result = generate_dynamic_title(config, added, updated)
        assert "[BitBot]" in result

    def test_generic_fallback_many_changes(self, config):
        """Test title falls back to generic for many changes."""
        added = {
            f"app{i}": {"display_name": f"App{i}", "version": "1.0", "url": "http://x.com"}
            for i in range(5)
        }
        result = generate_dynamic_title(config, added, {})
        assert "[BitBot]" in result

    def test_no_changes(self, config):
        """Test title with no changes uses generic."""
        result = generate_dynamic_title(config, {}, {})
        assert "[BitBot]" in result


# generate_changelog tests
class TestGenerateChangelog:
    """Tests for changelog generation."""

    def test_added_single_app(self, config):
        """Test changelog with single added app."""
        added = {
            "bitlife": {
                "display_name": "BitLife",
                "version": "3.21.0",
                "url": "http://example.com/dl",
            }
        }
        result = generate_changelog(config, added=added, updated={}, removed={})
        assert "### Added" in result
        assert "BitLife" in result
        assert "v3.21.0" in result

    def test_added_multiple_apps(self, config):
        """Test changelog with multiple added apps."""
        added = {
            "bitlife": {"display_name": "BitLife", "version": "3.21.0", "url": "http://x.com"},
            "doglife": {"display_name": "DogLife", "version": "1.8.0", "url": "http://x.com"},
        }
        result = generate_changelog(config, added=added, updated={}, removed={})
        assert "BitLife" in result
        assert "DogLife" in result

    def test_updated_shows_version_change(self, config):
        """Test changelog shows updated app with new version."""
        updated = {
            "bitlife": {
                "new": {"display_name": "BitLife", "version": "3.22.0", "url": "http://x.com"},
                "old": "3.21.0",
            }
        }
        result = generate_changelog(config, added={}, updated=updated, removed={})
        assert "### Updated" in result
        assert "BitLife" in result
        assert "3.22.0" in result  # New version shown

    def test_removed_app(self, config):
        """Test changelog with removed app."""
        removed = {"oldapp": {"display_name": "Old App", "version": "1.0.0"}}
        result = generate_changelog(config, added={}, updated={}, removed=removed)
        assert "### Removed" in result
        assert "Old App" in result

    def test_all_change_types(self, config):
        """Test changelog with all change types."""
        added = {"newapp": {"display_name": "New App", "version": "1.0.0", "url": "http://x.com"}}
        updated = {
            "bitlife": {
                "new": {"display_name": "BitLife", "version": "3.22.0", "url": "http://x.com"},
                "old": "3.21.0",
            }
        }
        removed = {"oldapp": {"display_name": "Old App", "version": "0.9.0"}}

        result = generate_changelog(config, added=added, updated=updated, removed=removed)

        assert "### Added" in result
        assert "### Updated" in result
        assert "### Removed" in result

    def test_empty_changelog(self, config):
        """Test changelog with no changes."""
        result = generate_changelog(config, added={}, updated={}, removed={})
        assert "No new updates" in result

    def test_changelog_sections_order(self, config):
        """Test changelog sections appear in correct order."""
        added = {"a": {"display_name": "A", "version": "1.0", "url": "http://x.com"}}
        updated = {
            "b": {
                "new": {"display_name": "B", "version": "2.0", "url": "http://x.com"},
                "old": "1.0",
            }
        }
        removed = {"c": {"display_name": "C", "version": "1.0"}}

        result = generate_changelog(config, added=added, updated=updated, removed=removed)

        added_pos = result.find("### Added")
        updated_pos = result.find("### Updated")
        removed_pos = result.find("### Removed")

        assert added_pos < updated_pos < removed_pos
