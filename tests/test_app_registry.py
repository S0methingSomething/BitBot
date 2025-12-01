"""Tests for app registry."""

import pytest

from bitbot.core.app_registry import AppNotFoundError, AppRegistry
from bitbot.models import App


@pytest.fixture
def bitlife_app():
    """BitLife app fixture."""
    return App(id="bitlife", displayName="BitLife")


@pytest.fixture
def doglife_app():
    """DogLife app fixture."""
    return App(id="doglife", displayName="DogLife")


@pytest.fixture
def catlife_app():
    """CatLife app fixture."""
    return App(id="catlife", displayName="CatLife")


@pytest.fixture
def registry(bitlife_app, doglife_app):
    """Registry with BitLife and DogLife."""
    return AppRegistry([bitlife_app, doglife_app])


@pytest.fixture
def full_registry(bitlife_app, doglife_app, catlife_app):
    """Registry with all apps."""
    return AppRegistry([bitlife_app, doglife_app, catlife_app])


class TestAppRegistry:
    """Tests for AppRegistry."""

    def test_get_by_exact_id(self, registry, bitlife_app):
        """Get app by exact ID."""
        assert registry.get("bitlife") == bitlife_app

    def test_get_by_lowercase_id(self, registry, bitlife_app):
        """Get app by lowercase ID."""
        assert registry.get("BITLIFE") == bitlife_app

    def test_get_by_display_name(self, registry, bitlife_app):
        """Get app by display name."""
        assert registry.get("BitLife") == bitlife_app

    def test_get_by_display_name_case_insensitive(self, registry, bitlife_app):
        """Get app by display name case insensitive."""
        assert registry.get("bitlife") == bitlife_app
        assert registry.get("BITLIFE") == bitlife_app

    def test_get_returns_none_for_unknown(self, registry):
        """Get returns None for unknown app."""
        assert registry.get("unknown") is None
        assert registry.get("notanapp") is None

    def test_get_or_raise_success(self, registry, bitlife_app):
        """get_or_raise returns app when found."""
        assert registry.get_or_raise("bitlife") == bitlife_app

    def test_get_or_raise_raises(self, registry):
        """get_or_raise raises AppNotFoundError when not found."""
        with pytest.raises(AppNotFoundError):
            registry.get_or_raise("unknown")

    def test_exists_true(self, registry):
        """exists returns True for known app."""
        assert registry.exists("bitlife")
        assert registry.exists("BitLife")
        assert registry.exists("doglife")

    def test_exists_false(self, registry):
        """exists returns False for unknown app."""
        assert not registry.exists("unknown")
        assert not registry.exists("catlife")

    def test_all_returns_all_apps(self, registry, bitlife_app, doglife_app):
        """all returns all registered apps."""
        all_apps = registry.all
        assert bitlife_app in all_apps
        assert doglife_app in all_apps
        assert len(all_apps) == 2

    def test_ids_returns_all_ids(self, registry):
        """ids returns all app IDs."""
        ids = registry.ids
        assert "bitlife" in ids
        assert "doglife" in ids
        assert len(ids) == 2

    def test_len(self, registry):
        """len() returns number of apps."""
        assert len(registry) == 2

    def test_contains(self, registry):
        """in operator works."""
        assert "bitlife" in registry
        assert "BitLife" in registry
        assert "unknown" not in registry

    # BitBot-specific scenarios
    def test_real_app_ids(self, full_registry):
        """Test with real BitBot app IDs."""
        assert full_registry.get("bitlife") is not None
        assert full_registry.get("doglife") is not None
        assert full_registry.get("catlife") is not None

    def test_lookup_from_release_body_app_id(self, registry):
        """Test lookup using app ID from release body."""
        # Simulating: app: bitlife from release body
        app_id_from_release = "bitlife"
        app = registry.get(app_id_from_release)
        assert app is not None
        assert app.display_name == "BitLife"

    def test_lookup_preserves_original_case(self, registry):
        """Test that returned app preserves original case."""
        app = registry.get("BITLIFE")
        assert app.id == "bitlife"  # Original case
        assert app.display_name == "BitLife"  # Original case

    def test_empty_registry(self):
        """Test empty registry."""
        empty = AppRegistry([])
        assert len(empty) == 0
        assert empty.get("anything") is None
        assert not empty.exists("anything")

    def test_single_app_registry(self, bitlife_app):
        """Test registry with single app."""
        single = AppRegistry([bitlife_app])
        assert len(single) == 1
        assert single.get("bitlife") == bitlife_app

    def test_iteration(self, registry, bitlife_app, doglife_app):
        """Test getting all apps from registry."""
        apps = registry.all
        assert len(apps) == 2
        assert bitlife_app in apps
        assert doglife_app in apps


class TestAppNotFoundError:
    """Tests for AppNotFoundError."""

    def test_error_message(self):
        """Error has descriptive message."""
        error = AppNotFoundError("bitlife", ["doglife", "catlife"])
        assert "bitlife" in str(error)
        assert "not found" in str(error).lower()

    def test_error_attributes(self):
        """Error stores app identifier."""
        error = AppNotFoundError("bitlife", ["doglife"])
        assert error.identifier == "bitlife"
        assert error.available == ["doglife"]

    def test_error_shows_available_apps(self):
        """Error shows available apps."""
        error = AppNotFoundError("unknown", ["bitlife", "doglife"])
        assert "bitlife" in str(error)
        assert "doglife" in str(error)
