"""Pydantic models for the application's configuration."""

from pydantic import BaseModel, Field, HttpUrl


class GitHubConfig(BaseModel):
    """Configuration for GitHub repositories."""

    token: str | None = None
    source_repo: str = Field(..., alias="sourceRepo")
    bot_repo: str = Field(..., alias="botRepo")
    asset_file_name: str = Field(..., alias="assetFileName")
    pages_url: HttpUrl = Field(..., alias="pages_url")


class RedditTemplates(BaseModel):
    """Paths to Reddit templates."""

    post: str
    outdated_post: str
    inject_banner: str
    custom_landing: str | None = None


class RedditFormatsTitles(BaseModel):
    """Formats for Reddit post titles."""

    added_only: str
    updated_only_single: str
    updated_only_multi: str
    mixed_single_update: str
    mixed_multi_update: str
    generic: str


class RedditFormatsChangelog(BaseModel):
    """Formats for the changelog in Reddit posts."""

    added_landing: str
    updated_landing: str
    removed_landing: str
    added_direct: str
    updated_direct: str
    removed_direct: str


class RedditFormatsTable(BaseModel):
    """Formats for the table in Reddit posts."""

    header: str
    divider: str
    line: str


class RedditFormats(BaseModel):
    """All Reddit format strings."""

    titles: RedditFormatsTitles
    changelog: RedditFormatsChangelog
    table: RedditFormatsTable


class RedditConfig(BaseModel):
    """Configuration for Reddit interaction."""

    subreddit: str
    bot_name: str = Field(..., alias="botName")
    creator: str
    post_mode: str = Field(..., alias="postMode")
    post_manually: bool = Field(..., alias="post_manually")
    post_frequency_days: int = Field(..., alias="post_frequency_days")
    templates: RedditTemplates
    formats: RedditFormats


class SafetyConfig(BaseModel):
    """Safety features configuration."""

    max_outbound_links_warn: int


class OutdatedPostHandlingConfig(BaseModel):
    """Configuration for handling outdated posts."""

    mode: str


class MessagesConfig(BaseModel):
    """Text formats for GitHub releases."""

    release_title: str = Field(..., alias="releaseTitle")
    release_description: str = Field(..., alias="releaseDescription")


class SkipContentConfig(BaseModel):
    """Tags for content to be skipped."""

    start_tag: str = Field(..., alias="startTag")
    end_tag: str = Field(..., alias="endTag")


class FeedbackLabels(BaseModel):
    """Labels for feedback status."""

    working: str
    broken: str
    unknown: str


class FeedbackConfig(BaseModel):
    """Configuration for analyzing Reddit comments."""

    status_line_format: str = Field(..., alias="statusLineFormat")
    status_line_regex: str = Field(..., alias="statusLineRegex")
    labels: FeedbackLabels
    working_keywords: list[str] = Field(..., alias="workingKeywords")
    not_working_keywords: list[str] = Field(..., alias="notWorkingKeywords")
    min_feedback_count: int = Field(..., alias="minFeedbackCount")


class TimingConfig(BaseModel):
    """Configuration for adaptive polling interval."""

    first_check: int = Field(..., alias="firstCheck")
    max_wait: int = Field(..., alias="maxWait")
    increase_by: int = Field(..., alias="increaseBy")


class ParsingConfig(BaseModel):
    """Keys for parsing release descriptions."""

    app_key: str
    version_key: str
    asset_name_key: str


class AppConfig(BaseModel):
    """Configuration for a single app."""

    id: str
    display_name: str = Field(..., alias="displayName")


class Config(BaseModel):
    """The root configuration model."""

    github: GitHubConfig
    reddit: RedditConfig
    safety: SafetyConfig
    outdated_post_handling: OutdatedPostHandlingConfig = Field(..., alias="outdatedPostHandling")
    messages: MessagesConfig
    skip_content: SkipContentConfig = Field(..., alias="skipContent")
    feedback: FeedbackConfig
    timing: TimingConfig
    parsing: ParsingConfig
    apps: list[AppConfig]
