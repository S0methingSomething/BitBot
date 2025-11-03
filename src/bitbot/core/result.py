"""Result type for error handling without exceptions."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

import deal
from beartype import beartype

T = TypeVar("T")
E = TypeVar("E")


@dataclass
class Ok[T]:
    """Success result."""

    value: T

    @beartype
    def is_ok(self) -> bool:
        """Check if result is Ok."""
        return True

    @beartype
    def is_err(self) -> bool:
        """Check if result is Err."""
        return False

    @deal.post(lambda result: result is not None, message="unwrap() must never return None")
    @beartype
    def unwrap(self) -> T:
        """Get the value."""
        return self.value

    @beartype
    def unwrap_or(self, default: T) -> T:
        """Get value or default."""
        return self.value

    @beartype
    def map(self, func: Callable[[T], T]) -> "Ok[T]":
        """Transform Ok value."""
        return Ok(func(self.value))

    @beartype
    def and_then(self, func: Callable[[T], "Result[T, E]"]) -> "Result[T, E]":
        """Chain Result-returning operations."""
        return func(self.value)


@dataclass
class Err[E]:
    """Error result."""

    error: E

    @beartype
    def is_ok(self) -> bool:
        """Check if result is Ok."""
        return False

    @beartype
    def is_err(self) -> bool:
        """Check if result is Err."""
        return True

    @deal.raises(RuntimeError, message="unwrap() on Err always raises")
    @beartype
    def unwrap(self) -> None:
        """Raise error."""
        msg = f"Called unwrap on Err: {self.error}"
        raise RuntimeError(msg)

    @beartype
    def unwrap_or(self, default: E) -> E:
        """Get default value."""
        return default

    @beartype
    def map(self, func: Callable[[T], T]) -> "Err[E]":
        """Transform does nothing on Err."""
        return self

    @beartype
    def and_then(self, func: Callable[[T], "Result[T, E]"]) -> "Err[E]":
        """Chain does nothing on Err."""
        return self

    @beartype
    def map_err(self, func: Callable[[E], E]) -> "Err[E]":
        """Transform error value."""
        return Err(func(self.error))


# Type alias for Result
Result = Ok[T] | Err[E]
