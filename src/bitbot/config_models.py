"""Typed configuration models."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class GitHubConfig(BaseModel):
    """GitHub configuration."""

    model_config = ConfigDict(populate_by_name=True)

    source_repo: str = Field(alias="sourceRepo")
    bot_repo: str = Field(alias="botRepo")
    asset_file_name: str = Field(alias="assetFileName")

    @field_validator("source_repo", "bot_repo")
    @classmethod
    def validate_repo_format(cls, v: str) -> str:
        """Validate repo is in owner/name format."""
        _ = cls
        if "/" not in v or v.count("/") != 1:
            msg = "Repository must be in 'owner/name' format"
            raise ValueError(msg)
        return v


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

    @field_validator("subreddit")
    @classmethod
    def validate_subreddit(cls, v: str) -> str:
        """Validate subreddit format."""
        _ = cls
        v = v.removeprefix("r/")
        if not v or "/" in v:
            msg = "Invalid subreddit name"
            raise ValueError(msg)
        return v

    @field_validator("post_mode")
    @classmethod
    def validate_post_mode(cls, v: str) -> str:
        """Validate post_mode is valid."""
        _ = cls
        valid_modes = {"rolling_update", "new_post"}
        if v not in valid_modes:
            msg = f"post_mode must be one of {valid_modes}"
            raise ValueError(msg)
        return v


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

    @field_validator("safety", "timing")
    @classmethod
    def validate_positive_ints(cls, v: dict[str, int]) -> dict[str, int]:
        """Validate numeric values are positive."""
        _ = cls
        for key, val in v.items():
            if val < 0:
                msg = f"{key} must be non-negative"
                raise ValueError(msg)
        return v
