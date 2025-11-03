"""Data modification for BitBot file patching."""

from typing import Any

import deal
from beartype import beartype


@deal.pre(lambda data_object: len(data_object) > 0, message="Data object cannot be empty")
@deal.post(lambda result: isinstance(result, dict))
@beartype
def modify(data_object: dict[str, Any]) -> dict[str, Any]:
    """Modify decrypted data by setting all boolean false values to true."""
    for key, value in data_object.items():
        if value is False:
            data_object[key] = True
    return data_object
