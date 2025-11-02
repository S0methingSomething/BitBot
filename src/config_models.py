"""Typed configuration models."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class GitHubConfig(BaseModel):
    """GitHub configuration."""

    model_config = ConfigDict(populate_by_name=True)

    source_repo: str = Field(alias="sourceRepo")
    bot_repo: str = Field(alias="botRepo")
    asset_file_name: str = Field(alias="assetFileName")


class RedditTemplates(BaseModel):
    """Reddit template paths."""

    post: str
    outdated_post: str = Field(alias="outdated_post")
    inject_banner: str = Field(alias="inject_banner")
    custom_landing: str | None = Field(default=None, alias="custom_landing")


class RedditFormats(BaseModel):
    """Reddit post formats."""

    changelog: dict[str, str]
    table: dict[str, str]


class RedditConfig(BaseModel):
    """Reddit configuration."""

    model_config = ConfigDict(populate_by_name=True)

    subreddit: str
    bot_name: str = Field(alias="botName")
    creator: str
    user_agent: str = Field(alias="userAgent")
    post_mode: str = Field(alias="postMode", default="rolling_update")
    download_mode: str = Field(alias="downloadMode", default="landing_page")
    post_manually: bool = Field(default=False)
    templates: RedditTemplates
    formats: RedditFormats


class Config(BaseModel):
    """Main configuration."""

    model_config = ConfigDict(populate_by_name=True)

    github: GitHubConfig
    reddit: RedditConfig
    outdated_post_handling: dict[str, str] = Field(
        default_factory=dict, alias="outdatedPostHandling"
    )
    feedback: dict[str, Any] = Field(default_factory=dict)
    safety: dict[str, int] = Field(default_factory=dict)
    skip_content: dict[str, str] = Field(default_factory=dict, alias="skipContent")
    apps: list[dict[str, str]] = Field(default_factory=list)
    parsing: dict[str, str] = Field(default_factory=dict)
    messages: dict[str, str] = Field(default_factory=dict)
    timing: dict[str, int] = Field(default_factory=dict)
