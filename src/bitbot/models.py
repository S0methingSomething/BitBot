"""Pydantic models for BitBot runtime data structures."""

from beartype import beartype
from pydantic import BaseModel, ConfigDict, Field, field_validator


class App(BaseModel):
    """Configured application that BitBot manages."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    display_name: str = Field(alias="displayName")

    @field_validator("id", "display_name")
    @classmethod
    @beartype
    def validate_non_empty(cls, v: str) -> str:
        """Validate fields are non-empty."""
        if not v.strip():
            msg = "Field cannot be empty"
            raise ValueError(msg)
        return v

    @property
    def identifiers(self) -> frozenset[str]:
        """All identifiers that can match this app (case-insensitive)."""
        return frozenset({
            self.id,
            self.id.lower(),
            self.display_name,
            self.display_name.lower(),
        })


class ParsedRelease(BaseModel):
    """Parsed release metadata from a release body."""

    app_id: str | None = None
    version: str | None = None
    asset_name: str | None = None
    sha256: str | None = None

    @property
    def is_complete(self) -> bool:
        """Check if all required fields are present."""
        return self.app_id is not None and self.version is not None
