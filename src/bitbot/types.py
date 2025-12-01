"""Type definitions for BitBot data structures."""

from typing import TypedDict


class ReleaseInfo(TypedDict):
    """Basic release information."""

    display_name: str
    version: str
    url: str


class UpdatedReleaseInfo(TypedDict):
    """Updated release with old and new versions."""

    new: ReleaseInfo
    old: str


class RemovedReleaseInfo(TypedDict):
    """Removed release information."""

    display_name: str
    version: str


class Changelog(TypedDict):
    """Changelog with added, updated, and removed releases."""

    added: dict[str, ReleaseInfo]
    updated: dict[str, UpdatedReleaseInfo]
    removed: dict[str, RemovedReleaseInfo]


class LatestRelease(TypedDict):
    """Latest release details."""

    version: str
    download_url: str


class LatestReleaseWithDate(TypedDict, total=False):
    """Latest release details with optional published date."""

    version: str
    download_url: str
    published_at: str


class PreviousRelease(TypedDict):
    """Previous release in history."""

    version: str
    download_url: str


class AppReleaseData(TypedDict):
    """Release data for a single app."""

    display_name: str
    latest_release: LatestRelease | LatestReleaseWithDate
    previous_releases: list[PreviousRelease]


# Type alias for the full releases data structure
ReleasesData = dict[str, AppReleaseData]
