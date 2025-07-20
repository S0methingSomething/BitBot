"""Base test case for the bot's tests."""

import unittest
from pathlib import Path
from unittest.mock import MagicMock

import toml

from bitbot.data.models import BotState, Config
from bitbot.interfaces.config_protocol import ConfigManagerProtocol
from bitbot.interfaces.github_protocol import GitHubManagerProtocol
from bitbot.interfaces.reddit_protocol import RedditManagerProtocol
from bitbot.interfaces.state_protocol import StateManagerProtocol
from bitbot.interfaces.template_protocol import TemplateManagerProtocol


class BaseTestCase(unittest.TestCase):
    """A base test case for the bot's tests."""

    def setUp(self) -> None:
        """Sets up the test case."""
        with Path("tests/config.toml").open("r") as f:
            self.test_config = toml.load(f)

        self.mock_config_manager = MagicMock(spec=ConfigManagerProtocol)
        self.mock_state_manager = MagicMock(spec=StateManagerProtocol)
        self.mock_reddit_manager = MagicMock(spec=RedditManagerProtocol)
        self.mock_github_manager = MagicMock(spec=GitHubManagerProtocol)
        self.mock_template_manager = MagicMock(spec=TemplateManagerProtocol)

        self.mock_config_manager.load_config.return_value = Config(**self.test_config)
        self.mock_state_manager.load_state.return_value = BotState(
            **self.test_config["state"]["initial"]
        )
        self.mock_template_manager.get_template.side_effect = (
            lambda name: self.test_config["templates"][name]
        )
