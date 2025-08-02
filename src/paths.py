import os

# Determine the absolute path to the project's root directory.
# This is done by taking the directory of the current file (__file__),
# which is /path/to/project/src, and going one level up.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# --- Core Configuration and State Files ---
CONFIG_FILE = os.path.join(ROOT_DIR, 'config.toml')
BOT_STATE_FILE = os.path.join(ROOT_DIR, 'bot_state.json')
RELEASE_STATE_FILE = os.path.join(ROOT_DIR, 'release_state.json')
REQUIREMENTS_FILE = os.path.join(ROOT_DIR, 'requirements.txt')

# --- Output and Artifact Directories ---
DIST_DIR = os.path.join(ROOT_DIR, 'dist')
RELEASES_JSON_FILE = os.path.join(DIST_DIR, 'releases.json')
LANDING_PAGE_OUTPUT = os.path.join(DIST_DIR, 'index.html')

# --- Template Directory ---
TEMPLATES_DIR = os.path.join(ROOT_DIR, 'templates')
DEFAULT_LANDING_PAGE = os.path.join(TEMPLATES_DIR, 'default_landing_page.html')

def get_template_path(template_name: str) -> str:
    """Returns the absolute path for a given template name."""
    return os.path.join(TEMPLATES_DIR, template_name)
