"""Error context manager for propagating context through call stack."""

import threading
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

from beartype import beartype

_context_stack: threading.local = threading.local()


@beartype
def get_error_context() -> dict[str, Any]:
    """Get current error context."""
    if not hasattr(_context_stack, "stack"):
        _context_stack.stack = []

    merged: dict[str, Any] = {}
    for ctx in _context_stack.stack:
        merged.update(ctx)
    return merged


@contextmanager
@beartype
# Any: Accepts arbitrary context kwargs
def error_context(**context: Any) -> Generator[None]:
    """Context manager for adding error context."""
    if not hasattr(_context_stack, "stack"):
        _context_stack.stack = []

    _context_stack.stack.append(context)
    try:
        yield
    finally:
        if _context_stack.stack:
            _context_stack.stack.pop()
