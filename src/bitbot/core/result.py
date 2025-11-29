"""Result type for error handling without exceptions."""

from __future__ import annotations

from collections.abc import Callable  # noqa: TC003
from dataclasses import dataclass
from typing import NoReturn, TypeVar

import deal
from beartype import beartype

# TypeVars for method signatures (class generics don't cover cross-type operations)
T = TypeVar("T")
E = TypeVar("E")
U = TypeVar("U")


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

    @beartype
    def unwrap(self) -> T:
        """Get the value."""
        return self.value

    @beartype
    def unwrap_or(self, default: T) -> T:
        """Get value or default."""
        return self.value

    @beartype
    def map(self, func: Callable[[T], U]) -> Ok[U]:
        """Transform Ok value."""
        return Ok(func(self.value))

    @beartype
    def and_then(self, func: Callable[[T], Ok[U] | Err[E]]) -> Ok[U] | Err[E]:
        """Chain Result-returning operations."""
        return func(self.value)

    @beartype
    def map_err(self, func: Callable[[E], E]) -> Ok[T]:
        """Transform error (no-op for Ok)."""
        return self

    @deal.raises(RuntimeError, message="unwrap_err() on Ok always raises")
    @beartype
    def unwrap_err(self) -> NoReturn:
        """Raise error - Ok has no error to unwrap."""
        msg = f"Called unwrap_err on Ok: {self.value}"
        raise RuntimeError(msg)


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
    def unwrap(self) -> NoReturn:
        """Raise error."""
        msg = f"Called unwrap on Err: {self.error}"
        raise RuntimeError(msg)

    @beartype
    def unwrap_or(self, default: T) -> T:
        """Get default value."""
        return default

    @beartype
    def map(self, func: Callable[[T], U]) -> Err[E]:
        """Transform does nothing on Err."""
        return self

    @beartype
    def and_then(self, func: Callable[[T], Ok[U] | Err[E]]) -> Err[E]:
        """Chain does nothing on Err."""
        return self

    @beartype
    def map_err(self, func: Callable[[E], E]) -> Err[E]:
        """Transform error value."""
        return Err(func(self.error))

    @beartype
    def unwrap_err(self) -> E:
        """Get the error value."""
        return self.error


# Type alias for Result
type Result[T, E] = Ok[T] | Err[E]
