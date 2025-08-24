from pathlib import Path

# Determine the absolute path to the project's root directory.
ROOT_DIR = Path(__file__).resolve().parent.parent

# --- Core Configuration and State Files ---
CONFIG_FILE = ROOT_DIR / "config.toml"
BOT_STATE_FILE = ROOT_DIR / "bot_state.json"
RELEASE_STATE_FILE = ROOT_DIR / "release_state.json"
REQUIREMENTS_FILE = ROOT_DIR / "requirements.txt"

# --- Output and Artifact Directories ---
DIST_DIR = ROOT_DIR / "dist"
RELEASES_JSON_FILE = DIST_DIR / "releases.json"
LANDING_PAGE_OUTPUT = DIST_DIR / "index.html"

# --- Template Directory ---
TEMPLATES_DIR = ROOT_DIR / "templates"
DEFAULT_LANDING_PAGE = TEMPLATES_DIR / "default_landing_page.html"


def get_template_path(template_name: str) -> Path:
    """Returns the absolute path for a given template name."""
    return TEMPLATES_DIR / template_name
