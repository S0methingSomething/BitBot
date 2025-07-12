#!/usr/bin/env python
from __future__ import annotations

import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.bitbot.config import Credentials


def main() -> None:
    """
    Generates a template credentials.toml file.
    """
    # Create an empty Credentials object
    credentials = Credentials()
    # Save it to the default location
    credentials.save()


if __name__ == "__main__":
    main()
