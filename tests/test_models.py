"""Tests for Pydantic models."""

from bitbot.models import AccountState, GlobalState, PendingRelease


def test_global_state_validation():
    """Test GlobalState model validation."""
    state = GlobalState(offline={"app1": "1.0.0", "app2": "2.0.0"})
    assert state.offline["app1"] == "1.0.0"
    assert state.offline["app2"] == "2.0.0"


def test_global_state_empty():
    """Test GlobalState with empty offline dict."""
    state = GlobalState(offline={})
    assert state.offline == {}


def test_account_state_validation():
    """Test AccountState model validation."""
    state = AccountState(
        online={"app1": "1.0.0"}, all_post_ids=["abc123", "def456"], active_post_id="abc123"
    )
    assert state.online["app1"] == "1.0.0"
    assert len(state.all_post_ids) == 2
    assert state.active_post_id == "abc123"


def test_account_state_optional_fields():
    """Test AccountState with optional fields."""
    state = AccountState(online={})
    assert state.online == {}
    assert state.all_post_ids == []
    assert state.active_post_id is None


def test_pending_release_validation():
    """Test PendingRelease model validation."""
    release = PendingRelease(
        release_id=123, tag="v1.0.0", app_id="test_app", display_name="Test App", version="1.0.0"
    )
    assert release.release_id == 123
    assert release.tag == "v1.0.0"
    assert release.app_id == "test_app"
    assert release.display_name == "Test App"
    assert release.version == "1.0.0"
    assert release.asset_name is None


def test_pending_release_with_asset_name():
    """Test PendingRelease with optional asset_name."""
    release = PendingRelease(
        release_id=123,
        tag="v1.0.0",
        app_id="test_app",
        display_name="Test App",
        version="1.0.0",
        asset_name="custom_asset.json",
    )
    assert release.asset_name == "custom_asset.json"
