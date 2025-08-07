"""Service for parsing data from various sources."""

import re

from ..models.config import Config


class ParsingService:
    """A service dedicated to parsing structured data."""

    def parse_release_notes(self, body: str, config: Config) -> dict | None:
        """Parse release information from its body.

        Supports all legacy formats and the new structured format.
        """
        # --- Priority 1: New Structured Format (from release body) ---
        parsing_keys = config.parsing
        app_match = re.search(rf"^{parsing_keys.app_key}:\s*(\S+)", body, re.MULTILINE)
        version_match = re.search(rf"^{parsing_keys.version_key}:\s*([\d\.]+)", body, re.MULTILINE)
        asset_match = re.search(rf"^{parsing_keys.asset_name_key}:\s*(\S+)", body, re.MULTILINE)

        if app_match and version_match and asset_match:
            return {
                "app_id": app_match.group(1),
                "version": version_match.group(1),
                "asset_name": asset_match.group(1),
            }

        return None
