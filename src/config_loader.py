"""Centralized configuration management for BitBot."""

from pathlib import Path
from typing import Any

import toml

from models.config import Config


def load_config(config_path: str = "config.toml") -> Config:
    """Load and validate configuration using Pydantic."""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    config_data = toml.loads(path.read_text())

    # Fix the feedback section structure if needed
    if "feedback" in config_data:
        feedback = config_data["feedback"]
        # If keywords are nested in labels, move them up to the main feedback section
        if "labels" in feedback:
            labels = feedback["labels"]
            if "workingKeywords" in labels:
                feedback["workingKeywords"] = labels.pop("workingKeywords")
            if "notWorkingKeywords" in labels:
                feedback["notWorkingKeywords"] = labels.pop("notWorkingKeywords")
            if "minFeedbackCount" in labels:
                feedback["minFeedbackCount"] = labels.pop("minFeedbackCount")

    return Config(**config_data)


def get_config_value(config: Config, path: str) -> Any:
    """Get a configuration value using dot notation path."""
    keys = path.split(".")
    value = config
    for key in keys:
        if hasattr(value, key):
            value = getattr(value, key)
        else:
            raise AttributeError(f"Config path '{path}' not found")
    return value
