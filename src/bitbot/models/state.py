"""Pydantic models for the application's state files."""

from datetime import datetime

from pydantic import BaseModel, Field, RootModel


class BotState(BaseModel):
    """Represents the state of the bot's interaction with Reddit."""

    active_post_id: str | None = Field(None, alias="activePostId")
    last_major_post_timestamp: datetime | None = Field(None, alias="lastMajorPostTimestamp")
    last_check_timestamp: datetime | None = Field(None, alias="lastCheckTimestamp")
    current_interval_seconds: int | None = Field(None, alias="currentIntervalSeconds")
    last_comment_count: int | None = Field(None, alias="lastCommentCount")


class ReleaseState(RootModel[list[int]]):
    """Represents the state of processed releases, which is a list of IDs."""

    root: list[int] = Field(default_factory=list)

    def __contains__(self, item: int) -> bool:
        """Check if a release ID is in the state."""
        return item in self.root

    def append(self, item: int) -> None:
        """Add a release ID to the state."""
        self.root.append(item)
