"""Tests for the ReleaseManagementService."""

import pytest

from src.bitbot.services.release_management_service import ReleaseManagementService


@pytest.fixture
def mock_services(mocker):
    """Fixture to create mocked services."""
    return {
        "logging_service": mocker.MagicMock(),
        "config_service": mocker.MagicMock(),
        "github_service": mocker.MagicMock(),
        "state_service": mocker.MagicMock(),
        "parsing_service": mocker.MagicMock(),
        "file_patcher_service": mocker.MagicMock(),
    }


def test_no_new_releases(mock_services):
    """Test that the service does nothing when there are no new releases."""
    # Arrange
    mock_services["github_service"].get_source_releases.return_value = []
    mock_services["state_service"].load_release_state.return_value = []
    service = ReleaseManagementService(**mock_services)

    # Act
    service.process_new_releases()

    # Assert
    mock_services["logging_service"].info.assert_any_call("No new source releases found to process.")
    mock_services["state_service"].save_release_state.assert_not_called()


def test_process_new_release_successfully(mock_services):
    """Test that a new release is processed correctly."""
    # Arrange
    new_release = {"id": 123, "tag_name": "v1.0", "body": "Release notes", "created_at": "2025-01-01T00:00:00Z"}
    parsed_info = {"app_id": "test_app", "version": "1.0", "asset_name": "test.zip"}

    mock_services["github_service"].get_source_releases.return_value = [new_release]
    mock_services["state_service"].load_release_state.return_value = []
    mock_services["parsing_service"].parse_release_notes.return_value = parsed_info
    mock_services["github_service"].check_release_exists.return_value = False
    service = ReleaseManagementService(**mock_services)

    # Act
    service.process_new_releases()

    # Assert
    mock_services["parsing_service"].parse_release_notes.assert_called_once_with(
        "Release notes", mock_services["config_service"].get_config()
    )
    mock_services["github_service"].check_release_exists.assert_called_once_with("test_app-v1.0")
    mock_services["logging_service"].info.assert_any_call("Successfully processed release 123")
    mock_services["state_service"].save_release_state.assert_called_once()


def test_skip_already_processed_release(mock_services):
    """Test that an already processed release is skipped."""
    # Arrange
    release = {"id": 123, "tag_name": "v1.0", "body": "Release notes", "created_at": "2025-01-01T00:00:00Z"}
    mock_services["github_service"].get_source_releases.return_value = [release]
    mock_services["state_service"].load_release_state.return_value = [123]  # This ID is already in the state
    service = ReleaseManagementService(**mock_services)

    # Act
    service.process_new_releases()

    # Assert
    mock_services["logging_service"].info.assert_any_call("No new source releases found to process.")
    mock_services["parsing_service"].parse_release_notes.assert_not_called()


def test_skip_release_if_parsing_fails(mock_services):
    """Test that a release is skipped if parsing fails."""
    # Arrange
    new_release = {"id": 456, "tag_name": "v2.0", "body": "Bad notes", "created_at": "2025-01-02T00:00:00Z"}
    mock_services["github_service"].get_source_releases.return_value = [new_release]
    mock_services["state_service"].load_release_state.return_value = []
    mock_services["parsing_service"].parse_release_notes.return_value = None  # Parsing fails
    service = ReleaseManagementService(**mock_services)

    # Act
    service.process_new_releases()

    # Assert
    mock_services["logging_service"].warning.assert_any_call("Could not parse release info. Skipping.")
    mock_services["github_service"].check_release_exists.assert_not_called()
    # The state should still be saved even if one release fails
    mock_services["state_service"].save_release_state.assert_called_once()
