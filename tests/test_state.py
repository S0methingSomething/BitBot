"""Tests for state management."""

import json
from pathlib import Path

import pytest

from bitbot.core.state import load_global_state, save_global_state
from bitbot.models import GlobalState


def test_save_global_state_atomic(tmp_path, monkeypatch):
    """Test save_global_state uses atomic writes."""
    state_file = tmp_path / "bot_state.json"
    monkeypatch.setattr("bitbot.paths.BOT_STATE_FILE", state_file)
    
    state = GlobalState(offline={"app1": "1.0.0"})
    result = save_global_state(state)
    
    assert result.is_ok()
    assert state_file.exists()
    
    # Verify content
    data = json.loads(state_file.read_text())
    assert data["offline"]["app1"] == "1.0.0"


def test_load_global_state_missing_file(tmp_path, monkeypatch):
    """Test load_global_state returns empty state on missing file."""
    state_file = tmp_path / "nonexistent.json"
    monkeypatch.setattr("bitbot.paths.BOT_STATE_FILE", state_file)
    
    result = load_global_state()
    
    assert result.is_ok()
    state = result.unwrap()
    assert state.offline == {}


def test_load_global_state_invalid_json(tmp_path, monkeypatch):
    """Test load_global_state returns Err on invalid JSON."""
    state_file = tmp_path / "invalid.json"
    state_file.write_text("not valid json{")
    monkeypatch.setattr("bitbot.paths.BOT_STATE_FILE", state_file)
    
    result = load_global_state()
    
    assert result.is_err()
    assert "Invalid JSON" in str(result.unwrap_err())


def test_save_load_roundtrip(tmp_path, monkeypatch):
    """Test save/load roundtrip preserves state."""
    state_file = tmp_path / "bot_state.json"
    monkeypatch.setattr("bitbot.paths.BOT_STATE_FILE", state_file)
    
    original = GlobalState(offline={"app1": "1.0.0", "app2": "2.0.0"})
    
    save_result = save_global_state(original)
    assert save_result.is_ok()
    
    load_result = load_global_state()
    assert load_result.is_ok()
    
    loaded = load_result.unwrap()
    assert loaded.offline == original.offline
