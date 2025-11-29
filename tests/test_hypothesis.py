"""Property-based tests using Hypothesis."""

import string

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from pydantic import ValidationError

from bitbot.core.result import Err, Ok
from bitbot.crypto.cipher import decrypt, encrypt
from bitbot.crypto.modifier import unlock_premium_features
from bitbot.crypto.obfuscation import get_obfuscated_key
from bitbot.models import PendingRelease
from bitbot.reddit.posting.poster import count_outbound_links


# Result type properties
@given(st.integers())
def test_ok_unwrap_returns_value(value):
    """Ok.unwrap() always returns the wrapped value."""
    assert Ok(value).unwrap() == value


@given(st.text())
def test_err_unwrap_or_returns_default(error):
    """Err.unwrap_or() always returns the default."""
    default = "default"
    assert Err(error).unwrap_or(default) == default


@given(st.integers(), st.integers())
def test_ok_map_applies_function(value, add):
    """Ok.map() applies function to value."""
    result = Ok(value).map(lambda x: x + add)
    assert result.unwrap() == value + add


@given(st.text())
def test_err_map_preserves_error(error):
    """Err.map() preserves the error unchanged."""
    result = Err(error).map(lambda x: x * 2)
    assert result.is_err()
    assert result.unwrap_err() == error


@given(st.integers())
def test_ok_is_ok_true(value):
    """Ok.is_ok() is always True."""
    assert Ok(value).is_ok() is True
    assert Ok(value).is_err() is False


@given(st.text())
def test_err_is_err_true(error):
    """Err.is_err() is always True."""
    assert Err(error).is_err() is True
    assert Err(error).is_ok() is False


# Crypto properties
@given(st.dictionaries(
    st.text(alphabet=string.ascii_letters + string.digits, min_size=1, max_size=20),
    st.booleans(),
    min_size=1,
    max_size=10,
))
@settings(max_examples=50)
def test_encrypt_decrypt_roundtrip_booleans(data):
    """Encrypt then decrypt returns original boolean data."""
    key = get_obfuscated_key("testkey")
    encrypted = encrypt(data, key)
    decrypted = decrypt(encrypted, key)
    assert decrypted == data


@given(st.dictionaries(
    st.text(alphabet=string.ascii_letters, min_size=1, max_size=10),
    st.booleans(),
    min_size=1,
    max_size=5,
))
@settings(max_examples=30)
def test_unlock_premium_features_all_true(data):
    """unlock_premium_features sets all False values to True."""
    result = unlock_premium_features(data)
    for key in data:
        if data[key] is False:
            assert result[key] is True
        else:
            assert result[key] == data[key]


@given(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=20))
def test_obfuscation_changes_key(key):
    """Obfuscation always changes the key."""
    obfuscated = get_obfuscated_key(key)
    assert obfuscated != key
    assert len(obfuscated) == len(key)


# URL counting properties
@given(st.text())
def test_count_outbound_links_non_negative(text):
    """Link count is always non-negative."""
    count = count_outbound_links(text)
    assert count >= 0


@given(st.lists(st.sampled_from([
    "https://example.com",
    "http://test.org",
    "https://a.b.c",
]), min_size=0, max_size=10))
def test_count_outbound_links_upper_bound(urls):
    """Link count is at most the number of unique URLs."""
    text = " ".join(urls)
    count = count_outbound_links(text)
    assert count <= len(set(urls))


@given(st.text(alphabet=string.ascii_letters + " "))
def test_count_outbound_links_no_urls_zero(text):
    """Text without URLs has zero link count."""
    count = count_outbound_links(text)
    assert count == 0


# Model validation properties
@given(st.text(min_size=1).filter(lambda x: x.strip()))
def test_pending_release_rejects_zero_id(tag):
    """PendingRelease rejects release_id <= 0."""
    with pytest.raises(ValidationError):
        PendingRelease(
            release_id=0,
            tag=tag,
            app_id="test",
            display_name="Test",
            version="1.0.0",
        )


@given(st.integers(min_value=1, max_value=1000000))
def test_pending_release_accepts_positive_id(release_id):
    """PendingRelease accepts positive release_id."""
    release = PendingRelease(
        release_id=release_id,
        tag="v1.0.0",
        app_id="test",
        display_name="Test",
        version="1.0.0",
    )
    assert release.release_id == release_id
