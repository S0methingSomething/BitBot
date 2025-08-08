"""Tests for the RedditOrchestrationService."""

from datetime import datetime, timedelta, timezone

import pytest

from src.bitbot.models.changelog import Changelog, ChangelogEntry
from src.bitbot.models.state import BotState
from src.bitbot.services.reddit_orchestration_service import RedditOrchestrationService


@pytest.fixture
def mock_services(mocker):
    """Fixture to create mocked services."""
    return {
        "logging_service": mocker.MagicMock(),
        "state_service": mocker.MagicMock(),
        "reddit_service": mocker.MagicMock(),
        "reddit_post_service": mocker.MagicMock(),
    }


def test_manage_reddit_post_creates_new_post_if_none_exists(mock_services):
    """Test that a new post is created if no active post exists."""
    # Arrange
    changelog = Changelog(added=[ChangelogEntry(app_id="test", version="1.0", asset_name="test.zip")])
    mock_services["state_service"].load_bot_state.return_value = BotState(active_post_id=None)
    mock_services["reddit_service"].create_post.return_value = "new_post_id"
    service = RedditOrchestrationService(**mock_services)

    # Act
    service.manage_reddit_post(changelog)

    # Assert
    mock_services["reddit_service"].create_post.assert_called_once()
    mock_services["state_service"].save_bot_state.assert_called_once()
    saved_state = mock_services["state_service"].save_bot_state.call_args[0][0]
    assert saved_state.active_post_id == "new_post_id"


def test_manage_reddit_post_creates_new_post_if_old(mock_services):
    """Test that a new post is created if the active post is old."""
    # Arrange
    changelog = Changelog(added=[ChangelogEntry(app_id="test", version="1.0", asset_name="test.zip")])
    eight_days_ago = datetime.now(timezone.utc) - timedelta(days=8)
    mock_services["state_service"].load_bot_state.return_value = BotState(
        active_post_id="old_post_id", last_major_post_timestamp=eight_days_ago
    )
    mock_services["reddit_service"].create_post.return_value = "new_post_id"
    service = RedditOrchestrationService(**mock_services)

    # Act
    service.manage_reddit_post(changelog)

    # Assert
    mock_services["reddit_service"].create_post.assert_called_once()
    mock_services["state_service"].save_bot_state.assert_called_once()


def test_manage_reddit_post_updates_existing_post_if_recent(mock_services):
    """Test that an existing post is updated if it is recent."""
    # Arrange
    changelog = Changelog(added=[ChangelogEntry(app_id="test", version="1.0", asset_name="test.zip")])
    six_days_ago = datetime.now(timezone.utc) - timedelta(days=6)
    mock_services["state_service"].load_bot_state.return_value = BotState(
        active_post_id="recent_post_id"
    )
    service = RedditOrchestrationService(**mock_services)

    # Act
    service.manage_reddit_post(changelog)

    # Assert
    mock_services["reddit_service"].update_post.assert_called_once()
    mock_services["state_service"].save_bot_state.assert_called_once()


def test_manage_reddit_post_does_nothing_if_changelog_is_empty(mock_services):
    """Test that nothing happens if the changelog is empty."""
    # Arrange
    changelog = Changelog()  # Changelog is empty
    service = RedditOrchestrationService(**mock_services)

    # Act
    service.manage_reddit_post(changelog)

    # Assert
    mock_services["reddit_service"].create_post.assert_not_called()
    mock_services["reddit_service"].update_post.assert_not_called()
    mock_services["state_service"].save_bot_state.assert_not_called()
