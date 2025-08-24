"""Simple credential management for BitBot - saves/loads from file for Codespaces."""

import os
from pathlib import Path

import toml

from logging_config import get_logger

logger = get_logger(__name__)

# Credential file location
CREDENTIALS_FILE = Path("credentials.toml")


def save_current_credentials() -> None:
    """Save current environment variables to file."""
    creds = {
        "github": {"token": os.environ.get("GITHUB_TOKEN", "")},
        "reddit": {
            "client_id": os.environ.get("REDDIT_CLIENT_ID", ""),
            "client_secret": os.environ.get("REDDIT_CLIENT_SECRET", ""),
            "username": os.environ.get("REDDIT_USERNAME", ""),
            "password": os.environ.get("REDDIT_PASSWORD", ""),
            "user_agent": os.environ.get("REDDIT_USER_AGENT", ""),
        },
    }

    # Only save if we have actual values
    has_github = bool(creds["github"]["token"])
    has_reddit = any(creds["reddit"].values())

    if has_github or has_reddit:
        try:
            with CREDENTIALS_FILE.open("w") as f:
                toml.dump(creds, f)
            CREDENTIALS_FILE.chmod(0o600)  # Secure permissions
            logger.info("Credentials saved to credentials.toml")
        except Exception as e:
            logger.error(f"Failed to save credentials: {e}")
    else:
        logger.info("No credentials found in environment variables to save")


def load_saved_credentials() -> None:
    """Load credentials from file into environment variables."""
    if not CREDENTIALS_FILE.exists():
        logger.info("No credentials.toml file found")
        return

    try:
        creds = toml.load(CREDENTIALS_FILE)

        # Load GitHub credentials
        github_creds = creds.get("github", {})
        if github_creds.get("token") and not os.environ.get("GITHUB_TOKEN"):
            os.environ["GITHUB_TOKEN"] = github_creds["token"]
            logger.info("Loaded GitHub token from credentials.toml")

        # Load Reddit credentials
        reddit_creds = creds.get("reddit", {})
        loaded_reddit = []
        reddit_env_mapping = {
            "client_id": "REDDIT_CLIENT_ID",
            "client_secret": "REDDIT_CLIENT_SECRET",
            "username": "REDDIT_USERNAME",
            "password": "REDDIT_PASSWORD",
            "user_agent": "REDDIT_USER_AGENT",
        }

        for key, env_var in reddit_env_mapping.items():
            if reddit_creds.get(key) and not os.environ.get(env_var):
                os.environ[env_var] = reddit_creds[key]
                loaded_reddit.append(key)

        if loaded_reddit:
            logger.info(
                f"Loaded Reddit credentials from credentials.toml: {', '.join(loaded_reddit)}"
            )

    except Exception as e:
        logger.error(f"Failed to load credentials: {e}")


def setup_credentials(auto_save: bool = False, auto_load: bool = False) -> None:
    """Auto-setup credentials based on configuration."""
    # Auto-load saved credentials if configured or environment variable set
    if auto_load or os.environ.get("BITBOT_LOAD_CREDS") == "1":
        load_saved_credentials()

    # Auto-save current credentials if configured or environment variable set
    if auto_save or os.environ.get("BITBOT_SAVE_CREDS") == "1":
        save_current_credentials()
