import os
import sys
from unittest.mock import patch

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from helpers import is_dry_run


def test_is_dry_run_enabled():
    """Test that is_dry_run() returns True when DRY_RUN is set to 'true'."""
    with patch.dict(os.environ, {'DRY_RUN': 'true'}):
        assert is_dry_run() is True


def test_is_dry_run_disabled():
    """Test that is_dry_run() returns False when DRY_RUN is not set."""
    with patch.dict(os.environ, {}, clear=True):
        assert is_dry_run() is False


def test_is_dry_run_false():
    """Test that is_dry_run() returns False when DRY_RUN is set to 'false'."""
    with patch.dict(os.environ, {'DRY_RUN': 'false'}):
        assert is_dry_run() is False