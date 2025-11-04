"""Pydantic models for BitBot runtime data structures."""

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BotState(BaseModel):
    """Bot state structure."""

    model_config = ConfigDict(populate_by_name=True)

    # Maps app_id -> version string
    online: dict[str, str] = Field(default_factory=dict)
    offline: dict[str, str] = Field(default_factory=dict)
    active_post_id: str | None = Field(default=None, alias="activePostId")
    last_check_timestamp: str | None = Field(default=None, alias="lastCheckTimestamp")
    current_interval_seconds: int | None = Field(default=None, alias="currentIntervalSeconds")
    all_post_ids: list[str] = Field(default_factory=list, alias="allPostIds")

    @field_validator("current_interval_seconds")
    @classmethod
    def validate_interval(cls, v: int | None) -> int | None:
        """Validate interval is positive."""
        if v is not None and v <= 0:
            msg = "current_interval_seconds must be positive"
            raise ValueError(msg)
        return v


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
    def validate_release_id(cls, v: int) -> int:
        """Validate release_id is positive."""
        if v <= 0:
            msg = "release_id must be positive"
            raise ValueError(msg)
        return v

    @field_validator("tag", "app_id", "display_name", "version")
    @classmethod
    def validate_non_empty(cls, v: str) -> str:
        """Validate string fields are non-empty."""
        if not v.strip():
            msg = "Field cannot be empty"
            raise ValueError(msg)
        return v
