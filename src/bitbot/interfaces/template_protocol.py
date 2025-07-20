"""Protocol for the template management service."""

from typing import Protocol


class TemplateManagerProtocol(Protocol):
    """A protocol for managing the bot's templates."""

    async def get_template(self, name: str) -> str:
        """Gets a template by name."""
        ...
