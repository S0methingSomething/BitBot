"""Dependency injection container for BitBot."""

from beartype import beartype
from dependency_injector import containers, providers
from returns.result import Failure
from rich.console import Console

from bitbot.config_models import Config
from bitbot.core.app_registry import AppRegistry
from bitbot.core.config import load_config
from bitbot.core.error_logger import ErrorLogger
from bitbot.models import App


@beartype
def _load_config_or_exit() -> Config:
    """Load config and exit with error if it fails."""
    result = load_config()
    if isinstance(result, Failure):
        console = Console()
        console.print(f"[red]✗ Configuration Error:[/red] {result.failure().message}")
        raise SystemExit(1)
    return result.unwrap()


@beartype
def _create_app_registry(config: Config) -> AppRegistry:
    """Create AppRegistry from config."""
    apps = [App(**app_dict) for app_dict in config.apps]
    return AppRegistry(apps)


class Container(containers.DeclarativeContainer):
    """Application DI container."""

    # Core services
    console = providers.Singleton(Console)

    config = providers.Singleton(_load_config_or_exit)

    app_registry = providers.Singleton(
        _create_app_registry,
        config=config,
    )

    logger = providers.Singleton(
        ErrorLogger,
        console=console,
    )
