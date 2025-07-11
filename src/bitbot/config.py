from __future__ import annotations

import logging
import os
import tomllib
from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel, Field, model_validator

from .messages import ExitMessages
from .utils import log_and_exit

# --- Constants ---
TEMPLATES_DIR = Path(__file__).parent / "templates"
CREDENTIALS_PATH = Path("credentials.toml")


# --- Pydantic Models for credentials.toml ---
class Credentials(BaseModel):
    github_token: str | None = Field(None, alias="GITHUB_TOKEN")
    reddit_client_id: str | None = Field(None, alias="REDDIT_CLIENT_ID")
    reddit_client_secret: str | None = Field(None, alias="REDDIT_CLIENT_SECRET")
    reddit_user_agent: str | None = Field(None, alias="REDDIT_USER_AGENT")
    reddit_username: str | None = Field(None, alias="REDDIT_USERNAME")
    reddit_password: str | None = Field(None, alias="REDDIT_PASSWORD")

    @classmethod
    def load(cls) -> "Credentials":
        """Loads credentials from environment variables, with an optional override
        from a `credentials.toml` file. Environment variables always take precedence.
        """
        toml_creds = {}
        if CREDENTIALS_PATH.exists():
            logging.info(f"Loading credentials from '{CREDENTIALS_PATH}'")
            with CREDENTIALS_PATH.open("rb") as f:
                toml_creds = tomllib.load(f)
        else:
            logging.info(f"'{CREDENTIALS_PATH}' not found, loading from environment variables.")

        # Load from environment, falling back to TOML, then to None
        return cls(
            github_token=os.environ.get("GITHUB_TOKEN") or toml_creds.get("GITHUB_TOKEN"),
            reddit_client_id=os.environ.get("REDDIT_CLIENT_ID") or toml_creds.get("REDDIT_CLIENT_ID"),
            reddit_client_secret=os.environ.get("REDDIT_CLIENT_SECRET") or toml_creds.get("REDDIT_CLIENT_SECRET"),
            reddit_user_agent=os.environ.get("REDDIT_USER_AGENT") or toml_creds.get("REDDIT_USER_AGENT"),
            reddit_username=os.environ.get("REDDIT_USERNAME") or toml_creds.get("REDDIT_USERNAME"),
            reddit_password=os.environ.get("REDDIT_PASSWORD") or toml_creds.get("REDDIT_PASSWORD"),
        )


# --- Pydantic Models for config.toml ---
class GitHubConfig(BaseModel):
    source_repo: str = Field(..., alias="sourceRepo")
    bot_repo: str = Field(..., alias="botRepo")
    asset_file_name: str = Field(..., alias="assetFileName")


class RedditConfig(BaseModel):
    subreddit: str
    template_file: Path = Field(..., alias="templateFile")
    outdated_template_file: Path = Field(..., alias="outdatedTemplateFile")
    post_title: str = Field(..., alias="postTitle")
    bot_name: str = Field(..., alias="botName")
    creator: str


class OutdatedPostHandlingConfig(BaseModel):
    mode: str
    inject_template_file: Path = Field(..., alias="injectTemplateFile")


class MessagesConfig(BaseModel):
    release_title: str = Field(..., alias="releaseTitle")
    release_description: str = Field(..., alias="releaseDescription")


class SkipContentConfig(BaseModel):
    start_tag: str = Field(..., alias="startTag")
    end_tag: str = Field(..., alias="endTag")


class FeedbackLabelsConfig(BaseModel):
    working: str
    broken: str
    unknown: str


class FeedbackConfig(BaseModel):
    status_line_format: str = Field(..., alias="statusLineFormat")
    status_line_regex: str = Field(..., alias="statusLineRegex")
    labels: FeedbackLabelsConfig
    working_keywords: list[str] = Field(..., alias="workingKeywords")
    not_working_keywords: list[str] = Field(..., alias="notWorkingKeywords")
    min_feedback_count: int = Field(..., alias="minFeedbackCount")


class TimingConfig(BaseModel):
    first_check: int = Field(..., alias="firstCheck")
    max_wait: int = Field(..., alias="maxWait")
    increase_by: int = Field(..., alias="increaseBy")


class Config(BaseModel):
    github: GitHubConfig
    reddit: RedditConfig
    outdated_post_handling: OutdatedPostHandlingConfig = Field(..., alias="outdatedPostHandling")
    messages: MessagesConfig
    skip_content: SkipContentConfig = Field(..., alias="skipContent")
    feedback: FeedbackConfig
    timing: TimingConfig

    _config: ClassVar[Config | None] = None

    @model_validator(mode="after")
    def resolve_template_paths(self) -> "Config":
        """Prepend the templates directory path to template file names."""
        self.reddit.template_file = TEMPLATES_DIR / self.reddit.template_file.name
        self.reddit.outdated_template_file = TEMPLATES_DIR / self.reddit.outdated_template_file.name
        self.outdated_post_handling.inject_template_file = (
            TEMPLATES_DIR / self.outdated_post_handling.inject_template_file.name
        )
        return self

    @classmethod
    def get_instance(cls) -> Config:
        if cls._config is None:
            raise RuntimeError("Config has not been loaded.")
        return cls._config

    @classmethod
    def load(cls, config_path: str | Path = "config.toml") -> Config:
        config_p = Path(config_path)
        if not config_p.exists():
            log_and_exit(ExitMessages.CONFIG_NOT_FOUND.format(path=config_p))

        with config_p.open("rb") as f:
            raw_config = tomllib.load(f)

        try:
            config = cls.model_validate(raw_config)
            cls._config = config
            logging.info("Configuration loaded and validated successfully from TOML.")
            return config
        except Exception as e:
            log_and_exit(ExitMessages.CONFIG_VALIDATION_FAILED.format(error=e))
        return cls.model_validate(raw_config)  # Should be unreachable
