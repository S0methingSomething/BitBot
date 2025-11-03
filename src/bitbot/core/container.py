"""Dependency injection container for BitBot."""

from dependency_injector import containers, providers
from rich.console import Console

from bitbot.core.config import load_config
from bitbot.core.error_logger import ErrorLogger


class Container(containers.DeclarativeContainer):
    """Application DI container."""

    # Configuration
    wiring_config = containers.WiringConfiguration(
        modules=[
            "bitbot.commands.check",
            "bitbot.commands.gather",
            "bitbot.commands.maintain",
            "bitbot.commands.page",
            "bitbot.commands.patch",
            "bitbot.commands.post",
            "bitbot.commands.release",
            "bitbot.commands.sync",
        ]
    )

    # Core services
    console = providers.Singleton(Console)

    config = providers.Singleton(
        lambda: load_config().unwrap(),
    )

    logger = providers.Singleton(
        ErrorLogger,
        console=console,
    )
