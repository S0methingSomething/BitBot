"""Dependency injection container for BitBot."""

from dependency_injector import containers, providers
from rich.console import Console

from bitbot.config_models import Config
from bitbot.core.config import load_config
from bitbot.core.error_logger import ErrorLogger


def _load_config_or_exit() -> Config:
    """Load config and exit with error if it fails."""
    result = load_config()
    if result.is_err():
        console = Console()
        console.print(f"[red]✗ Configuration Error:[/red] {result.unwrap_err().message}")
        raise SystemExit(1)
    return result.unwrap()


class Container(containers.DeclarativeContainer):
    """Application DI container."""

    # Core services
    console = providers.Singleton(Console)

    config = providers.Singleton(_load_config_or_exit)

    logger = providers.Singleton(
        ErrorLogger,
        console=console,
    )
