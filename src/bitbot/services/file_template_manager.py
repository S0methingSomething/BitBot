"""A service for managing the bot's templates."""

from pathlib import Path

from ..interfaces.template_protocol import TemplateManagerProtocol


class FileTemplateManager(TemplateManagerProtocol):
    """Manages the bot's templates."""

    def __init__(self, template_dir: Path) -> None:
        """Initializes the FileTemplateManager."""
        self.template_dir = template_dir

    async def get_template(self, name: str) -> str:
        """Gets a template by name."""
        with (self.template_dir / name).open("r") as f:
            return f.read()
