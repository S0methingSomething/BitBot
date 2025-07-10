import logging
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

CACHE_FILE = Path(tempfile.gettempdir()) / "bitbot_creds_valid.txt"
CACHE_DURATION = timedelta(hours=24)


def is_cache_valid() -> bool:
    """Checks if the credential cache is still valid."""
    if not CACHE_FILE.exists():
        return False
    try:
        cached_time_str = CACHE_FILE.read_text(encoding="utf-8").strip()
        cached_time = datetime.fromisoformat(cached_time_str)
        if datetime.now() - cached_time < CACHE_DURATION:
            logging.info("Credential cache is still valid.")
            return True
        logging.info("Credential cache has expired.")
        return False
    except (ValueError, OSError) as e:
        logging.warning(f"Could not read or parse cache file: {e}")
        return False


def update_cache() -> None:
    """Updates the credential cache with the current timestamp."""
    try:
        CACHE_FILE.write_text(datetime.now().isoformat(), encoding="utf-8")
        logging.info("Credential cache updated.")
    except OSError as e:
        logging.error(f"Could not write to cache file: {e}")
