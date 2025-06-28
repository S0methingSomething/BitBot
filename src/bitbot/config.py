from typing import Any

from pydantic import BaseModel, Field, field_validator


# Define sub-models for clarity and strictness
class GitHubConfig(BaseModel):
    source_repo: str = Field(alias="sourceRepo")
    bot_repo: str = Field(alias="botRepo")
    asset_file_name: str = Field(alias="assetFileName")


class RedditConfig(BaseModel):
    subreddit: str
    creator: str
    bot_name: str = Field(alias="botName")


class FeedbackConfig(BaseModel):
    status_line_regex: str = Field(alias="statusLineRegex")
    labels: dict[str, str]
    working_keywords: list[str] = Field(alias="workingKeywords")
    not_working_keywords: list[str] = Field(alias="notWorkingKeywords")
    min_feedback_count: int = Field(alias="minFeedbackCount", gt=0)


class Config(BaseModel):
    """The main application configuration model."""

    github: GitHubConfig
    reddit: RedditConfig
    outdated_post_handling: dict[str, Any] = Field(alias="outdatedPostHandling")
    messages: dict[str, str]
    feedback: FeedbackConfig
    skip_content: dict[str, str] = Field(alias="skipContent")
    templates: dict[str, str]

    @field_validator("messages")
    def validate_templates(cls, messages: dict[str, str]) -> dict[str, str]:
        """
        Validates that the message templates contain expected placeholders.
        This prevents runtime errors from misconfigured templates.
        """
        required_placeholders = {
            "releaseTitle": ["{{asset_name}}", "{{version}}"],
            "postTitle": ["{{asset_name}}", "{{version}}"],
            "statusLine": ["{{status}}"],
        }
        for key, placeholders in required_placeholders.items():
            if key in messages:
                for placeholder in placeholders:
                    if placeholder not in messages[key]:
                        raise ValueError(
                            f"Template '{key}' is missing placeholder: {placeholder}"
                        )
        return messages
