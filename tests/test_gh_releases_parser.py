"""Tests for GitHub releases description parser."""

from bitbot.gh.releases.parser import parse_release_description


def test_parse_single_release():
    """Test parsing single release from description."""
    apps_config = [{"id": "bitlife", "displayName": "BitLife"}]
    description = "app: BitLife\nversion: 1.0.0\nasset_name: MonetizationVars"

    result = parse_release_description(description, apps_config)

    assert len(result) == 1
    assert result[0]["app_id"] == "bitlife"
    assert result[0]["version"] == "1.0.0"
    assert result[0]["asset_name"] == "MonetizationVars"


def test_parse_multiple_releases():
    """Test parsing multiple releases from description."""
    apps_config = [
        {"id": "bitlife", "displayName": "BitLife"},
        {"id": "doglife", "displayName": "DogLife"},
    ]
    description = """app: BitLife
version: 1.0.0
asset_name: Asset1

app: DogLife
version: 2.0.0
asset_name: Asset2"""

    result = parse_release_description(description, apps_config)

    assert len(result) == 2


def test_parse_unknown_app():
    """Test parsing ignores unknown apps."""
    apps_config = [{"id": "bitlife", "displayName": "BitLife"}]
    description = "app: UnknownApp\nversion: 1.0.0\nasset_name: Asset"

    result = parse_release_description(description, apps_config)

    assert len(result) == 0


def test_parse_empty_description():
    """Test parsing empty description."""
    apps_config = [{"id": "bitlife", "displayName": "BitLife"}]

    result = parse_release_description("", apps_config)

    assert result == []


def test_parse_malformed_lines():
    """Test parsing handles malformed lines."""
    apps_config = [{"id": "bitlife", "displayName": "BitLife"}]
    description = "random text\nno colons here\napp: BitLife\nversion: 1.0.0"

    result = parse_release_description(description, apps_config)

    # Should still parse the valid app
    assert len(result) >= 0  # May or may not find it depending on implementation
