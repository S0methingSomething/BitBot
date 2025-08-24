import json
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import pytest

from src.digest_aggregator import (
    add_release_to_digest,
    format_digest_changelog,
    get_current_cycle_releases,
    load_digest_history,
    save_digest_history,
    should_create_new_digest_cycle,
    start_new_digest_cycle,
)


class TestDigestAggregator:
    """Test cases for the digest aggregator."""

    @pytest.fixture
    def mock_digest_file(self, tmp_path):
        """Create a mock digest file."""
        digest_file = tmp_path / "digest_history.json"
        return digest_file

    def test_load_digest_history_empty(self):
        """Test loading digest history when file doesn't exist."""
        with patch("io_handler.IOHandler.load_digest_history", return_value={}):
            history = load_digest_history()
            assert history == {}

    def test_load_digest_history_with_data(self):
        """Test loading digest history with data."""
        test_data = {"current_cycle": {"releases": []}}
        with patch("io_handler.IOHandler.load_digest_history", return_value=test_data):
            history = load_digest_history()
            assert history == test_data

    def test_save_digest_history(self):
        """Test saving digest history."""
        test_data = {"current_cycle": {"releases": []}}
        with patch("io_handler.IOHandler.save_digest_history") as mock_save:
            save_digest_history(test_data)
            mock_save.assert_called_once_with(test_data)

    def test_add_release_to_digest(self):
        """Test adding a release to digest."""
        release_info = {
            "bitlife": {
                "display_name": "BitLife",
                "version": "3.19.7"
            }
        }

        # Mock the load and save functions to avoid file I/O
        with patch("src.digest_aggregator.load_digest_history", return_value={}), \
             patch("src.digest_aggregator.save_digest_history") as mock_save:
            # Add release
            add_release_to_digest(release_info)
            
            # Check that save was called with correct data
            mock_save.assert_called_once()
            saved_data = mock_save.call_args[0][0]
            assert "current_cycle" in saved_data
            assert len(saved_data["current_cycle"]["releases"]) == 1
            assert saved_data["current_cycle"]["releases"][0]["release"] == release_info

    def test_get_current_cycle_releases(self):
        """Test getting current cycle releases."""
        test_releases = [
            {
                "timestamp": "2025-01-01T00:00:00Z",
                "release": {"bitlife": {"display_name": "BitLife", "version": "3.19.7"}}
            }
        ]

        test_data = {"current_cycle": {"releases": test_releases}}

        with patch("src.digest_aggregator.load_digest_history", return_value=test_data):
            releases = get_current_cycle_releases()
            assert releases == test_releases

    def test_should_create_new_digest_cycle_disabled(self):
        """Test that digest cycle is not created when disabled."""
        class MockConfig:
            def __init__(self):
                self.digest = type("Digest", (), {"enabled": False})()
        
        config = MockConfig()
        assert not should_create_new_digest_cycle(config)

    def test_should_create_new_digest_cycle_no_cycle(self):
        """Test that digest cycle is created when no cycle exists."""
        class MockConfig:
            def __init__(self):
                self.digest = type("Digest", (), {"enabled": True})()
        
        config = MockConfig()
        with patch("src.digest_aggregator.load_digest_history", return_value={}):
            assert should_create_new_digest_cycle(config)

    def test_should_create_new_digest_cycle_expired(self):
        """Test that digest cycle is created when cycle has expired."""
        class MockConfig:
            def __init__(self):
                self.digest = type("Digest", (), {"enabled": True, "cycle_days": 7})()
        
        config = MockConfig()
        past_date = (datetime.now(UTC) - timedelta(days=8)).isoformat()
        history = {"current_cycle": {"start_date": past_date}}
        
        with patch("src.digest_aggregator.load_digest_history", return_value=history):
            assert should_create_new_digest_cycle(config)

    def test_should_create_new_digest_cycle_not_expired(self):
        """Test that digest cycle is not created when cycle has not expired."""
        class MockConfig:
            def __init__(self):
                self.digest = type("Digest", (), {"enabled": True, "cycle_days": 7})()
        
        config = MockConfig()
        recent_date = (datetime.now(UTC) - timedelta(days=1)).isoformat()
        history = {"current_cycle": {"start_date": recent_date}}
        
        with patch("src.digest_aggregator.load_digest_history", return_value=history):
            assert not should_create_new_digest_cycle(config)

    def test_start_new_digest_cycle(self):
        """Test starting a new digest cycle."""
        previous_cycle = {
            "start_date": "2025-01-01T00:00:00Z",
            "releases": [
                {
                    "timestamp": "2025-01-01T00:00:00Z",
                    "release": {"bitlife": {"display_name": "BitLife", "version": "3.19.7"}}
                }
            ]
        }
        
        # Mock the load and save functions
        with patch("src.digest_aggregator.load_digest_history", return_value={"current_cycle": previous_cycle}), \
             patch("src.digest_aggregator.save_digest_history") as mock_save, \
             patch("src.digest_aggregator.datetime") as mock_datetime:
            
            # Mock the current date to be a specific date
            mock_now = datetime(2025, 1, 8, 12, 0, 0, tzinfo=UTC)  # 7 days later
            mock_datetime.now.return_value = mock_now
            mock_datetime.fromisoformat = datetime.fromisoformat
            
            # Start new cycle
            result = start_new_digest_cycle()
        
        # Check that previous cycle was returned
        assert result == previous_cycle
        
        # Check that save was called with correct data
        mock_save.assert_called_once()
        saved_data = mock_save.call_args[0][0]
        assert "current_cycle" in saved_data
        assert len(saved_data["current_cycle"]["releases"]) == 0
        assert "cycle_2025-01-08" in saved_data  # Previous cycle saved with current date

    def test_format_digest_changelog(self):
        """Test formatting digest changelog."""
        releases = [
            {
                "timestamp": "2025-01-01T10:00:00Z",
                "release": {
                    "bitlife": {
                        "display_name": "BitLife",
                        "version": "3.19.7"
                    }
                }
            },
            {
                "timestamp": "2025-01-02T10:00:00Z",
                "release": {
                    "bitlife": {
                        "display_name": "BitLife",
                        "version": "3.19.8"
                    }
                }
            }
        ]
        
        class MockConfig:
            pass
        
        config = MockConfig()
        changelog = format_digest_changelog(releases, config)
        
        assert "## Weekly Digest Changelog" in changelog
        assert "### BitLife" in changelog
        assert "* v3.19.7 - 2025-01-01" in changelog
        assert "* v3.19.8 - 2025-01-02" in changelog