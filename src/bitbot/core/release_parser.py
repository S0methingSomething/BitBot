"""Unified release body parser.

Single source of truth for parsing release metadata from GitHub release bodies.
"""

from beartype import beartype

from bitbot.models import ParsedRelease


@beartype
def parse_release_body(body: str) -> ParsedRelease:
    """Parse release metadata from a release body.

    Expects structured format:
        app: <app_id>
        version: <version>
        asset_name: <asset_name>
        sha256: <hash>

    Args:
        body: Release body text

    Returns:
        ParsedRelease with extracted fields (None for missing fields)
    """
    data: dict[str, str | None] = {
        "app_id": None,
        "version": None,
        "asset_name": None,
        "sha256": None,
    }

    key_mapping = {
        "app": "app_id",
        "version": "version",
        "asset_name": "asset_name",
        "sha256": "sha256",
    }

    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue

        key, _, value = line.partition(":")
        key = key.strip().lower()
        value = value.strip()

        if key in key_mapping and value:
            data[key_mapping[key]] = value

    return ParsedRelease(**data)


@beartype
def parse_release_body_strict(body: str) -> ParsedRelease:
    """Parse release body and raise if incomplete.

    Args:
        body: Release body text

    Returns:
        ParsedRelease with app_id and version guaranteed

    Raises:
        ValueError: If app_id or version is missing
    """
    parsed = parse_release_body(body)
    if not parsed.is_complete:
        missing = []
        if parsed.app_id is None:
            missing.append("app")
        if parsed.version is None:
            missing.append("version")
        msg = f"Release body missing required fields: {', '.join(missing)}"
        raise ValueError(msg)
    return parsed
