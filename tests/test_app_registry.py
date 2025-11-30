"""Tests for AppRegistry."""

import pytest

from bitbot.core.app_registry import AppNotFoundError, AppRegistry
from bitbot.models import App


@pytest.fixture
def registry():
    """Create test registry."""
    apps = [
        App(id="BitLife", displayName="BitLife"),
        App(id="BitLife Go", displayName="BitLife Go"),
        App(id="intl_bitlife", displayName="BitLife (International)"),
    ]
    return AppRegistry(apps)


class TestAppRegistry:
    """Tests for AppRegistry."""

    def test_get_by_exact_id(self, registry):
        """Get app by exact ID."""
        app = registry.get("BitLife")
        assert app is not None
        assert app.id == "BitLife"

    def test_get_by_lowercase_id(self, registry):
        """Get app by lowercase ID (case-insensitive)."""
        app = registry.get("bitlife")
        assert app is not None
        assert app.id == "BitLife"

    def test_get_by_display_name(self, registry):
        """Get app by display name."""
        app = registry.get("BitLife (International)")
        assert app is not None
        assert app.id == "intl_bitlife"

    def test_get_returns_none_for_unknown(self, registry):
        """Get returns None for unknown identifier."""
        app = registry.get("unknown_app")
        assert app is None

    def test_get_or_raise_success(self, registry):
        """get_or_raise returns app for valid identifier."""
        app = registry.get_or_raise("BitLife")
        assert app.id == "BitLife"

    def test_get_or_raise_raises(self, registry):
        """get_or_raise raises AppNotFoundError for unknown."""
        with pytest.raises(AppNotFoundError) as exc_info:
            registry.get_or_raise("unknown")
        assert "unknown" in str(exc_info.value)
        assert "BitLife" in exc_info.value.available

    def test_exists_true(self, registry):
        """Exists returns True for known app."""
        assert registry.exists("BitLife")
        assert registry.exists("bitlife")  # case-insensitive

    def test_exists_false(self, registry):
        """Exists returns False for unknown app."""
        assert not registry.exists("unknown")

    def test_all_returns_all_apps(self, registry):
        """All property returns all apps."""
        assert len(registry.all) == 3

    def test_ids_returns_all_ids(self, registry):
        """Ids property returns all app IDs."""
        assert registry.ids == frozenset({"BitLife", "BitLife Go", "intl_bitlife"})

    def test_len(self, registry):
        """Len returns number of apps."""
        assert len(registry) == 3

    def test_contains(self, registry):
        """In operator works."""
        assert "BitLife" in registry
        assert "unknown" not in registry


class TestAppNotFoundError:
    """Tests for AppNotFoundError."""

    def test_error_message(self):
        """Error message includes identifier and available apps."""
        error = AppNotFoundError("unknown", ["BitLife", "DogLife"])
        assert "unknown" in str(error)
        assert "BitLife" in str(error)
        assert "DogLife" in str(error)

    def test_error_attributes(self):
        """Error has identifier and available attributes."""
        error = AppNotFoundError("test", ["a", "b"])
        assert error.identifier == "test"
        assert error.available == ["a", "b"]
