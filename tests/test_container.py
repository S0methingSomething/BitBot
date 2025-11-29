"""Tests for dependency injection container."""

from rich.console import Console

from bitbot.config_models import Config
from bitbot.core.container import Container
from bitbot.core.error_logger import ErrorLogger


def test_container_provides_console():
    """Test container provides Console singleton."""
    container = Container()
    console = container.console()

    assert isinstance(console, Console)


def test_container_console_is_singleton():
    """Test container returns same Console instance."""
    container = Container()
    console1 = container.console()
    console2 = container.console()

    assert console1 is console2


def test_container_provides_config():
    """Test container provides Config."""
    container = Container()
    config = container.config()

    assert isinstance(config, Config)


def test_container_provides_logger():
    """Test container provides ErrorLogger."""
    container = Container()
    logger = container.logger()

    assert isinstance(logger, ErrorLogger)
