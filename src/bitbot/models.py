"""Pydantic models for BitBot runtime data structures."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class BotState(BaseModel):
    """Bot state structure."""

    model_config = ConfigDict(populate_by_name=True)

    # Any: Dynamic state tracking for apps, structure varies by app
    online: dict[str, Any] = Field(default_factory=dict)
    offline: dict[str, Any] = Field(default_factory=dict)
    active_post_id: str | None = Field(default=None, alias="activePostId")
    last_check_timestamp: str | None = Field(default=None, alias="lastCheckTimestamp")
    current_interval_seconds: int | None = Field(default=None, alias="currentIntervalSeconds")
    all_post_ids: list[str] = Field(default_factory=list, alias="allPostIds")


class PendingRelease(BaseModel):
    """Pending release to process."""

    release_id: int
    tag: str
    app_id: str
    display_name: str
    version: str
    asset_name: str | None = None
