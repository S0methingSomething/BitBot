"""Tests for Reddit posting modules."""

from bitbot.reddit.posting.changelog import generate_changelog
from bitbot.reddit.posting.poster import count_outbound_links
from bitbot.reddit.posting.title_generator import create_app_list, generate_dynamic_title


# count_outbound_links tests
def test_count_outbound_links_none():
    """Test counting links in text with no links."""
    assert count_outbound_links("No links here") == 0


def test_count_outbound_links_single():
    """Test counting single link."""
    assert count_outbound_links("Check https://example.com") == 1


def test_count_outbound_links_multiple():
    """Test counting multiple links."""
    text = "Visit https://a.com and https://b.com or http://c.com"
    assert count_outbound_links(text) == 3


def test_count_outbound_links_duplicates():
    """Test duplicate links counted once."""
    text = "https://example.com and https://example.com again"
    assert count_outbound_links(text) == 1


# create_app_list tests
def test_create_app_list_single():
    """Test creating app list with single app."""
    apps = {"app1": {"display_name": "App One", "version": "1.0.0"}}
    result = create_app_list(apps)
    assert result == "App One v1.0.0"


def test_create_app_list_multiple():
    """Test creating app list with multiple apps."""
    apps = {
        "app1": {"display_name": "App One", "version": "1.0.0"},
        "app2": {"display_name": "App Two", "version": "2.0.0"},
    }
    result = create_app_list(apps)
    assert "App One v1.0.0" in result
    assert "App Two v2.0.0" in result


def test_create_app_list_nested_new():
    """Test creating app list with nested 'new' structure."""
    apps = {"app1": {"new": {"display_name": "Updated App", "version": "3.0.0"}}}
    result = create_app_list(apps)
    assert result == "Updated App v3.0.0"


# generate_dynamic_title tests
def test_generate_title_added_only(config):
    """Test title generation for added apps only."""
    added = {"app1": {"display_name": "New App", "version": "1.0.0"}}
    updated = {}

    result = generate_dynamic_title(config, added, updated)

    assert "[BitBot]" in result
    assert "New App v1.0.0" in result


def test_generate_title_updated_single(config):
    """Test title generation for single update."""
    added = {}
    updated = {"app1": {"new": {"display_name": "App", "version": "2.0.0"}}}

    result = generate_dynamic_title(config, added, updated)

    assert "Update" in result


def test_generate_title_generic_many_changes(config):
    """Test title falls back to generic for many changes."""
    added = {f"app{i}": {"display_name": f"App {i}", "version": "1.0"} for i in range(5)}
    updated = {}

    result = generate_dynamic_title(config, added, updated)

    assert "[BitBot]" in result


# generate_changelog tests
def test_generate_changelog_added(config):
    """Test changelog with added apps."""
    added = {"app1": {"display_name": "New App", "version": "1.0.0", "url": "http://x.com"}}

    result = generate_changelog(config, added=added, updated={}, removed={})

    assert "Added" in result
    assert "New App" in result
    assert "v1.0.0" in result


def test_generate_changelog_updated(config):
    """Test changelog with updated apps."""
    updated = {
        "app1": {
            "new": {"display_name": "App", "version": "2.0.0", "url": "http://x.com"},
            "old": "1.0.0",
        }
    }

    result = generate_changelog(config, added={}, updated=updated, removed={})

    assert "Updated" in result
    assert "v2.0.0" in result


def test_generate_changelog_removed(config):
    """Test changelog with removed apps."""
    removed = {"app1": {"display_name": "Old App", "version": "1.0.0"}}

    result = generate_changelog(config, added={}, updated={}, removed=removed)

    assert "Removed" in result
    assert "Old App" in result


def test_generate_changelog_empty(config):
    """Test changelog with no changes."""
    result = generate_changelog(config, added={}, updated={}, removed={})

    assert "No new updates" in result
