"""Result type for error handling without exceptions."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, TypeVar

from beartype import beartype

T = TypeVar("T")
E = TypeVar("E")


@dataclass
class Ok(Generic[T]):
    """Success result."""
    value: T

    @beartype  # type: ignore[misc]
    def is_ok(self) -> bool:
        """Check if result is Ok."""
        return True

    @beartype  # type: ignore[misc]
    def is_err(self) -> bool:
        """Check if result is Err."""
        return False

    @beartype  # type: ignore[misc]
    def unwrap(self) -> T:
        """Get the value."""
        return self.value

    @beartype  # type: ignore[misc]
    def unwrap_or(self, default: T) -> T:  # noqa: ARG002
        """Get value or default."""
        return self.value

    @beartype  # type: ignore[misc]
    def map(self, func: Callable  # noqa: ARG002[[T], T]) -> "Ok[T]":
        """Transform Ok value."""
        return Ok(func(self.value))

    @beartype  # type: ignore[misc]
    def and_then(self, func: Callable  # noqa: ARG002[[T], "Result[T, E]"]) -> "Result[T, E]":
        """Chain Result-returning operations."""
        return func(self.value)


@dataclass
class Err(Generic[E]):
    """Error result."""
    error: E

    @beartype  # type: ignore[misc]
    def is_ok(self) -> bool:
        """Check if result is Ok."""
        return False

    @beartype  # type: ignore[misc]
    def is_err(self) -> bool:
        """Check if result is Err."""
        return True

    @beartype  # type: ignore[misc]
    def unwrap(self) -> None:
        """Raise error."""
        msg = f"Called unwrap on Err: {self.error}"
        raise RuntimeError(msg)

    @beartype  # type: ignore[misc]
    def unwrap_or(self, default: E) -> E:
        """Get default value."""
        return default

    @beartype  # type: ignore[misc]
    def map(self, func: Callable  # noqa: ARG002[[T], T]) -> "Err[E]":
        """Transform does nothing on Err."""
        return self

    @beartype  # type: ignore[misc]
    def and_then(self, func: Callable  # noqa: ARG002[[T], "Result[T, E]"]) -> "Err[E]":
        """Chain does nothing on Err."""
        return self

    @beartype  # type: ignore[misc]
    def map_err(self, func: Callable[[E], E]) -> "Err[E]":
        """Transform error value."""
        return Err(func(self.error))


# Type alias for Result
Result = Ok[T] | Err[E]
