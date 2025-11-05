"""Tests for GitHub release operations."""

from unittest.mock import MagicMock

from bitbot.core.errors import GitHubAPIError
from bitbot.core.result import Err, Ok
from bitbot.gh.releases.fetcher import get_github_data, get_source_releases


def test_get_github_data_success(mocker):
    """Test get_github_data returns Ok on success."""
    mock_run = mocker.patch("bitbot.gh.releases.fetcher.run_command")
    mock_process = MagicMock()
    mock_process.stdout = '{"name": "test-repo"}'
    mock_run.return_value = Ok(mock_process)

    result = get_github_data("/repos/owner/repo")

    assert result.is_ok()
    data = result.unwrap()
    assert data["name"] == "test-repo"


def test_get_github_data_invalid_json(mocker):
    """Test get_github_data returns Err on invalid JSON."""
    mock_run = mocker.patch("bitbot.gh.releases.fetcher.run_command")
    mock_process = MagicMock()
    mock_process.stdout = "not valid json{"
    mock_run.return_value = Ok(mock_process)

    result = get_github_data("/repos/owner/repo")

    assert result.is_err()
    assert "Failed to parse" in str(result.unwrap_err())


def test_get_source_releases_success(mocker):
    """Test get_source_releases returns list of releases."""
    mock_get = mocker.patch("bitbot.gh.releases.fetcher.get_github_data")
    mock_get.return_value = Ok(
        [
            {"id": 1, "tag_name": "v1.0.0"},
            {"id": 2, "tag_name": "v2.0.0"},
        ]
    )

    result = get_source_releases("owner/repo")

    assert result.is_ok()
    releases = result.unwrap()
    assert len(releases) == 2
    assert releases[0]["tag_name"] == "v1.0.0"


def test_get_source_releases_not_list(mocker):
    """Test get_source_releases returns Err if response not list."""
    mock_get = mocker.patch("bitbot.gh.releases.fetcher.get_github_data")
    mock_get.return_value = Ok({"error": "not a list"})

    result = get_source_releases("owner/repo")

    assert result.is_err()
    assert "Expected list" in str(result.unwrap_err())


def test_get_github_data_empty_response(mocker):
    """Test get_github_data handles empty JSON object."""
    mock_run = mocker.patch("bitbot.gh.releases.fetcher.run_command")
    mock_process = MagicMock()
    mock_process.stdout = "{}"
    mock_run.return_value = Ok(mock_process)

    result = get_github_data("/repos/owner/repo")

    assert result.is_ok()
    assert result.unwrap() == {}


def test_get_github_data_array_response(mocker):
    """Test get_github_data handles JSON array."""
    mock_run = mocker.patch("bitbot.gh.releases.fetcher.run_command")
    mock_process = MagicMock()
    mock_process.stdout = '[{"id": 1}, {"id": 2}]'
    mock_run.return_value = Ok(mock_process)

    result = get_github_data("/repos/owner/repo")

    assert result.is_ok()
    data = result.unwrap()
    assert isinstance(data, list)
    assert len(data) == 2


def test_get_source_releases_empty_list(mocker):
    """Test get_source_releases handles empty release list."""
    mock_get = mocker.patch("bitbot.gh.releases.fetcher.get_github_data")
    mock_get.return_value = Ok([])

    result = get_source_releases("owner/repo")

    assert result.is_ok()
    assert result.unwrap() == []


def test_get_source_releases_propagates_error(mocker):
    """Test get_source_releases propagates get_github_data errors."""
    mock_get = mocker.patch("bitbot.gh.releases.fetcher.get_github_data")
    mock_get.return_value = Err(GitHubAPIError("API failed"))

    result = get_source_releases("owner/repo")

    assert result.is_err()
    assert "API failed" in str(result.unwrap_err())
