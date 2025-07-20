# Basic type stubs for asyncpraw
from typing import AsyncGenerator, List, TypeVar

T = TypeVar("T")

class Reddit:
    def __init__(self, **kwargs: T) -> None: ...
    async def submission(self, submission_id: str) -> "Submission": ...
    @property
    def user(self) -> "User": ...
    async def subreddit(self, name: str) -> "Subreddit": ...
    async def close(self) -> None: ...

class Submission:
    id: str
    title: str
    selftext: str
    shortlink: str
    comments: "CommentForest"
    async def edit(self, body: str) -> None: ...

class Comment:
    body: str

class CommentForest:
    async def replace_more(self, limit: int) -> None: ...
    async def list(self) -> List[Comment]: ...

class User:
    async def me(self) -> "Redditor": ...

class Redditor:
    @property
    def submissions(self) -> "Submissions": ...

class Submissions:
    def new(self, limit: int) -> AsyncGenerator[Submission, None]: ...

class Subreddit:
    async def submit(self, title: str, selftext: str) -> Submission: ...
