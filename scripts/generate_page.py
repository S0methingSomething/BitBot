#!/usr/bin/env python
"""This script generates the landing page."""

import argparse
import json
from pathlib import Path

from src.bitbot.core.container import container
from src.bitbot.models.page_data import PageData


def main():
    """The main function."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--vercel", action="store_true", help="Generate a Vercel deployment.")
    args = parser.parse_args()

    # This is a placeholder for the actual data fetching logic
    page_data = PageData(apps={})

    page_generator_service = container.page_generator_service()
    html = page_generator_service.generate_page(page_data)

    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)
    (dist_dir / "index.html").write_text(html)

    if args.vercel:
        vercel_config = {
            "version": 2,
            "builds": [{"src": "dist/index.html", "use": "@vercel/static"}],
        }
        (dist_dir / "vercel.json").write_text(json.dumps(vercel_config, indent=4))

    logger = container.logging_service()
    logger.info("Landing page generated successfully.")


if __name__ == "__main__":
    main()
