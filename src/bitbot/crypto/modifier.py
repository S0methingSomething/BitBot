"""Game asset data modification for unlocking premium features.

This module modifies decrypted game configuration data to unlock IAP
(In-App Purchase) features by changing False → True.
"""

from typing import Any

import icontract
from beartype import beartype


@icontract.require(
    lambda data_object: len(data_object) > 0,
    description="Data object cannot be empty",
)
@icontract.ensure(lambda result: len(result) > 0)
@beartype
def unlock_premium_features(data_object: dict[str, Any]) -> dict[str, Any]:
    """Unlock premium features by setting all False values to True.

    Creates a new dict without mutating the input.

    Args:
        data_object: Decrypted game asset data

    Returns:
        New dict with all False values changed to True
    """
    return {key: True if value is False else value for key, value in data_object.items()}


# Backward compatibility alias
modify = unlock_premium_features
