"""Pydantic models for the application's changelog."""

from pydantic import BaseModel


class ChangelogEntry(BaseModel):
    """Represents a single entry in the changelog."""

    app_id: str
    version: str
    asset_name: str


class Changelog(BaseModel):
    """Represents the full changelog for a set of releases."""

    added: list[ChangelogEntry] = []
    updated: list[ChangelogEntry] = []
    removed: list[ChangelogEntry] = []
