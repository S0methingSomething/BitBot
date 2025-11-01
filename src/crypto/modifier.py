"""Data modification for BitBot crypto."""

import deal
from beartype import beartype


@deal.pre(lambda data_object: isinstance(data_object, dict))
@deal.post(lambda result: isinstance(result, dict))
@beartype
def modify(data_object: dict[str, str | bool]) -> dict[str, str | bool]:
    """Modifies the decrypted data object by setting all boolean false values to true."""
    for key, value in data_object.items():
        if value is False:
            data_object[key] = True
    return data_object
