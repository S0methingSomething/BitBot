"""Shared test fixtures."""

import pytest

from bitbot.config_models import (
    Config,
    GitHubConfig,
    RedditConfig,
    RedditFormats,
    RedditTemplates,
)


@pytest.fixture
def github_config():
    """Create minimal GitHubConfig for testing."""
    return GitHubConfig(
        sourceRepo="owner/source",
        botRepo="owner/bot",
        assetFileName="TestAsset",
        pages_url="https://example.com",
    )


@pytest.fixture
def reddit_templates():
    """Create minimal RedditTemplates for testing."""
    return RedditTemplates(
        post="post.md",
        outdated_post="outdated.md",
        inject_banner="banner.md",
    )


@pytest.fixture
def reddit_formats():
    """Create minimal RedditFormats for testing."""
    return RedditFormats(
        titles={
            "added_only": "[BitBot] New: {{added_list}}",
            "updated_only_single": "[BitBot] Update: {{updated_list}}",
            "updated_only_multi": "[BitBot] Updates: {{updated_list}}",
            "mixed_single_update": "[BitBot] New: {{added_list}} | Update: {{updated_list}}",
            "mixed_multi_update": "[BitBot] New: {{added_list}} | Updates: {{updated_list}}",
            "generic": "[BitBot] Update ({{date}})",
        },
        changelog={
            "added_landing": "* Added {{display_name}} {{asset_name}} v{{version}}",
            "updated_landing": "* Updated {{display_name}} to v{{new_version}}",
            "removed_landing": "* Removed {{display_name}} (was v{{old_version}})",
            "added_direct": "* Added {{display_name}} v{{version}}",
            "updated_direct": "* Updated {{display_name}} to v{{new_version}}",
            "removed_direct": "* Removed {{display_name}} (was v{{old_version}})",
        },
        table={
            "header": "| App | Asset | Version |",
            "divider": "|---|---|---:|",
            "line": "| {{display_name}} | {{asset_name}} | v{{version}} |",
        },
    )


@pytest.fixture
def reddit_config(reddit_templates, reddit_formats):
    """Create minimal RedditConfig for testing."""
    return RedditConfig(
        subreddit="TestSubreddit",
        botName="TestBot",
        creator="TestCreator",
        userAgent="TestBot/1.0",
        postMode="rolling_update",
        downloadMode="landing_page",
        templates=reddit_templates,
        formats=reddit_formats,
    )


@pytest.fixture
def config(github_config, reddit_config):
    """Create minimal Config for testing."""
    return Config(
        github=github_config,
        reddit=reddit_config,
        apps=[
            {"id": "bitlife", "displayName": "BitLife"},
            {"id": "doglife", "displayName": "DogLife"},
        ],
        parsing={
            "app_key": "app",
            "version_key": "version",
            "asset_name_key": "asset_name",
        },
        feedback={
            "statusLineFormat": "**Status:** {{status}}",
            "statusLineRegex": r"^\*\*Status:\*\*.*$",
            "workingKeywords": ["working", "works"],
            "notWorkingKeywords": ["broken", "not working"],
            "minFeedbackCount": 2,
            "labels": {"working": "Working", "broken": "Broken", "unknown": "Unknown"},
        },
        timing={"firstCheck": 300, "maxWait": 3600, "increaseBy": 300},
        safety={"max_outbound_links_warn": 5, "max_outbound_links_error": 8},
    )


@pytest.fixture
def config_single_app(github_config, reddit_config):
    """Create Config with single app for testing."""
    return Config(
        github=github_config,
        reddit=reddit_config,
        apps=[{"id": "bitlife", "displayName": "BitLife"}],
        parsing={
            "app_key": "app",
            "version_key": "version",
            "asset_name_key": "asset_name",
        },
    )
