# src/bitbot/settings.py
"""
Pydantic models for loading and validating application configuration.
"""

from pathlib import Path
from typing import List

import tomlkit
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class AppSettings(BaseModel):
    """Configuration for a single monitored application."""

    id: str
    display_name: str


class GitHubSettings(BaseModel):
    """Settings related to GitHub repositories."""

    source_repo: str
    bot_repo: str
    asset_file_name: str


class RedditSettings(BaseModel):
    """Settings related to Reddit interaction."""

    subreddit: str
    post_style: str
    max_outbound_links_warning: int
    post_title_template: str
    creator_username: str


class Settings(BaseSettings):
    """The main settings object for the application."""

    github: GitHubSettings
    reddit: RedditSettings
    apps: List[AppSettings]


def load_settings(path: Path = Path("config.toml")) -> Settings:
    """Loads and validates the application settings from a TOML file."""
    data = tomlkit.loads(path.read_text())
    return Settings(**data)
