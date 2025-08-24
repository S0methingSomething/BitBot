import datetime
import inspect
from collections.abc import Callable
from functools import wraps
from typing import Any


class ComponentBroker:
    """
    A simple broker for managing components and services with communication tracing.
    This helps with debugging and compliance by tracking who requests what services.
    """

    def __init__(self, config: Any) -> None:
        self.config = config
        self._services: dict[str, Any] = {}
        self._communication_log: list[dict[str, Any]] = []

    def requires(
        self, service_name: str, reason: str, content_keys: list[str] | None = None
    ) -> Callable[..., Any]:
        """
        Decorator to declare service requirements for methods.

        Args:
            service_name: Name of the required service
            reason: Reason for requesting the service
            content_keys: Keys of content/data being processed
        """

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(func)
            def wrapper(component_instance: Any, *args: Any, **kwargs: Any) -> Any:
                # Extract content from arguments
                content = {}
                if content_keys:
                    sig = inspect.signature(func)
                    param_names = list(sig.parameters.keys())[1:]  # Skip 'self'
                    for _i, (param_name, arg_value) in enumerate(
                        zip(param_names, args, strict=False)
                    ):
                        if param_name in content_keys:
                            content[param_name] = arg_value

                # Log the requirement
                log_entry = {
                    "component": component_instance.__class__.__name__,
                    "method": func.__name__,
                    "service": service_name,
                    "reason": reason,
                    "content": content,
                    "timestamp": datetime.datetime.now().isoformat(),
                }
                self._communication_log.append(log_entry)

                # Get the service
                service = self.get_service(service_name)

                # Inject service as first argument (after self)
                # We need to modify args to insert the service
                new_args = (
                    (args[0] if args else service, *args[1:]) if args else (service,)
                )

                return func(component_instance, *new_args, **kwargs)

            return wrapper

        return decorator

    def get_service(self, name: str) -> Any:
        """Get a service by name, creating it if needed."""
        if name not in self._services:
            self._services[name] = self._create_service(name)
        return self._services[name]

    def _create_service(self, name: str) -> Any:
        """Factory method to create services based on name."""
        # For now, we'll create simple mock services
        # Later we'll implement real service creation
        if name == "github":
            return GitHubService(self.config.github)
        if name == "reddit":
            return RedditService(self.config.reddit)
        raise ValueError(f"Unknown service: {name}")

    def get_communication_log(self) -> list[dict[str, Any]]:
        """Get the communication log for debugging and compliance."""
        return self._communication_log


# Simple service classes for now
class GitHubService:
    def __init__(self, config: Any) -> None:
        self.config = config


class RedditService:
    def __init__(self, config: Any) -> None:
        self.config = config
