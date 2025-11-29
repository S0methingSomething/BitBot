"""Tests for Reddit post parsing."""

from unittest.mock import MagicMock

import praw.models

from bitbot.reddit.parser import parse_versions_from_post


def _make_post(title, body):
    """Create mock Reddit post with proper spec."""
    post = MagicMock(spec=praw.models.Submission)
    post.title = title
    post.selftext = body
    return post


def test_parse_versions_changelog_format(config):
    """Test parsing versions from changelog format."""
    post = _make_post(
        "Update Post",
        "## Changelog\nUpdated BitLife to version 1.2.3\nSome other text",
    )

    result = parse_versions_from_post(post, config)

    assert result.get("bitlife") == "1.2.3"


def test_parse_versions_legacy_title_format(config_single_app):
    """Test parsing versions from legacy title format."""
    post = _make_post("Update for BitLife v2.0.0", "No changelog here")

    result = parse_versions_from_post(post, config_single_app)

    assert result.get("bitlife") == "2.0.0"


def test_parse_versions_no_match(config_single_app):
    """Test returns empty dict when no versions found."""
    post = _make_post("Random Title", "Random body")

    result = parse_versions_from_post(post, config_single_app)

    assert result == {}


def test_parse_versions_multiple_apps(config):
    """Test parsing multiple apps from changelog."""
    post = _make_post(
        "Multi Update",
        "## Changelog\nUpdated BitLife to version 1.0.0\nUpdated DogLife to version 2.0.0",
    )

    result = parse_versions_from_post(post, config)

    assert result.get("bitlife") == "1.0.0"
    assert result.get("doglife") == "2.0.0"


def test_parse_versions_case_insensitive(config_single_app):
    """Test parsing is case insensitive."""
    post = _make_post(
        "Update",
        "## Changelog\nUpdated BITLIFE to version 3.0.0",
    )

    result = parse_versions_from_post(post, config_single_app)

    assert result.get("bitlife") == "3.0.0"
