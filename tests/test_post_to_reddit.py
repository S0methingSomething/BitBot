import pytest
from hypothesis import given, strategies as st

from post_to_reddit import _generate_dynamic_title
from models.config import Config

# --- Test Data ---

MOCK_CONFIG = Config(
    github={
        "sourceRepo": "test/test",
        "botRepo": "test/test",
        "assetFileName": "test",
    },
    reddit={
        "subreddit": "test",
        "botName": "test",
        "creator": "test",
        "postMode": "landing_page",
        "post_manually": False,
        "templates": {
            "post": "test",
            "outdated_post": "test",
            "inject_banner": "test",
        },
        "formats": {
            "titles": {
                "added_only": "New Apps Added: {{added_list}}",
                "updated_only_single": "App Update: {{updated_list}}",
                "updated_only_multi": "App Updates: {{updated_list}}",
                "mixed_single_update": "New: {{added_list}} & Updated: {{updated_list}}",
                "mixed_multi_update": "New: {{added_list}} & Updates: {{updated_list}}",
                "generic": "Bot Update",
            },
            "changelog": {
                "added_landing": "test",
                "updated_landing": "test",
                "removed_landing": "test",
                "added_direct": "test",
                "updated_direct": "test",
                "removed_direct": "test",
            },
            "table": {
                "header": "test",
                "divider": "test",
                "line": "test",
            }
        }
    },
    safety={"max_outbound_links_warn": 5},
    outdatedPostHandling={"mode": "test"},
    messages={"releaseTitle": "test", "releaseDescription": "test"},
    skipContent={"startTag": "test", "endTag": "test"},
    feedback={
        "statusLineFormat": "test",
        "statusLineRegex": "test",
        "labels": {
            "working": "test",
            "broken": "test",
            "unknown": "test",
        },
        "workingKeywords": ["test"],
        "notWorkingKeywords": ["test"],
        "minFeedbackCount": 1,
    },
    timing={"firstCheck": 1, "maxWait": 1, "increaseBy": 1},
    parsing={"app_key": "test", "version_key": "test", "asset_name_key": "test"},
    apps=[],
)

ADDED_SINGLE = {"app1": {"display_name": "App One", "version": "1.0.0"}}
ADDED_MULTI = {
    "app1": {"display_name": "App One", "version": "1.0.0"},
    "app2": {"display_name": "App Two", "version": "2.0.0"},
}
UPDATED_SINGLE = {"app3": {"display_name": "App Three", "version": "1.1.0"}}
UPDATED_MULTI = {
    "app3": {"display_name": "App Three", "version": "1.1.0"},
    "app4": {"display_name": "App Four", "version": "2.1.0"},
}

# --- Test Cases ---

def test_title_added_only():
    """Tests title generation for only added apps."""
    result = _generate_dynamic_title(MOCK_CONFIG, ADDED_MULTI, {})
    assert result == "New Apps Added: App One v1.0.0, App Two v2.0.0"

def test_title_updated_only_single():
    """Tests title generation for a single updated app."""
    result = _generate_dynamic_title(MOCK_CONFIG, {}, UPDATED_SINGLE)
    assert result == "App Update: App Three v1.1.0"

def test_title_updated_only_multi():
    """Tests title generation for multiple updated apps."""
    result = _generate_dynamic_title(MOCK_CONFIG, {}, UPDATED_MULTI)
    assert result == "App Updates: App Three v1.1.0, App Four v2.1.0"

def test_title_mixed_single_update():
    """Tests title generation for added apps and a single updated app."""
    result = _generate_dynamic_title(MOCK_CONFIG, ADDED_SINGLE, UPDATED_SINGLE)
    assert result == "New: App One v1.0.0 & Updated: App Three v1.1.0"

def test_title_mixed_multi_update():
    """Tests title generation for added apps and multiple updated apps."""
    result = _generate_dynamic_title(MOCK_CONFIG, ADDED_MULTI, UPDATED_MULTI)
    assert result == "New: App One v1.0.0, App Two v2.0.0 & Updates: App Three v1.1.0, App Four v2.1.0"

def test_title_no_changes():
    """Tests title generation for no changes."""
    result = _generate_dynamic_title(MOCK_CONFIG, {}, {})
    assert result == "Bot Update"

# --- Property-Based Tests with Hypothesis ---

# Strategy for generating app dictionaries
app_strategy = st.dictionaries(
    keys=st.text(min_size=1, alphabet="abcdefghijklmnopqrstuvwxyz"),
    values=st.fixed_dictionaries({
        "display_name": st.text(min_size=1),
        "version": st.text(min_size=1)
    }),
    min_size=1,
    max_size=5
)

@given(added=app_strategy, updated=app_strategy)
def test_title_generation_hypothesis(added, updated):
    """Ensures title generation runs without errors for various inputs."""
    try:
        _generate_dynamic_title(MOCK_CONFIG, added, updated)
    except Exception as e:
        pytest.fail(f"Title generation failed with error: {e}")

@given(added=app_strategy)
def test_title_generation_added_only_hypothesis(added):
    """Ensures added-only titles are generated correctly."""
    result = _generate_dynamic_title(MOCK_CONFIG, added, {})
    assert "New Apps Added:" in result

@given(updated=app_strategy)
def test_title_generation_updated_only_hypothesis(updated):
    """Ensures updated-only titles are generated correctly."""
    result = _generate_dynamic_title(MOCK_CONFIG, {}, updated)
    if len(updated) == 1:
        assert "App Update:" in result
    else:
        assert "App Updates:" in result
