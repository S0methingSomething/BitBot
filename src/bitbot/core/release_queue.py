"""Release queue management for BitBot."""

import json
from pathlib import Path

from beartype import beartype
from pydantic import ValidationError

from bitbot import paths
from bitbot.core.errors import ReleaseQueueError
from bitbot.core.result import Err, Ok, Result
from bitbot.models import PendingRelease


@beartype
def load_pending_releases() -> Result[list[PendingRelease], ReleaseQueueError]:
    """Load pending releases from queue file."""
    try:
        queue_file = Path(paths.RELEASE_QUEUE_FILE)
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


@beartype
def save_pending_releases(releases: list[PendingRelease]) -> Result[None, ReleaseQueueError]:
    """Save pending releases to queue file."""
    try:
        queue_file = Path(paths.RELEASE_QUEUE_FILE)
        queue_file.parent.mkdir(parents=True, exist_ok=True)

        data = [release.model_dump() for release in releases]

        temp_file = queue_file.with_suffix(".tmp")
        with temp_file.open("w") as f:
            json.dump(data, f, indent=2)
        temp_file.replace(queue_file)

        return Ok(None)

    except (OSError, ValueError) as e:
        return Err(ReleaseQueueError(f"Failed to save queue: {e}"))


@beartype
def add_release(release: PendingRelease) -> Result[None, ReleaseQueueError]:
    """Add a release to the queue."""
    load_result = load_pending_releases()
    if load_result.is_err():
        return Err(load_result.error)

    releases = load_result.unwrap()

    # Check for duplicate release_id
    if any(r.release_id == release.release_id for r in releases):
        return Err(ReleaseQueueError(f"Release {release.release_id} already in queue"))

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
