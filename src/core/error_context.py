"""Error context manager for propagating context through call stack."""

import threading
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

import deal
from beartype import beartype

_context_stack: threading.local = threading.local()


@deal.post(lambda result: isinstance(result, dict))  # type: ignore[misc]
@beartype  # type: ignore[misc]
def get_error_context() -> dict[str, Any]:
    """Get current error context."""
    if not hasattr(_context_stack, "stack"):
        _context_stack.stack = []

    merged: dict[str, Any] = {}
    for ctx in _context_stack.stack:
        merged.update(ctx)
    return merged


@deal.pre(lambda **context: context is not None)  # type: ignore[misc]
@contextmanager
@beartype  # type: ignore[misc]
def error_context(**context: Any) -> Generator[None, None, None]:
    """Context manager for adding error context."""
    if not hasattr(_context_stack, "stack"):
        _context_stack.stack = []

    _context_stack.stack.append(context)
    try:
        yield
    finally:
        _context_stack.stack.pop()
