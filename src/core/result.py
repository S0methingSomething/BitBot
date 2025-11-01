"""Result type for error handling without exceptions."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, TypeVar

import deal
from beartype import beartype

T = TypeVar("T")
E = TypeVar("E")


@dataclass
class Ok(Generic[T]):
    """Success result."""

    value: T

    @deal.post(lambda result: result is True)  # type: ignore[misc]
    @beartype  # type: ignore[misc]
    def is_ok(self) -> bool:
        """Check if result is Ok."""
        return True

    @deal.post(lambda result: result is False)  # type: ignore[misc]
    @beartype  # type: ignore[misc]
    def is_err(self) -> bool:
        """Check if result is Err."""
        return False

    @deal.post(lambda result: result is not None)  # type: ignore[misc]
    @beartype  # type: ignore[misc]
    def unwrap(self) -> T:
        """Get the value."""
        return self.value

    @beartype  # type: ignore[misc]
    def unwrap_or(self, default: T) -> T:
        """Get value or default."""
        return self.value

    @deal.pre(lambda _, func: func is not None)  # type: ignore[misc]
    @deal.post(lambda result: isinstance(result, Ok))  # type: ignore[misc]
    @beartype  # type: ignore[misc]
    def map(self, func: Callable[[T], T]) -> "Ok[T]":
        """Transform Ok value."""
        return Ok(func(self.value))

    @deal.pre(lambda _, func: func is not None)  # type: ignore[misc]
    @beartype  # type: ignore[misc]
    def and_then(self, func: Callable[[T], "Result[T, E]"]) -> "Result[T, E]":
        """Chain Result-returning operations."""
        return func(self.value)


@dataclass
class Err(Generic[E]):
    """Error result."""

    error: E

    @deal.post(lambda result: result is False)  # type: ignore[misc]
    @beartype  # type: ignore[misc]
    def is_ok(self) -> bool:
        """Check if result is Ok."""
        return False

    @deal.post(lambda result: result is True)  # type: ignore[misc]
    @beartype  # type: ignore[misc]
    def is_err(self) -> bool:
        """Check if result is Err."""
        return True

    @deal.raises(RuntimeError)  # type: ignore[misc]
    @beartype  # type: ignore[misc]
    def unwrap(self) -> None:
        """Raise error."""
        msg = f"Called unwrap on Err: {self.error}"
        raise RuntimeError(msg)

    @beartype  # type: ignore[misc]
    def unwrap_or(self, default: E) -> E:
        """Get default value."""
        return default

    @deal.post(lambda result: isinstance(result, Err))  # type: ignore[misc]
    @beartype  # type: ignore[misc]
    def map(self, func: Callable[[T], T]) -> "Err[E]":
        """Transform does nothing on Err."""
        return self

    @deal.post(lambda result: isinstance(result, Err))  # type: ignore[misc]
    @beartype  # type: ignore[misc]
    def and_then(self, func: Callable[[T], "Result[T, E]"]) -> "Err[E]":
        """Chain does nothing on Err."""
        return self

    @deal.pre(lambda _, func: func is not None)  # type: ignore[misc]
    @deal.post(lambda result: isinstance(result, Err))  # type: ignore[misc]
    @beartype  # type: ignore[misc]
    def map_err(self, func: Callable[[E], E]) -> "Err[E]":
        """Transform error value."""
        return Err(func(self.error))


# Type alias for Result
Result = Ok[T] | Err[E]
