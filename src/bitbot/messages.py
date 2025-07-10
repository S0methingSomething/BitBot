"""
Centralized location for user-facing messages, especially for errors and exits.
"""


class ExitMessages:
    """
    A collection of critical error messages that result in application exit.
    Using a class to group them, but not instantiating it.
    """

    # --- Configuration & Initialization Errors ---
    CONFIG_NOT_FOUND = "Configuration file not found at: {path}"
    CONFIG_VALIDATION_FAILED = "Configuration validation failed: {error}"
    CREDENTIALS_MISSING = "Missing required credentials: {missing}"
    CLIENT_INIT_FAILED = "Failed to initialize API clients."
    CLIENT_INIT_FAILED_DESPITE_CREDS = (
        "Client initialization failed despite credentials being present."
    )

    # --- API & Connection Errors ---
    GITHUB_TOKEN_MISSING = "Missing GITHUB_TOKEN."
    CREDENTIAL_VALIDATION_FAILED_API = "Credential validation failed at the API level."
    PREFLIGHT_CHECK_FAILED = (
        "Credential validation failed. Please run 'test-credentials' for details."
    )

    # --- General Errors ---
    UNEXPECTED_ERROR = "An unexpected error occurred: {error}"
    INITIALIZATION_FAILED = "Initialization failed: {error}"
