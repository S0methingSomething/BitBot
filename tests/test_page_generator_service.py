"""Tests for the PageGeneratorService."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.bitbot.models.page_data import AppData, PageData, WebRelease
from src.bitbot.services.page_generator_service import PageGeneratorService


@pytest.fixture
def mock_config(mocker):
    """Fixture to create a mocked config."""
    config = mocker.MagicMock()
    # Use an absolute path for the template
    config.reddit.templates.custom_landing = str(Path("tests/dummy_template.html").resolve())
    config.github.bot_repo = "test/repo"
    return config


def test_generate_page_with_data(mock_config):
    """Test that the page is generated correctly with data."""
    # Arrange
    page_data = PageData(
        apps={
            "app1": AppData(
                display_name="App One",
                latest_release=WebRelease(
                    version="2.0",
                    published_at="2025-01-02",
                    download_url="http://example.com/app1-2.0.zip",
                ),
                previous_releases=[
                    WebRelease(
                        version="1.0",
                        published_at="2025-01-01",
                        download_url="http://example.com/app1-1.0.zip",
                    )
                ],
            )
        }
    )
    service = PageGeneratorService(config=mock_config, logger=MagicMock())

    # Act
    html = service.generate_page(page_data)

    # Assert
    assert "<h1>App One</h1>" in html
    assert "<p>Latest: 2.0</p>" in html
    assert "<p>1.0</p>" in html
    assert "No releases yet." not in html


def test_generate_page_with_no_releases(mock_config):
    """Test that the page is generated correctly when an app has no releases."""
    # Arrange
    page_data = PageData(apps={"app1": AppData(display_name="App One", latest_release=None, previous_releases=[])})
    service = PageGeneratorService(config=mock_config, logger=MagicMock())

    # Act
    html = service.generate_page(page_data)

    # Assert
    assert "<h1>App One</h1>" in html
    assert "No releases yet." in html
    assert "Latest:" not in html
