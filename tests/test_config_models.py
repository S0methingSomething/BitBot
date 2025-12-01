"""Tests for BitBot configuration models."""

import pytest
from pydantic import ValidationError

from bitbot.config_models import Config, GitHubConfig, RedditConfig, RedditFormats, RedditTemplates


class TestGitHubConfig:
    """Tests for GitHubConfig validation."""

    def test_valid_config(self):
        """Test valid GitHub config."""
        config = GitHubConfig(
            sourceRepo="owner/source",
            botRepo="owner/bot",
            assetFileName="asset.zip",
            pages_url="https://example.com",
        )
        assert config.source_repo == "owner/source"
        assert config.bot_repo == "owner/bot"

    def test_invalid_repo_format_no_slash(self):
        """Test repo without slash is rejected."""
        with pytest.raises(ValidationError, match="owner/name"):
            GitHubConfig(
                sourceRepo="invalid",
                botRepo="owner/bot",
                assetFileName="asset.zip",
                pages_url="https://example.com",
            )

    def test_invalid_repo_format_multiple_slashes(self):
        """Test repo with multiple slashes is rejected."""
        with pytest.raises(ValidationError, match="owner/name"):
            GitHubConfig(
                sourceRepo="owner/repo/extra",
                botRepo="owner/bot",
                assetFileName="asset.zip",
                pages_url="https://example.com",
            )

    def test_invalid_asset_with_path_separator(self):
        """Test asset filename with path separator is rejected."""
        with pytest.raises(ValidationError, match="path separators"):
            GitHubConfig(
                sourceRepo="owner/source",
                botRepo="owner/bot",
                assetFileName="path/to/asset.zip",
                pages_url="https://example.com",
            )

    def test_empty_asset_name(self):
        """Test empty asset filename is rejected."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            GitHubConfig(
                sourceRepo="owner/source",
                botRepo="owner/bot",
                assetFileName="   ",
                pages_url="https://example.com",
            )


class TestRedditConfig:
    """Tests for RedditConfig validation."""

    def test_valid_config(self):
        """Test valid Reddit config."""
        config = RedditConfig(
            subreddit="test",
            botName="TestBot",
            creator="testuser",
            userAgent="TestAgent/1.0",
            templates=RedditTemplates(
                post="post.md", outdated_post="outdated.md", inject_banner="banner.md"
            ),
            formats=RedditFormats(titles={}, changelog={}, table={}),
        )
        assert config.subreddit == "test"
        assert config.post_mode == "rolling_update"  # default

    def test_subreddit_strips_prefix(self):
        """Test r/ prefix is stripped from subreddit."""
        config = RedditConfig(
            subreddit="r/test",
            botName="TestBot",
            creator="testuser",
            userAgent="TestAgent/1.0",
            templates=RedditTemplates(
                post="post.md", outdated_post="outdated.md", inject_banner="banner.md"
            ),
            formats=RedditFormats(titles={}, changelog={}, table={}),
        )
        assert config.subreddit == "test"

    def test_invalid_post_mode(self):
        """Test invalid post_mode is rejected."""
        with pytest.raises(ValidationError, match="post_mode"):
            RedditConfig(
                subreddit="test",
                botName="TestBot",
                creator="testuser",
                userAgent="TestAgent/1.0",
                postMode="invalid_mode",
                templates=RedditTemplates(
                    post="post.md", outdated_post="outdated.md", inject_banner="banner.md"
                ),
                formats=RedditFormats(titles={}, changelog={}, table={}),
            )

    def test_invalid_download_mode(self):
        """Test invalid download_mode is rejected."""
        with pytest.raises(ValidationError, match="download_mode"):
            RedditConfig(
                subreddit="test",
                botName="TestBot",
                creator="testuser",
                userAgent="TestAgent/1.0",
                downloadMode="invalid_mode",
                templates=RedditTemplates(
                    post="post.md", outdated_post="outdated.md", inject_banner="banner.md"
                ),
                formats=RedditFormats(titles={}, changelog={}, table={}),
            )

    def test_empty_bot_name_rejected(self):
        """Test empty bot name is rejected."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            RedditConfig(
                subreddit="test",
                botName="   ",
                creator="testuser",
                userAgent="TestAgent/1.0",
                templates=RedditTemplates(
                    post="post.md", outdated_post="outdated.md", inject_banner="banner.md"
                ),
                formats=RedditFormats(titles={}, changelog={}, table={}),
            )


class TestConfig:
    """Tests for main Config model."""

    def test_negative_safety_value_rejected(self):
        """Test negative safety values are rejected."""
        with pytest.raises(ValidationError, match="non-negative"):
            Config(
                github=GitHubConfig(
                    sourceRepo="owner/source",
                    botRepo="owner/bot",
                    assetFileName="asset.zip",
                    pages_url="https://example.com",
                ),
                reddit=RedditConfig(
                    subreddit="test",
                    botName="TestBot",
                    creator="testuser",
                    userAgent="TestAgent/1.0",
                    templates=RedditTemplates(
                        post="post.md", outdated_post="outdated.md", inject_banner="banner.md"
                    ),
                    formats=RedditFormats(titles={}, changelog={}, table={}),
                ),
                safety={"max_retries": -1},
            )

    def test_negative_timing_value_rejected(self):
        """Test negative timing values are rejected."""
        with pytest.raises(ValidationError, match="non-negative"):
            Config(
                github=GitHubConfig(
                    sourceRepo="owner/source",
                    botRepo="owner/bot",
                    assetFileName="asset.zip",
                    pages_url="https://example.com",
                ),
                reddit=RedditConfig(
                    subreddit="test",
                    botName="TestBot",
                    creator="testuser",
                    userAgent="TestAgent/1.0",
                    templates=RedditTemplates(
                        post="post.md", outdated_post="outdated.md", inject_banner="banner.md"
                    ),
                    formats=RedditFormats(titles={}, changelog={}, table={}),
                ),
                timing={"interval": -5},
            )
