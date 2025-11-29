"""Pydantic models for BitBot runtime data structures."""

from beartype import beartype
from pydantic import BaseModel, ConfigDict, Field, field_validator


class GlobalState(BaseModel):
    """Global state tracking bot's GitHub repo versions."""

    model_config = ConfigDict(populate_by_name=True)

    # Maps app_id -> version string (what's in bot's repo)
    offline: dict[str, str] = Field(default_factory=dict)

    @field_validator("offline")
    @classmethod
    @beartype
    def validate_offline(cls, v: dict[str, str]) -> dict[str, str]:
        """Validate offline versions are non-empty."""
        for app_id, version in v.items():
            if not version.strip():
                msg = f"Version for {app_id} cannot be empty"
                raise ValueError(msg)
        return v


class AccountState(BaseModel):
    """Account-specific state tracking Reddit posts."""

    model_config = ConfigDict(populate_by_name=True)

    # Maps app_id -> version string (what's posted to this account)
    online: dict[str, str] = Field(default_factory=dict)
    active_post_id: str | None = Field(default=None, alias="activePostId")
    last_check_timestamp: str | None = Field(default=None, alias="lastCheckTimestamp")
    current_interval_seconds: int | None = Field(default=None, alias="currentIntervalSeconds")
    all_post_ids: list[str] = Field(default_factory=list, alias="allPostIds")

    @field_validator("online")
    @classmethod
    @beartype
    def validate_online(cls, v: dict[str, str]) -> dict[str, str]:
        """Validate online versions are non-empty."""
        for app_id, version in v.items():
            if not version.strip():
                msg = f"Version for {app_id} cannot be empty"
                raise ValueError(msg)
        return v

    @field_validator("current_interval_seconds")
    @classmethod
    @beartype
    def validate_interval(cls, v: int | None) -> int | None:
        """Validate interval is positive."""
        if v is not None and v <= 0:
            msg = "current_interval_seconds must be positive"
            raise ValueError(msg)
        return v


# Backward compatibility alias
BotState = AccountState


class PendingRelease(BaseModel):
    """Pending release to process."""

    release_id: int
    tag: str
    app_id: str
    display_name: str
    version: str
    asset_name: str | None = None

    @field_validator("release_id")
    @classmethod
    @beartype
    def validate_release_id(cls, v: int) -> int:
        """Validate release_id is positive."""
        if v <= 0:
            msg = "release_id must be positive"
            raise ValueError(msg)
        return v

    @field_validator("tag", "app_id", "display_name", "version")
    @classmethod
    @beartype
    def validate_non_empty(cls, v: str) -> str:
        """Validate string fields are non-empty."""
        if not v.strip():
            msg = "Field cannot be empty"
            raise ValueError(msg)
        return v
