# Vulture whitelist for false positives
# These are used by frameworks or are part of the public API

# Pydantic model configuration and validators (called by Pydantic internally)
model_config  # Pydantic model configuration
cls  # Pydantic field_validator first parameter
validate_repo_format  # Pydantic validator
validate_asset_name  # Pydantic validator
validate_subreddit  # Pydantic validator
validate_non_empty  # Pydantic validator
validate_post_mode  # Pydantic validator
validate_download_mode  # Pydantic validator
validate_positive_ints  # Pydantic validator
validate_offline  # Pydantic validator
validate_online  # Pydantic validator
validate_interval  # Pydantic validator
validate_release_id  # Pydantic validator
outdated_post  # Pydantic field
custom_landing  # Pydantic field
post_manually  # Pydantic field
offline  # Pydantic field
messages  # Pydantic field

# Result type methods (public API)
unwrap_or  # Result API method
map  # Result API method
and_then  # Result API method
map_err  # Result API method

# CLI entry point
main  # Typer callback

# Public API functions (used by CLI commands or external callers)
get_github_token  # Used by external callers
get_github_output  # Used by GitHub Actions
add_release  # Queue management API
clear_pending_releases  # Queue management API
load_global_state  # State management API
save_global_state  # State management API
load_release_state  # State management API
save_release_state  # State management API
parse_release_notes  # Parser API
get_source_releases  # GitHub API
check_if_bot_release_exists  # GitHub API
parse_release_description  # Parser API
update_older_posts  # Reddit API
DEFAULT_LANDING_PAGE  # Path constant
