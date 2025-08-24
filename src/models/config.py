from pydantic import BaseModel, Field


class AuthConfig(BaseModel):
    mode: str = Field(default="environment", alias="mode")
    auto_save: bool = Field(default=False, alias="auto_save")
    auto_load: bool = Field(default=False, alias="auto_load")


class GitHubPagesConfig(BaseModel):
    owner: str = Field(alias="owner")
    repo: str = Field(alias="repo")
    branch: str = Field(default="gh-pages", alias="branch")
    token: str | None = Field(default=None, alias="token")


class CloudflarePagesConfig(BaseModel):
    account_id: str = Field(alias="accountId")
    project_name: str = Field(alias="projectName")
    api_token: str | None = Field(default=None, alias="apiToken")
    branch: str = Field(default="main", alias="branch")


class DeploymentProvidersConfig(BaseModel):
    github: GitHubPagesConfig | None = Field(default=None, alias="github")
    cloudflare: CloudflarePagesConfig | None = Field(default=None, alias="cloudflare")


class DeploymentConfig(BaseModel):
    providers: list[str] = Field(default=[], alias="providers")
    github: GitHubPagesConfig | None = Field(default=None, alias="github")
    cloudflare: CloudflarePagesConfig | None = Field(default=None, alias="cloudflare")


class GitHubConfig(BaseModel):
    source_repo: str = Field(alias="sourceRepo")
    bot_repo: str = Field(alias="botRepo")
    asset_file_name: str = Field(alias="assetFileName")
    pages_url: str | None = Field(default=None, alias="pages_url")


class RedditTemplatesConfig(BaseModel):
    post: str = Field(alias="post")
    outdated_post: str = Field(alias="outdated_post")
    inject_banner: str = Field(alias="inject_banner")
    custom_landing: str | None = Field(default=None, alias="custom_landing")


class RedditTitlesConfig(BaseModel):
    added_only: str = Field(alias="added_only")
    updated_only_single: str = Field(alias="updated_only_single")
    updated_only_multi: str = Field(alias="updated_only_multi")
    mixed_single_update: str = Field(alias="mixed_single_update")
    mixed_multi_update: str = Field(alias="mixed_multi_update")
    generic: str = Field(alias="generic")


class RedditChangelogConfig(BaseModel):
    added_landing: str = Field(alias="added_landing")
    updated_landing: str = Field(alias="updated_landing")
    removed_landing: str = Field(alias="removed_landing")
    added_direct: str = Field(alias="added_direct")
    updated_direct: str = Field(alias="updated_direct")
    removed_direct: str = Field(alias="removed_direct")


class RedditTableConfig(BaseModel):
    header: str = Field(alias="header")
    divider: str = Field(alias="divider")
    line: str = Field(alias="line")


class RedditFormatsConfig(BaseModel):
    titles: RedditTitlesConfig
    changelog: RedditChangelogConfig
    table: RedditTableConfig


class SafetyConfig(BaseModel):
    max_outbound_links_warn: int = Field(alias="max_outbound_links_warn")


class OutdatedPostHandlingConfig(BaseModel):
    mode: str = Field(alias="mode")


class MessagesConfig(BaseModel):
    release_title: str = Field(alias="releaseTitle")
    release_description: str = Field(alias="releaseDescription")


class SkipContentConfig(BaseModel):
    start_tag: str = Field(alias="startTag")
    end_tag: str = Field(alias="endTag")


class FeedbackLabelsConfig(BaseModel):
    working: str = Field(alias="working")
    broken: str = Field(alias="broken")
    unknown: str = Field(alias="unknown")


class FeedbackConfig(BaseModel):
    status_line_format: str = Field(alias="statusLineFormat")
    status_line_regex: str = Field(alias="statusLineRegex")
    labels: FeedbackLabelsConfig
    working_keywords: list[str] = Field(alias="workingKeywords")
    not_working_keywords: list[str] = Field(alias="notWorkingKeywords")
    min_feedback_count: int = Field(alias="minFeedbackCount")


class TimingConfig(BaseModel):
    first_check: int = Field(alias="firstCheck")
    max_wait: int = Field(alias="maxWait")
    increase_by: int = Field(alias="increaseBy")


class ParsingConfig(BaseModel):
    app_key: str = Field(alias="app_key")
    version_key: str = Field(alias="version_key")
    asset_name_key: str = Field(alias="asset_name_key")


class App(BaseModel):
    id: str = Field(alias="id")
    display_name: str = Field(alias="displayName")


class RedditConfig(BaseModel):
    subreddit: str = Field(alias="subreddit")
    bot_name: str = Field(alias="botName")
    creator: str = Field(alias="creator")
    post_mode: str = Field(alias="postMode")
    post_manually: bool = Field(alias="post_manually")
    templates: RedditTemplatesConfig
    formats: RedditFormatsConfig


class DigestConfig(BaseModel):
    enabled: bool = Field(default=False, alias="enabled")
    cycle_days: int = Field(default=7, alias="cycleDays")


class Config(BaseModel):
    auth: AuthConfig = Field(default_factory=AuthConfig)
    github: GitHubConfig
    reddit: RedditConfig
    safety: SafetyConfig
    outdated_post_handling: OutdatedPostHandlingConfig = Field(
        alias="outdatedPostHandling"
    )
    messages: MessagesConfig
    skip_content: SkipContentConfig = Field(alias="skipContent")
    feedback: FeedbackConfig
    timing: TimingConfig
    parsing: ParsingConfig
    digest: DigestConfig = Field(default_factory=DigestConfig)
    deployment: DeploymentConfig | None = Field(default=None, alias="deployment")
    apps: list[App]
