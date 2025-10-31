"""Path constants for the BitBot project."""

from pathlib import Path

import deal
from beartype import beartype

# Determine the absolute path to the project's root directory
ROOT_DIR: str = str(Path(__file__).parent.parent.resolve())

# Core Configuration and State Files
CONFIG_FILE: str = str(Path(ROOT_DIR) / "config.toml")
BOT_STATE_FILE: str = str(Path(ROOT_DIR) / "bot_state.json")
RELEASE_STATE_FILE: str = str(Path(ROOT_DIR) / "release_state.json")

# Output and Artifact Directories
DIST_DIR: str = str(Path(ROOT_DIR) / "dist")
RELEASES_JSON_FILE: str = str(Path(DIST_DIR) / "releases.json")

# Template Directory
TEMPLATES_DIR: str = str(Path(ROOT_DIR) / "templates")
DEFAULT_LANDING_PAGE: str = str(Path(TEMPLATES_DIR) / "default_landing_page.html")


@deal.pre(lambda template_name: len(template_name) > 0)  # type: ignore[misc]
@deal.post(lambda result: len(result) > 0)  # type: ignore[misc]
@beartype  # type: ignore[misc]
def get_template_path(template_name: str) -> str:
    """Return the absolute path for a given template name.

    Args:
        template_name: Name of the template file.

    Returns:
        Absolute path to the template file.
    """
    return str(Path(TEMPLATES_DIR) / template_name)
