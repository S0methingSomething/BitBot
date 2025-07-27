# src/bitbot/services/workspace.py
"""
A service for managing all file system interactions.
"""

import json
from ..core import ApplicationCore


class WorkspaceService:
    """Manages reading and writing files for the application."""

    def __init__(self, core: ApplicationCore):
        self._core = core

    @property
    def _broker(self):
        return self._core.broker

    async def get_template(self, template_name: str) -> str:
        """
        Reads a template file from the templates directory by making a
        request to the Execution Broker.
        """
        template_path = f"templates/{template_name}"
        return await self._broker.request_file_read(requester=self, path=template_path)

    async def get_state(self) -> dict:
        """
        Reads the bot's state from a JSON file.
        """
        state_path = "bot_state.json"
        content = await self._broker.request_file_read(requester=self, path=state_path)
        return json.loads(content)

    async def save_state(self, state: dict) -> None:
        """
        Saves the bot's state to a JSON file by making a request to the
        Execution Broker.
        """
        state_path = "bot_state.json"
        content = json.dumps(state, indent=2)
        await self._broker.request_file_write(
            requester=self, path=state_path, content=content
        )
