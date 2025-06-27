from typing import Any

from pydantic import BaseModel, Field


# Define sub-models for clarity and strictness
class GitHubConfig(BaseModel):
    source_repo: str = Field(alias="sourceRepo")
    bot_repo: str = Field(alias="botRepo")
    asset_file_name: str = Field(alias="assetFileName")


class RedditConfig(BaseModel):
    subreddit: str
    creator: str
    bot_name: str = Field(alias="botName")
    state_issue_number: int


class FeedbackConfig(BaseModel):
    status_line_regex: str = Field(alias="statusLineRegex")
    labels: dict[str, str]
    working_keywords: list[str] = Field(alias="workingKeywords")
    not_working_keywords: list[str] = Field(alias="notWorkingKeywords")
    min_feedback_count: int = Field(alias="minFeedbackCount", gt=0)


class TimingConfig(BaseModel):
    first_check: int = Field(alias="firstCheck", gt=0)
    max_wait: int = Field(alias="maxWait", gt=0)
    increase_by: int = Field(alias="increaseBy", gt=0)


class Config(BaseModel):
    """The main application configuration model."""

    github: GitHubConfig
    reddit: RedditConfig
    outdated_post_handling: dict[str, Any] = Field(alias="outdatedPostHandling")
    messages: dict[str, str]
    feedback: FeedbackConfig
    timing: TimingConfig
    skip_content: dict[str, str] = Field(alias="skipContent")
    templates: dict[str, str]


class BotState(BaseModel):
    """A model for the bot's persistent state."""

    active_post_id: str | None = Field(alias="activePostId", default=None)
    last_check_timestamp: str = Field(alias="lastCheckTimestamp")
    current_interval_seconds: int = Field(alias="currentIntervalSeconds")
    last_comment_count: int = Field(alias="lastCommentCount")
