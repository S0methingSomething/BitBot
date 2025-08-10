"""Pydantic models for representing the action to be taken for a Reddit post."""

from typing import Literal, Union

from pydantic import BaseModel


class CreatePost(BaseModel):
    """Represents the action to create a new post."""

    action: Literal["create"] = "create"


class UpdatePost(BaseModel):
    """Represents the action to update an existing post."""

    action: Literal["update"] = "update"
    post_id: str


class NoAction(BaseModel):
    """Represents that no action should be taken."""

    action: Literal["none"] = "none"


PostAction = Union[CreatePost, UpdatePost, NoAction]
"""A discriminated union of the possible post actions."""
