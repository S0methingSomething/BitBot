"""Hypothesis tests for the digest aggregator."""
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from hypothesis import given, strategies as st

from src.digest_aggregator import (
    add_release_to_digest,
    format_digest_changelog,
    get_current_cycle_releases,
    load_digest_history,
    save_digest_history,
    should_create_new_digest_cycle,
    start_new_digest_cycle,
)


class TestDigestAggregatorHypothesis:
    """Hypothesis tests for the digest aggregator."""

    @given(st.dictionaries(st.text(), st.text()))
    def test_save_and_load_digest_history_roundtrip(self, history):
        """Test that saving and loading digest history is a roundtrip."""
        # Make sure the history has the right structure
        if "current_cycle" not in history:
            history["current_cycle"] = {"releases": []}
        
        # Save and load
        save_digest_history(history)
        loaded = load_digest_history()
        
        # Check that the loaded history matches the saved one
        assert loaded == history
        
        # Clean up
        digest_file = Path("/workspaces/BitBot/dist/data/digest_history.json")
        if digest_file.exists():
            digest_file.unlink()

    @given(st.lists(st.dictionaries(st.text(), st.dictionaries(st.text(), st.text()))))
    def test_format_digest_changelog_with_various_inputs(self, releases):
        """Test formatting digest changelog with various inputs."""
        # Convert to the expected format
        formatted_releases = []
        for release in releases:
            # Make sure each app has the required fields
            formatted_release = {}
            for app_id, app_info in release.items():
                if isinstance(app_info, dict):
                    formatted_release[app_id] = app_info
                else:
                    formatted_release[app_id] = {"display_name": app_id, "version": "1.0.0"}
            
            formatted_releases.append({
                "timestamp": "2025-01-01T00:00:00Z",
                "release": formatted_release
            })
        
        # Create a mock config
        class MockConfig:
            pass
        
        config = MockConfig()
        
        # Format the changelog
        changelog = format_digest_changelog(formatted_releases, config)
        
        # Basic checks
        if formatted_releases:
            assert "## Weekly Digest Changelog" in changelog
        else:
            assert "No updates in this cycle." in changelog

    def test_should_create_new_digest_cycle_property(self):
        """Test properties of should_create_new_digest_cycle function."""
        # Create a mock config
        class MockConfig:
            def __init__(self, enabled=True, cycle_days=7):
                self.digest = type("Digest", (), {"enabled": enabled, "cycle_days": cycle_days})()
        
        # Test with disabled digest
        config_disabled = MockConfig(enabled=False)
        assert not should_create_new_digest_cycle(config_disabled)
        
        # Test with enabled digest but no history
        config_enabled = MockConfig(enabled=True)
        with pytest.MonkeyPatch().context() as mp:
            mp.setattr("src.digest_aggregator.load_digest_history", lambda: {})
            assert should_create_new_digest_cycle(config_enabled)