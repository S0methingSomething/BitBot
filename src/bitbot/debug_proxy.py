"""A debug proxy for intercepting and interactively debugging service calls."""

import asyncio
import logging
from typing import Awaitable, Callable, ParamSpec, TypeVar, cast

from rich.console import Console

logger = logging.getLogger(__name__)
console = Console()

P = ParamSpec("P")
T = TypeVar("T")


class DebugProxyManager:
    """
    A proxy that intercepts and logs method calls.

    It also has an optional interactive mode.
    """

    def __init__(
        self, wrapped_instance: object, service_name: str, interactive: bool = False
    ) -> None:
        """
        Initializes the DebugProxyManager.

        Args:
            wrapped_instance: The actual service instance to wrap.
            service_name: The name of the service for logging.
            interactive: If True, prompt the user before each call.
        """
        self._wrapped_instance = wrapped_instance
        self._service_name = service_name
        self._interactive = interactive

    def __getattr__(
        self, attr_name: str
    ) -> Callable[P, T] | Callable[P, Awaitable[T]]:
        """Intercepts attribute access on the wrapped object, such as method calls."""
        try:
            original_attr: Callable[P, T] | Callable[P, Awaitable[T]] = getattr(
                self._wrapped_instance, attr_name
            )
        except AttributeError as e:
            raise AttributeError(
                f"'{self._service_name}' object has no attribute '{attr_name}'"
            ) from e

        if not callable(original_attr):
            pass

        async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            """An async wrapper for intercepted async methods."""
            console.print(
                f"[bold yellow][DEBUG] Calling async:[/bold yellow] "
                f"[cyan]{self._service_name}.{attr_name}[/cyan]",
                "with args:",
                args,
                "kwargs:",
                kwargs,
            )

            if self._interactive:
                prompt = (
                    "  -> Proceed? ([bold green]Y[/bold green]es/"
                    "[bold red]n[/bold red]o): "
                )
                response = console.input(prompt).lower()
                if response in ["n", "no"]:
                    console.print("[bold red]Execution skipped by user.[/bold red]")
                    # We need to return something that fits the type T.
                    # Since we don't know what T is, we can't return a specific value.
                    # This is a limitation of the interactive mode.
                    # For now, we'll assume that returning None is acceptable.
                    return None  # type: ignore

            try:
                # We need to cast original_attr to the async callable type
                async_callable = cast(Callable[P, Awaitable[T]], original_attr)
                result = await async_callable(*args, **kwargs)
                console.print(
                    f"[bold green][DEBUG] Result from "
                    f"{self._service_name}.{attr_name}:[/bold green]",
                    result,
                )
                return result
            except Exception as e:
                console.print(
                    f"[bold red][DEBUG] Exception from "
                    f"{self._service_name}.{attr_name}:[/bold red]",
                    e,
                )
                raise

        def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            """A sync wrapper for intercepted sync methods."""
            console.print(
                f"[bold yellow][DEBUG] Calling sync:[/bold yellow] "
                f"[cyan]{self._service_name}.{attr_name}[/cyan]",
                "with args:",
                args,
                "kwargs:",
                kwargs,
            )
            if self._interactive:
                prompt = (
                    "  -> Proceed? ([bold green]Y[/bold green]es/"
                    "[bold red]n[/bold red]o): "
                )
                response = console.input(prompt).lower()
                if response in ["n", "no"]:
                    console.print("[bold red]Execution skipped by user.[/bold red]")
                    return None  # type: ignore

            try:
                # We need to cast original_attr to the sync callable type
                sync_callable = cast(Callable[P, T], original_attr)
                result = sync_callable(*args, **kwargs)
                console.print(
                    f"[bold green][DEBUG] Result from "
                    f"{self._service_name}.{attr_name}:[/bold green]",
                    result,
                )
                return result
            except Exception as e:
                console.print(
                    f"[bold red][DEBUG] Exception from "
                    f"{self._service_name}.{attr_name}:[/bold red]",
                    e,
                )
                raise

        if asyncio.iscoroutinefunction(original_attr):
            return async_wrapper
        return sync_wrapper
