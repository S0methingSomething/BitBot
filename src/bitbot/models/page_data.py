"""Pydantic models for the web landing page."""

from pydantic import BaseModel, HttpUrl


class WebRelease(BaseModel):
    """Represents a single release entry on the landing page."""

    version: str
    published_at: str
    download_url: HttpUrl


class AppData(BaseModel):
    """Represents all the data for a single app on the landing page."""

    display_name: str
    latest_release: WebRelease | None = None
    previous_releases: list[WebRelease] = []


class PageData(BaseModel):
    """Represents all the data needed to render the landing page."""

    apps: dict[str, AppData]
