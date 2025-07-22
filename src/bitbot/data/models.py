"""Pydantic models for BitBot."""

from typing import List, Optional

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseModel):
    """Represents the configuration for a single application to monitor."""

    name: str
    github_repo: str
    subreddit: str
    post_title_template: str


class Config(BaseModel):
    """Represents the main configuration for the bot."""

    apps: List[AppConfig]


class GitHubRelease(BaseModel):
    """Represents a GitHub release."""

    version: str
    url: str
    body: Optional[str] = None


class RedditPost(BaseModel):
    """Represents a Reddit post."""

    id: str
    url: str
    title: str
    body: str


class BotState(BaseModel):
    """Represents the state of the bot."""

    processed_releases: List[str] = Field(default_factory=list)


class Settings(BaseSettings):
    """Represents the application settings, loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    reddit_client_id: str
    reddit_client_secret: str
    reddit_user_agent: str
    reddit_username: str
    reddit_password: str
    github_token: str
    encryption_key: str
