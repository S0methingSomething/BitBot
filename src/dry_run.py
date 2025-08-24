"""Dry-run levels management for BitBot."""

import os
from enum import IntEnum

from logging_config import get_logger

logger = get_logger(__name__)


class DryRunLevel(IntEnum):
    """Dry-run levels for controlling external interactions."""

    # Level 0: No external interactions at all
    FULL_DRY_RUN = 0

    # Level 1: Allow read operations only
    READ_ONLY = 1

    # Level 2: Allow safe write operations (no public posts)
    SAFE_WRITES = 2

    # Level 3: Allow public preview operations (drafts/previews)
    PUBLIC_PREVIEW = 3

    # Level 4: Full production mode
    PRODUCTION = 4


def get_dry_run_level() -> DryRunLevel:
    """Get the current dry-run level from environment."""
    # Check for numeric level first
    if level_str := os.environ.get("DRY_RUN_LEVEL"):
        try:
            level = int(level_str)
            if level in [e.value for e in DryRunLevel]:
                return DryRunLevel(level)
        except ValueError:
            pass

    # Check for named level
    level_name = os.environ.get("DRY_RUN", "").upper()

    # Map level names to enum values
    level_mapping = {
        "TRUE": DryRunLevel.FULL_DRY_RUN,
        "1": DryRunLevel.FULL_DRY_RUN,
        "YES": DryRunLevel.FULL_DRY_RUN,
        "FULL": DryRunLevel.FULL_DRY_RUN,
        "READ_ONLY": DryRunLevel.READ_ONLY,
        "SAFE_WRITES": DryRunLevel.SAFE_WRITES,
        "PUBLIC_PREVIEW": DryRunLevel.PUBLIC_PREVIEW,
        "FALSE": DryRunLevel.PRODUCTION,
        "0": DryRunLevel.PRODUCTION,
        "NO": DryRunLevel.PRODUCTION,
        "PRODUCTION": DryRunLevel.PRODUCTION,
    }

    if level_name in level_mapping:
        return level_mapping[level_name]

    # Default behavior - check for legacy DRY_RUN
    if os.environ.get("DRY_RUN", "").lower() in ["true", "1", "yes"]:
        return DryRunLevel.FULL_DRY_RUN

    # Default to production if no dry-run settings
    return DryRunLevel.PRODUCTION


def is_dry_run() -> bool:
    """Check if any dry-run mode is enabled."""
    return get_dry_run_level() < DryRunLevel.PRODUCTION


def can_make_external_calls() -> bool:
    """Check if external API calls are allowed."""
    return get_dry_run_level() >= DryRunLevel.READ_ONLY


def can_make_writes() -> bool:
    """Check if write operations are allowed."""
    return get_dry_run_level() >= DryRunLevel.SAFE_WRITES


def can_make_public_posts() -> bool:
    """Check if public posts are allowed."""
    return get_dry_run_level() >= DryRunLevel.PUBLIC_PREVIEW


def should_create_drafts() -> bool:
    """Check if operations should be done in draft/preview mode."""
    level = get_dry_run_level()
    return level == DryRunLevel.PUBLIC_PREVIEW


def log_dry_run_status() -> None:
    """Log the current dry-run status."""
    level = get_dry_run_level()
    logger.info(f"Dry-run level: {level.name} ({level.value})")

    if level == DryRunLevel.FULL_DRY_RUN:
        logger.info("Full dry-run mode: No external interactions")
    elif level == DryRunLevel.READ_ONLY:
        logger.info("Read-only mode: External reads allowed, no writes")
    elif level == DryRunLevel.SAFE_WRITES:
        logger.info("Safe writes mode: Read and safe write operations allowed")
    elif level == DryRunLevel.PUBLIC_PREVIEW:
        logger.info("Public preview mode: Operations done in draft/preview mode")
    elif level == DryRunLevel.PRODUCTION:
        logger.info("Production mode: All operations allowed")


# Convenience functions for backward compatibility
def is_full_dry_run() -> bool:
    """Check if full dry-run mode is enabled (backward compatibility)."""
    return get_dry_run_level() == DryRunLevel.FULL_DRY_RUN
