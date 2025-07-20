"""Property-based tests for the bot's core logic."""

import asyncio

from hypothesis import given
from hypothesis import strategies as st

from bitbot import comments
from bitbot.data.models import BotState, RedditPost

from .base import BaseTestCase


@st.composite
def bot_states(draw: st.DrawFn) -> BotState:
    """Generate random BotState objects."""
    return BotState(
        activePostId=draw(st.text(min_size=1)),
        lastCheckTimestamp=draw(st.datetimes()).isoformat() + "Z",
        currentIntervalSeconds=draw(st.integers(min_value=0, max_value=100000000)),
        lastCommentCount=draw(st.integers(min_value=0)),
    )


@st.composite
def reddit_posts(draw: st.DrawFn) -> RedditPost:
    """Generate random RedditPost objects."""
    return RedditPost(
        id=draw(st.text(min_size=1)),
        title=draw(st.text()),
        body=draw(st.text()),
        url=draw(st.text()),
    )


class TestProperties(BaseTestCase):
    """Property-based tests for the bot's core logic."""

    @given(state=bot_states(), post=reddit_posts())
    def test_check_comments_property(self, state: BotState, post: RedditPost) -> None:
        """Test that check_comments always produces a valid status."""
        self.mock_state_manager.load_state.return_value = state
        self.mock_reddit_manager.get_post_by_id.return_value = post
        self.mock_reddit_manager.get_comments.return_value = []

        result = asyncio.run(
            comments.check_comments(
                config_manager=self.mock_config_manager,
                state_manager=self.mock_state_manager,
                reddit_manager=self.mock_reddit_manager,
            )
        )
        self.assertIsInstance(result, bool)
