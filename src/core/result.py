"""Result type for error handling without exceptions."""

from dataclasses import dataclass
from typing import Generic, TypeVar

from beartype import beartype

T = TypeVar('T')
E = TypeVar('E')


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
    def unwrap_or(self, default: T) -> T:
        """Get value or default."""
        return self.value
    
    @beartype  # type: ignore[misc]
    def map(self, func: callable) -> "Ok":  # type: ignore[misc]
        """Transform Ok value."""
        return Ok(func(self.value))
    
    @beartype  # type: ignore[misc]
    def and_then(self, func: callable) -> "Result":  # type: ignore[misc]
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
        raise RuntimeError(f"Called unwrap on Err: {self.error}")
    
    @beartype  # type: ignore[misc]
    def unwrap_or(self, default: E) -> E:
        """Get default value."""
        return default
    
    @beartype  # type: ignore[misc]
    def map(self, func: callable) -> "Err":  # type: ignore[misc]
        """Transform does nothing on Err."""
        return self
    
    @beartype  # type: ignore[misc]
    def and_then(self, func: callable) -> "Err":  # type: ignore[misc]
        """Chain does nothing on Err."""
        return self
    
    @beartype  # type: ignore[misc]
    def map_err(self, func: callable) -> "Err":  # type: ignore[misc]
        """Transform error value."""
        return Err(func(self.error))


# Type alias for Result
Result = Ok[T] | Err[E]
