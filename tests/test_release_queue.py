"""Tests for release queue management."""

import json

from bitbot.core.release_queue import (
    add_release,
    clear_pending_releases,
    load_pending_releases,
    save_pending_releases,
)
from bitbot.models import PendingRelease


def test_load_pending_releases_success(tmp_path, monkeypatch):
    """Test load_pending_releases returns Ok with valid data."""
    queue_file = tmp_path / "release_queue.json"
    queue_file.write_text(
        json.dumps(
            [
                {
                    "release_id": 123,
                    "tag": "v1.0.0",
                    "app_id": "test_app",
                    "display_name": "Test App",
                    "version": "1.0.0",
                    "asset_name": None,
                }
            ]
        )
    )
    monkeypatch.setattr("bitbot.paths.RELEASE_QUEUE_FILE", queue_file)

    result = load_pending_releases()

    assert result.is_ok()
    releases = result.unwrap()
    assert len(releases) == 1
    assert releases[0].app_id == "test_app"


def test_load_pending_releases_missing_file(tmp_path, monkeypatch):
    """Test load_pending_releases returns empty list when file missing."""
    queue_file = tmp_path / "nonexistent.json"
    monkeypatch.setattr("bitbot.paths.RELEASE_QUEUE_FILE", queue_file)

    result = load_pending_releases()

    assert result.is_ok()
    assert result.unwrap() == []


def test_save_pending_releases_success(tmp_path, monkeypatch):
    """Test save_pending_releases writes data correctly."""
    queue_file = tmp_path / "release_queue.json"
    monkeypatch.setattr("bitbot.paths.RELEASE_QUEUE_FILE", queue_file)

    releases = [
        PendingRelease(
            release_id=123,
            tag="v1.0.0",
            app_id="test_app",
            display_name="Test App",
            version="1.0.0",
        )
    ]

    result = save_pending_releases(releases)

    assert result.is_ok()
    assert queue_file.exists()
    data = json.loads(queue_file.read_text())
    assert len(data) == 1
    assert data[0]["app_id"] == "test_app"


def test_add_release_success(tmp_path, monkeypatch):
    """Test add_release appends to existing releases."""
    queue_file = tmp_path / "release_queue.json"
    queue_file.write_text("[]")
    monkeypatch.setattr("bitbot.paths.RELEASE_QUEUE_FILE", queue_file)

    release = PendingRelease(
        release_id=123, tag="v1.0.0", app_id="test_app", display_name="Test App", version="1.0.0"
    )

    result = add_release(release)

    assert result.is_ok()
    data = json.loads(queue_file.read_text())
    assert len(data) == 1


def test_clear_pending_releases_success(tmp_path, monkeypatch):
    """Test clear_pending_releases empties the queue."""
    queue_file = tmp_path / "release_queue.json"
    queue_file.write_text('[{"release_id": 123}]')
    monkeypatch.setattr("bitbot.paths.RELEASE_QUEUE_FILE", queue_file)

    result = clear_pending_releases()

    assert result.is_ok()
    data = json.loads(queue_file.read_text())
    assert data == []
