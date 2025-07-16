"""Tests for the release module."""

from unittest.mock import MagicMock, mock_open, patch

from bitbot import release


@patch("bitbot.release.run_command")
def test_get_source_releases(mock_run_command: MagicMock) -> None:
    """Test the get_source_releases function."""
    mock_run_command.return_value.stdout = '[{"tag_name": "v1.0.0"}]'
    releases = release.get_source_releases("test/repo")
    assert len(releases) == 1
    assert releases[0]["tag_name"] == "v1.0.0"


def test_parse_release_description() -> None:
    """Test the parse_release_description function."""
    description = "MonetizationVars for BitLife v3.19.4"
    apps_config = [{"id": "bitlife", "displayName": "BitLife"}]
    result = release.parse_release_description(description, apps_config)
    assert result == ("bitlife", "3.19.4")

    description = "Some other description"
    result = release.parse_release_description(description, apps_config)
    assert result is None


@patch("bitbot.release.run_command")
def test_check_if_bot_release_exists(mock_run_command: MagicMock) -> None:
    """Test the check_if_bot_release_exists function."""
    mock_run_command.return_value = MagicMock()
    assert release.check_if_bot_release_exists("test/repo", "v1.0.0") is True


@patch("bitbot.release.get_github_data")
@patch("bitbot.release.run_command")
def test_download_asset(
    mock_run_command: MagicMock, mock_get_github_data: MagicMock
) -> None:
    """Test the download_asset function."""
    mock_get_github_data.return_value = [{"id": 123, "name": "test.txt"}]
    mock_run_command.return_value = MagicMock()
    path = release.download_asset("test/repo", 1, "test.txt")
    assert path == "dist/original_test.txt"


@patch("bitbot.crypto.patch_file")
def test_patch_file(mock_patch_file: MagicMock) -> None:
    """Test the patch_file function."""
    release.patch_file("original.txt", "patched.txt")
    mock_patch_file.assert_called_once_with("original.txt", "dist/patched.txt")


@patch("bitbot.release.create_bot_release")
@patch("bitbot.release.patch_file")
@patch("bitbot.release.download_asset")
@patch("bitbot.release.check_if_bot_release_exists")
@patch("bitbot.release.get_source_releases")
@patch("bitbot.release.load_config")
def test_main(
    mock_load_config: MagicMock,
    mock_get_source_releases: MagicMock,
    mock_check_if_bot_release_exists: MagicMock,
    mock_download_asset: MagicMock,
    mock_patch_file: MagicMock,
    mock_create_bot_release: MagicMock,
) -> None:
    """Test the main function."""
    mock_load_config.return_value = {
        "github": {
            "sourceRepo": "test/source",
            "botRepo": "test/bot",
            "assetFileName": "test.txt",
        },
        "apps": [{"id": "bitlife", "displayName": "BitLife"}],
    }
    mock_get_source_releases.return_value = [
        {"body": "MonetizationVars for BitLife v1.0.0", "tag_name": "v1.0.0", "id": 1}
    ]
    mock_check_if_bot_release_exists.return_value = False
    mock_download_asset.return_value = "original.txt"
    mock_patch_file.return_value = "patched.txt"

    with patch("builtins.open", mock_open(read_data="")):
        release.main()

    mock_create_bot_release.assert_called_once()


@patch("bitbot.release.create_bot_release")
@patch("bitbot.release.patch_file")
@patch("bitbot.release.download_asset")
@patch("bitbot.release.check_if_bot_release_exists")
@patch("bitbot.release.get_source_releases")
@patch("bitbot.release.load_config")
def test_main_no_new_releases(
    mock_load_config: MagicMock,
    mock_get_source_releases: MagicMock,
    mock_check_if_bot_release_exists: MagicMock,
    mock_download_asset: MagicMock,
    mock_patch_file: MagicMock,
    mock_create_bot_release: MagicMock,
) -> None:
    """Test the main function when there are no new releases."""
    mock_load_config.return_value = {
        "github": {
            "sourceRepo": "test/source",
            "botRepo": "test/bot",
            "assetFileName": "test.txt",
        },
        "apps": [{"id": "bitlife", "displayName": "BitLife"}],
    }
    mock_get_source_releases.return_value = [
        {"body": "MonetizationVars for BitLife v1.0.0", "tag_name": "v1.0.0", "id": 1}
    ]
    mock_check_if_bot_release_exists.return_value = True

    with patch("builtins.open", mock_open(read_data="")):
        release.main()

    mock_create_bot_release.assert_not_called()
