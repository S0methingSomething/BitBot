"""Tests for the ChangelogService."""

import pytest

from src.bitbot.services.changelog_service import ChangelogService


@pytest.fixture
def mock_services(mocker):
    """Fixture to create mocked services."""
    return {
        "parsing_service": mocker.MagicMock(),
        "config": mocker.MagicMock(),
    }


def test_generate_changelog_with_releases(mock_services):
    """Test that the changelog is generated correctly with new releases."""
    # Arrange
    releases = [
        {"body": "app: app1\nversion: 1.0\nasset_name: app1.zip"},
        {"body": "app: app2\nversion: 2.0\nasset_name: app2.zip"},
    ]
    mock_services["parsing_service"].parse_release_notes.side_effect = [
        {"app_id": "app1", "version": "1.0", "asset_name": "app1.zip"},
        {"app_id": "app2", "version": "2.0", "asset_name": "app2.zip"},
    ]
    service = ChangelogService(**mock_services)

    # Act
    changelog = service.generate_changelog(releases)

    # Assert
    assert len(changelog.added) == 2
    assert changelog.added[0].app_id == "app1"
    assert changelog.added[1].app_id == "app2"


def test_generate_changelog_with_no_releases(mock_services):
    """Test that an empty changelog is generated when there are no releases."""
    # Arrange
    service = ChangelogService(**mock_services)

    # Act
    changelog = service.generate_changelog([])

    # Assert
    assert len(changelog.added) == 0
    assert len(changelog.updated) == 0
    assert len(changelog.removed) == 0


def test_generate_changelog_with_parsing_failure(mock_services):
    """Test that a release is skipped if parsing fails."""
    # Arrange
    releases = [
        {"body": "app: app1\nversion: 1.0\nasset_name: app1.zip"},
        {"body": "bad release notes"},
    ]
    mock_services["parsing_service"].parse_release_notes.side_effect = [
        {"app_id": "app1", "version": "1.0", "asset_name": "app1.zip"},
        None,
    ]
    service = ChangelogService(**mock_services)

    # Act
    changelog = service.generate_changelog(releases)

    # Assert
    assert len(changelog.added) == 1
    assert changelog.added[0].app_id == "app1"
