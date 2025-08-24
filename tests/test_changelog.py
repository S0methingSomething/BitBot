import pytest
from src.post_to_reddit import _get_version_changes, _generate_changelog

class TestChangelogGeneration:
    """Test cases for changelog generation functionality."""
    
    def test_generate_changelog_with_all_types(self):
        """Test generating changelog with added, updated, and removed items."""
        # Create mock config object with the formats we need
        class MockFormats:
            def __init__(self):
                self.added_landing = "* Added {display_name} {asset_name} v{version}"
                self.updated_landing = "* Updated {display_name} {asset_name} to v{new_version} (from v{old_version})"
                self.removed_landing = "* Removed {display_name} {asset_name} (was v{old_version})"
                
        class MockRedditFormats:
            def __init__(self):
                self.changelog = MockFormats()
                
        class MockReddit:
            def __init__(self):
                self.formats = MockRedditFormats()
                self.post_mode = "landing_page"
                
        class MockGitHub:
            def __init__(self):
                self.asset_file_name = "MonetizationVars"
                
        class MockConfig:
            def __init__(self):
                self.reddit = MockReddit()
                self.github = MockGitHub()
        
        config = MockConfig()
        
        added = {
            "bitlife": {
                "display_name": "BitLife",
                "version": "3.19.7",
                "url": "https://example.com/bitlife-v3.19.7"
            }
        }
        
        updated = {
            "bitlife_go": {
                "new": {
                    "display_name": "BitLife Go",
                    "version": "1.1.3",
                    "url": "https://example.com/bitlife_go-v1.1.3"
                },
                "old": "1.1.2"
            }
        }
        
        removed = {
            "bitlife_br": {
                "display_name": "BitLife BR",
                "version": "1.18.10"
            }
        }
        
        changelog = _generate_changelog(config, added, updated, removed)
        
        # Check that all sections are present
        assert "### Added" in changelog
        assert "### Updated" in changelog
        assert "### Removed" in changelog
        
        # Check specific entries
        assert "* Added BitLife MonetizationVars v3.19.7" in changelog
        assert "* Updated BitLife Go MonetizationVars to v1.1.3 (from v1.1.2)" in changelog
        assert "* Removed BitLife BR MonetizationVars (was v1.18.10)" in changelog