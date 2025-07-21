"""Stubs for asyncpraw."""

from typing import Any, Coroutine, Dict

from .models.submission import Submission

class Redditor:
    """Stub for the Redditor class."""

    ...

class User:
    """Stub for the User class."""

    def me(self) -> Coroutine[Any, Any, Redditor | None]: ...

class Subreddit:
    """Stub for the Subreddit class."""

    def submit(self, title: str, selftext: str) -> Coroutine[Any, Any, Submission]: ...

class Reddit:
    """Stub for the Reddit class."""

    user: User

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        username: str,
        password: str,
        **kwargs: Dict[str, Any],
    ) -> None: ...
    def subreddit(self, name: str) -> Coroutine[Any, Any, Subreddit]: ...

