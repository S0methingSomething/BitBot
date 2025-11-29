"""Tests for landing page generator."""

from returns.result import Failure, Success

from bitbot.core.errors import PageGeneratorError
from bitbot.gh.page_generator import generate_landing_page


def test_generate_landing_page_success(tmp_path):
    """Test successful page generation."""
    output_path = tmp_path / "output" / "index.html"
    releases_data = {
        "bot_repo": "user/repo",
        "apps": [
            {
                "id": "app1",
                "display_name": "Test App",
                "latest_release": {"version": "1.0.0", "download_url": "http://x.com"},
                "releases": [],
            }
        ],
    }

    result = generate_landing_page(releases_data, output_path, "default_landing_page.html")

    assert isinstance(result, Success)
    assert output_path.exists()


def test_generate_landing_page_creates_directory(tmp_path):
    """Test page generation creates output directory."""
    output_path = tmp_path / "deep" / "nested" / "dir" / "index.html"

    result = generate_landing_page({"apps": []}, output_path, "default_landing_page.html")

    assert isinstance(result, Success)
    assert output_path.parent.exists()


def test_generate_landing_page_template_not_found(tmp_path):
    """Test error when template not found."""
    output_path = tmp_path / "index.html"

    result = generate_landing_page({}, output_path, "nonexistent_template_xyz.html")

    assert isinstance(result, Failure)
    assert isinstance(result.failure(), PageGeneratorError)


def test_generate_landing_page_empty_data(tmp_path):
    """Test page generation with empty data."""
    output_path = tmp_path / "index.html"

    result = generate_landing_page({"apps": []}, output_path, "default_landing_page.html")

    assert isinstance(result, Success)
    assert output_path.exists()


def test_generate_landing_page_string_path(tmp_path):
    """Test page generation with string path."""
    output_path = str(tmp_path / "index.html")

    result = generate_landing_page({"apps": []}, output_path, "default_landing_page.html")

    assert isinstance(result, Success)
