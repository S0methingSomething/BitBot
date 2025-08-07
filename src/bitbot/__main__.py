"""Main entry point for the BitBot application.

This script initializes the service container and runs the primary services.
"""

from rich.traceback import install

from .core.container import container


def main() -> None:
    """Run the main application logic."""
    # Install rich traceback handler for beautiful error reporting
    install()

    release_service = container.release_management_service()
    release_service.process_new_releases()


if __name__ == "__main__":
    main()
