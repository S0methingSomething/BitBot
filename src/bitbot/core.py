import logging
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Coroutine

import httpx
import tomlkit

from .settings import Settings, load_settings

# Type alias for async functions
AsyncCallable = Callable[..., Coroutine[Any, Any, Any]]


class FeatureRegistry:
    """A simple, declarative registry of the bot's capabilities."""

    def __init__(self, features_path: Path = Path("features.toml")):
        self._features = tomlkit.loads(features_path.read_text()).get("feature", {})
        self._logger = logging.getLogger(__name__)
        self._logger.info(
            f"Loaded features: {[f for f, v in self._features.items() if v.get('enabled') is True]}"
        )

    def is_enabled(self, feature_name: str) -> bool:
        """Checks if a declared feature is enabled."""
        feature = self._features.get(feature_name)
        return feature is not None and feature.get("enabled", False)


class ExecutionBroker:
    """
    Manages permissions and executes all I/O operations.
    This is the "Head of Security" and the "Nervous System".
    """

    def __init__(self, settings: Settings):
        self._settings = settings
        self._logger = logging.getLogger(__name__)
        # The Rulebook: Defines which services can access which resources.
        self._rulebook: dict[str, Any] = {
            "file:read": [
                (
                    # Rule: Allow WorkspaceService to read from the templates directory
                    lambda req, ctx: req.__class__.__name__ == "WorkspaceService"
                    and ctx.get("path", "").startswith("templates/")
                ),
                (
                    # Rule: Allow WorkspaceService to read bot_state.json
                    lambda req, ctx: req.__class__.__name__ == "WorkspaceService"
                    and ctx.get("path") == "bot_state.json"
                )
            ],
            "file:write": [
                (
                    # Rule: Allow WorkspaceService to write ONLY to bot_state.json
                    lambda req, ctx: req.__class__.__name__ == "WorkspaceService"
                    and ctx.get("path") == "bot_state.json"
                )
            ],
            "network:call": [
                (
                    # Rule: Allow GitHubClient to make GET requests
                    lambda req, ctx: req.__class__.__name__ == "GitHubClient"
                    and ctx.get("method") == "GET"
                ),
                (
                    # Rule: Allow GitHubClient to make POST requests
                    lambda req, ctx: req.__class__.__name__ == "GitHubClient"
                    and ctx.get("method") == "POST"
                ),
                (
                    # Rule: Allow RedditClient to make POST requests
                    lambda req, ctx: req.__class__.__name__ == "RedditClient"
                    and ctx.get("method") == "POST"
                )
            ],
        }

    def _check_permissions(self, requester: Any, resource: str, context: dict) -> bool:
        """
        Checks if the requester has permission for the resource with the given context.
        """
        rules = self._rulebook.get(resource, [])
        for rule in rules:
            if rule(requester, context):
                self._logger.debug(
                    "Permission check for %s on '%s' with context %s. Approved.",
                    requester.__class__.__name__,
                    resource,
                    context,
                )
                return True

        self._logger.warning(
            "Permission check for %s on '%s' with context %s. DENIED.",
            requester.__class__.__name__,
            resource,
            context,
        )
        return False

    async def request_file_read(self, requester: Any, path: str) -> str:
        """Handles a request to read a file."""
        context = {"path": path}
        if not self._check_permissions(requester, "file:read", context):
            raise PermissionError(
                f"Permission denied for {requester.__class__.__name__} to read {path}"
            )

        try:
            self._logger.debug(f"Broker executing file read at: {path}")
            p = Path(path)
            return p.read_text()
        except FileNotFoundError as e:
            self._logger.error(f"File not found at {path}")
            raise e

    async def request_file_write(self, requester: Any, path: str, content: str) -> None:
        """Handles a request to write a file."""
        context = {"path": path, "content_len": len(content)}
        if not self._check_permissions(requester, "file:write", context):
            class_name = requester.__class__.__name__
            raise PermissionError(
                f"Permission denied for {class_name} to write to {path}"
            )

        try:
            self._logger.debug(f"Broker executing file write to: {path}")
            p = Path(path)
            p.write_text(content)
        except Exception as e:
            self._logger.error(f"Failed to write to file at {path}: {e}")
            raise e

    async def request_network_call(
        self, requester: Any, method: str, url: str, **kwargs
    ) -> Any:
        """Handles a request to make a network call."""
        context = {"method": method, "url": url, "kwargs": kwargs}
        if not self._check_permissions(requester, "network:call", context):
            raise PermissionError("Permission denied for network call.")

        try:
            self._logger.debug(f"Broker executing network call: {method} {url}")
            async with httpx.AsyncClient() as client:
                response = await client.request(method, url, **kwargs)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            self._logger.error(f"HTTP error during network call to {url}: {e}")
            raise
        except Exception as e:
            self._logger.error(f"Error during network call to {url}: {e}")
            raise


class ApplicationCore:
    """The central, unified core of the application."""

    def __init__(self, config_path: str = "config.toml"):
        self.settings = load_settings(Path(config_path))
        self.features = FeatureRegistry()
        self.broker = ExecutionBroker(self.settings)
        self.logger = logging.getLogger(__name__)
        # In a real implementation, we would initialize services here.

    def permission_required(
        self, resource: str
    ) -> Callable[[AsyncCallable], AsyncCallable]:
        """Decorator to enforce permissions via the Execution Broker."""

        def decorator(func: AsyncCallable) -> AsyncCallable:
            @wraps(func)
            async def wrapper(service_instance: Any, **kwargs: Any) -> Any:
                # This is a simplified version. The real one will be more robust.
                context = kwargs
                if not self.broker._check_permissions(
                    service_instance, resource, context
                ):
                    class_name = service_instance.__class__.__name__
                    raise PermissionError(
                        f"Permission denied for {class_name} on '{resource}'."
                    )
                return await func(service_instance, **kwargs)

            return wrapper

        return decorator
