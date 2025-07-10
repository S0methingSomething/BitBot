from __future__ import annotations

import logging
from pathlib import Path
from typing import ClassVar

import yaml
from pydantic import BaseModel, Field, ValidationError


class GitHubConfig(BaseModel):
    source_repo: str = Field(..., alias="sourceRepo")
    bot_repo: str = Field(..., alias="botRepo")
    asset_file_name: str = Field(..., alias="assetFileName")


class RedditConfig(BaseModel):
    subreddit: str
    creator: str
    bot_name: str = Field(..., alias="botName")


class OutdatedPostHandlingConfig(BaseModel):
    mode: str


class MessagesConfig(BaseModel):
    release_title: str = Field(..., alias="releaseTitle")
    release_description: str = Field(..., alias="releaseDescription")
    post_title: str = Field(..., alias="postTitle")
    status_line: str = Field(..., alias="statusLine")


class FeedbackConfig(BaseModel):
    status_line_regex: str = Field(..., alias="statusLineRegex")
    labels: dict[str, str]
    working_keywords: list[str] = Field(..., alias="workingKeywords")
    not_working_keywords: list[str] = Field(..., alias="notWorkingKeywords")
    min_feedback_count: int = Field(..., alias="minFeedbackCount")


class SkipContentConfig(BaseModel):
    start_tag: str = Field(..., alias="startTag")
    end_tag: str = Field(..., alias="endTag")


class TemplatesConfig(BaseModel):
    post: str
    outdated: str
    inject: str


class TimingConfig(BaseModel):
    first_check: int = Field(..., alias="firstCheck")
    max_wait: int = Field(..., alias="maxWait")
    increase_by: int = Field(..., alias="increaseBy")


class Config(BaseModel):
    github: GitHubConfig
    reddit: RedditConfig
    outdated_post_handling: OutdatedPostHandlingConfig = Field(
        ..., alias="outdatedPostHandling"
    )
    messages: MessagesConfig
    feedback: FeedbackConfig
    skip_content: SkipContentConfig = Field(..., alias="skipContent")
    templates: TemplatesConfig
    timing: TimingConfig

    _config: ClassVar[Config | None] = None

    @classmethod
    def get_instance(cls) -> Config:
        if cls._config is None:
            raise RuntimeError("Config has not been loaded.")
        return cls._config

    @classmethod
    def load(cls, config_path: str | Path = "config.yaml") -> Config:
        config_p = Path(config_path)
        if not config_p.exists():
            logging.critical(f"Configuration file not found at: {config_p}")
            raise FileNotFoundError(f"Config file not found: {config_p}")

        with config_p.open("r", encoding="utf-8") as f:
            raw_config = yaml.safe_load(f)

        try:
            config = cls.model_validate(raw_config)
            cls._config = config
            logging.info("Configuration loaded and validated successfully.")
            return config
        except ValidationError as e:
            logging.critical(f"Configuration validation failed:\n{e}")
            raise
