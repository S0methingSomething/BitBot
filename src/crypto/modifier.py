"""Data modification for BitBot file patching."""

from typing import Any

from beartype import beartype


@beartype
def modify(data_object: dict[str, Any]) -> dict[str, Any]:
    """Modify decrypted data by setting all boolean false values to true."""
    for key, value in data_object.items():
        if value is False:
            data_object[key] = True
    return data_object
