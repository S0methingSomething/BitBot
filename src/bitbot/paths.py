"""Path constants for the BitBot project."""

from pathlib import Path

import deal
from beartype import beartype

# Determine the absolute path to the project's root directory
ROOT_DIR: Path = Path(__file__).parent.parent.parent.resolve()

# Core Configuration and State Files
CONFIG_FILE: Path = ROOT_DIR / "config.toml"
BOT_STATE_FILE: Path = ROOT_DIR / "bot_state.json"
RELEASE_STATE_FILE: Path = ROOT_DIR / "release_state.json"

# Output and Artifact Directories
DIST_DIR: Path = ROOT_DIR / "dist"
RELEASE_QUEUE_FILE: Path = DIST_DIR / "release_queue.json"

# Template Directory
TEMPLATES_DIR: Path = ROOT_DIR / "templates"
DEFAULT_LANDING_PAGE: Path = TEMPLATES_DIR / "default_landing_page.html"


@deal.pre(
    lambda template_name: len(template_name) > 0,
    message="Template name cannot be empty",
)
@deal.pre(
    lambda template_name: ".." not in template_name and "/" not in template_name,
    message="Template name cannot contain path traversal characters",
)
@beartype
def get_template_path(template_name: str) -> Path:
    """Return the absolute path for a given template name.

    Args:
        template_name: Name of the template file.

    Returns:
        Absolute path to the template file.
    """
    return TEMPLATES_DIR / template_name
