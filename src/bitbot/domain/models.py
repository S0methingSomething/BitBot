# src/bitbot/domain/models.py
"""
Pydantic models representing the core data structures of the application.
"""

from pydantic import BaseModel, HttpUrl


class App(BaseModel):
    """Represents a single monitored application from the config."""

    id: str
    display_name: str


class GitHubRelease(BaseModel):
    """Represents a release fetched from the GitHub API."""

    tag_name: str
    html_url: HttpUrl
    body: str | None = None


class RedditPost(BaseModel):
    """Represents a post to be made or that exists on Reddit."""

    id: str | None = None
    title: str
    selftext: str
    url: HttpUrl | None = None
