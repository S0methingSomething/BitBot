"""Property-based tests using Hypothesis."""

import string

from hypothesis import given, settings
from hypothesis import strategies as st
from returns.result import Failure, Success

from bitbot.crypto.cipher import decrypt, encrypt
from bitbot.crypto.modifier import unlock_premium_features
from bitbot.crypto.obfuscation import get_obfuscated_key
from bitbot.reddit.posting.poster import count_outbound_links


# Result type properties
@given(st.integers())
def test_success_unwrap_returns_value(value):
    """Success.unwrap() always returns the wrapped value."""
    assert Success(value).unwrap() == value


@given(st.text())
def test_failure_value_or_returns_default(error):
    """Failure.value_or() always returns the default."""
    default = "default"
    assert Failure(error).value_or(default) == default


@given(st.integers(), st.integers())
def test_success_map_applies_function(value, add):
    """Success.map() applies function to value."""
    result = Success(value).map(lambda x: x + add)
    assert result.unwrap() == value + add


@given(st.text())
def test_failure_map_preserves_error(error):
    """Failure.map() preserves the error unchanged."""
    result = Failure(error).map(lambda x: x * 2)
    assert isinstance(result, Failure)
    assert result.failure() == error


@given(st.integers())
def test_success_is_success(value):
    """Success is instance of Success."""
    result = Success(value)
    assert isinstance(result, Success)
    assert not isinstance(result, Failure)


@given(st.text())
def test_failure_is_failure(error):
    """Failure is instance of Failure."""
    result = Failure(error)
    assert isinstance(result, Failure)
    assert not isinstance(result, Success)


# Crypto properties
@given(
    st.dictionaries(
        st.text(alphabet=string.ascii_letters + string.digits, min_size=1, max_size=20),
        st.booleans(),
        min_size=1,
        max_size=10,
    )
)
@settings(max_examples=50)
def test_encrypt_decrypt_roundtrip_booleans(data):
    """Encrypt then decrypt returns original boolean data."""
    key = get_obfuscated_key("testkey")
    encrypted = encrypt(data, key)
    decrypted = decrypt(encrypted, key)
    assert decrypted == data


@given(
    st.dictionaries(
        st.text(alphabet=string.ascii_letters, min_size=1, max_size=10),
        st.booleans(),
        min_size=1,
        max_size=5,
    )
)
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


@given(
    st.lists(
        st.sampled_from(
            [
                "https://example.com",
                "http://test.org",
                "https://a.b.c",
            ]
        ),
        min_size=0,
        max_size=10,
    )
)
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
