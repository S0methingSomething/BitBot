"""Tests for the RedditPostService."""

import pytest

from src.bitbot.models.changelog import Changelog, ChangelogEntry
from src.bitbot.services.reddit_post_service import RedditPostService


@pytest.fixture
def mock_config(mocker):
    """Fixture to create a mocked config."""
    config = mocker.MagicMock()
    config.reddit.templates.post = "tests/dummy_post_template.md"
    return config


def test_generate_post_with_changelog(mock_config):
    """Test that the post is generated correctly with a changelog."""
    # Arrange
    changelog = Changelog(
        added=[
            ChangelogEntry(app_id="app1", version="1.0", asset_name="app1.zip"),
            ChangelogEntry(app_id="app2", version="2.0", asset_name="app2.zip"),
        ]
    )
    service = RedditPostService(config=mock_config)

    # Act
    post = service.generate_post(changelog)

    # Assert
    assert "New releases available for 2 apps" in post.title
    assert "* app1 v1.0" in post.body
    assert "* app2 v2.0" in post.body


def test_generate_post_with_empty_changelog(mock_config):
    """Test that a post is generated correctly with an empty changelog."""
    # Arrange
    changelog = Changelog()
    service = RedditPostService(config=mock_config)

    # Act
    post = service.generate_post(changelog)

    # Assert
    assert "No new releases" in post.title
    assert "This is the changelog:" in post.body
    assert "* " not in post.body
