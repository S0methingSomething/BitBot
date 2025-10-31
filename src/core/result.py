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


@dataclass
class Err(Generic[E]):
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
    
    @beartype
    def unwrap(self) -> None:
        """Raise error."""
        raise RuntimeError(f"Called unwrap on Err: {self.error}")
    
    @beartype
    def unwrap_or(self, default: E) -> E:
        """Get default value."""
        return default


# Type alias for Result
Result = Ok[T] | Err[E]
