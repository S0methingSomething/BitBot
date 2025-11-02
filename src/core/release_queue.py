"""Release queue management for BitBot."""

import json
from pathlib import Path

import deal
from beartype import beartype
from pydantic import ValidationError

import paths
from core.errors import ReleaseQueueError
from core.result import Err, Ok, Result
from models import PendingRelease


@beartype
def load_pending_releases() -> Result[list[PendingRelease], ReleaseQueueError]:
    """Load pending releases from queue file."""
    try:
        queue_file = Path(paths.RELEASES_JSON_FILE)
        if not queue_file.exists():
            return Ok([])

        with queue_file.open() as f:
            data = json.load(f)

        if not isinstance(data, list):
            return Err(ReleaseQueueError("Queue file must contain a list"))

        releases = [PendingRelease(**item) for item in data]
        return Ok(releases)

    except json.JSONDecodeError as e:
        return Err(ReleaseQueueError(f"Invalid JSON in queue file: {e}"))
    except ValidationError as e:
        return Err(ReleaseQueueError(f"Invalid release data: {e}"))
    except OSError as e:
        return Err(ReleaseQueueError(f"Failed to load queue: {e}"))


@deal.pre(
    lambda releases: isinstance(releases, list),
    message="Releases must be a list of PendingRelease objects",
)
@beartype
def save_pending_releases(releases: list[PendingRelease]) -> Result[None, ReleaseQueueError]:
    """Save pending releases to queue file."""
    try:
        queue_file = Path(paths.RELEASES_JSON_FILE)
        queue_file.parent.mkdir(parents=True, exist_ok=True)

        data = [release.model_dump() for release in releases]

        with queue_file.open("w") as f:
            json.dump(data, f, indent=2)

        return Ok(None)

    except Exception as e:
        return Err(ReleaseQueueError(f"Failed to save queue: {e}"))


@deal.pre(
    lambda release: hasattr(release, "release_id"),
    message="Release must be a PendingRelease object",
)
@beartype
def add_release(release: PendingRelease) -> Result[None, ReleaseQueueError]:
    """Add a release to the queue."""
    load_result = load_pending_releases()
    if load_result.is_err():
        return Err(load_result.error)

    releases = load_result.unwrap()
    releases.append(release)

    save_result = save_pending_releases(releases)
    if save_result.is_err():
        return Err(save_result.error)
    return Ok(None)


@beartype
def clear_pending_releases() -> Result[None, ReleaseQueueError]:
    """Clear all pending releases from queue."""
    save_result = save_pending_releases([])
    if save_result.is_err():
        return Err(save_result.error)
    return Ok(None)
