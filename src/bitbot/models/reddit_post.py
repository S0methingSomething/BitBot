"""Pydantic models for a Reddit post."""

from pydantic import BaseModel


class RedditPost(BaseModel):
    """Represents a Reddit post to be submitted."""

    title: str
    body: str
