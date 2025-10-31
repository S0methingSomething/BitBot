"""Pydantic models for BitBot configuration and state validation."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class GitHubConfig(BaseModel):  # type: ignore[misc]
    """GitHub configuration."""

    model_config = ConfigDict(populate_by_name=True)

    source_repo: str = Field(alias="sourceRepo")
    bot_repo: str = Field(alias="botRepo")
    asset_file_name: str = Field(default="MonetizationVars.json", alias="assetFileName")


class RedditTemplates(BaseModel):  # type: ignore[misc]
    """Reddit template configuration."""

    direct_link: str | None = None
    landing_page: str | None = None
    custom_landing: str | None = None
    outdated_banner: str | None = None


class RedditFormats(BaseModel):  # type: ignore[misc]
    """Reddit post format configuration."""

    titles: dict[str, str] = Field(default_factory=dict)
    changelog: dict[str, str] = Field(default_factory=dict)


class RedditRollingConfig(BaseModel):  # type: ignore[misc]
    """Rolling update mode configuration."""

    days_before_new_post: int = Field(default=7, alias="daysBeforeNewPost")
    update_existing: bool = Field(default=True, alias="updateExisting")


class RedditConfig(BaseModel):  # type: ignore[misc]
    """Reddit configuration."""

    model_config = ConfigDict(populate_by_name=True)

    subreddit: str
    post_mode: str = Field(alias="postMode")
    post_identifier: str = Field(default="[BitBot]", alias="postIdentifier")
    rolling: RedditRollingConfig = Field(default_factory=RedditRollingConfig)
    templates: RedditTemplates = Field(default_factory=RedditTemplates)
    formats: RedditFormats = Field(default_factory=RedditFormats)


class AppConfig(BaseModel):  # type: ignore[misc]
    """Individual app configuration."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    display_name: str = Field(alias="displayName")
    asset_name: str | None = Field(default=None, alias="assetName")


class Config(BaseModel):  # type: ignore[misc]
    """Main BitBot configuration."""

    github: GitHubConfig
    reddit: RedditConfig
    apps: list[AppConfig] = Field(default_factory=list)
    safety: dict[str, Any] = Field(default_factory=dict)
    timing: dict[str, Any] = Field(default_factory=dict)
    parsing: dict[str, Any] = Field(default_factory=dict)


class BotState(BaseModel):  # type: ignore[misc]
    """Bot state structure."""

    model_config = ConfigDict(populate_by_name=True)

    online: dict[str, Any] = Field(default_factory=dict)
    offline: dict[str, Any] = Field(default_factory=dict)
    active_post_id: str | None = Field(default=None, alias="activePostId")
    last_check_timestamp: str | None = Field(default=None, alias="lastCheckTimestamp")
    current_interval_seconds: int | None = Field(default=None, alias="currentIntervalSeconds")
