"""Factory for creating service instances."""

import argparse
from typing import Any, Dict

from bitbot.data.models import Settings
from bitbot.debug_proxy import DebugProxyManager
from bitbot.services.config_manager import FileConfigManager
from bitbot.services.crypto_manager import FernetCryptoManager
from bitbot.services.github_manager import AiohttpGitHubManager
from bitbot.services.reddit_manager import PrawRedditManager
from bitbot.services.state_manager import JsonStateManager


def create_all_services(settings: Settings, args: argparse.Namespace) -> Dict[str, Any]:
    """
    Creates and wires up all application services.

    In debug mode, this function will wrap the services in a DebugProxyManager.

    Args:
        settings: The application settings.
        args: The command-line arguments.

    Returns:
        A dictionary containing all the service instances.
    """
    services: Dict[str, Any] = {
        "config_manager": FileConfigManager(args.config),
        "state_manager": JsonStateManager(args.state),
        "github_manager": AiohttpGitHubManager(settings.github_token),
        "reddit_manager": PrawRedditManager(settings),
        "crypto_manager": FernetCryptoManager(settings.encryption_key),
    }

    if args.debug:
        for service_name, service_instance in services.items():
            services[service_name] = DebugProxyManager(
                service_instance, service_name, interactive=args.interactive
            )

    return services
