"""Service for orchestrating Reddit posts."""

from datetime import datetime, timedelta, timezone

from ..models.changelog import Changelog
from .abstract.reddit_service_abc import RedditServiceABC
from .logging_service import LoggingService
from .reddit_post_service import RedditPostService
from .state_service import StateService


class RedditOrchestrationService:
    """Orchestrates the creation and updating of Reddit posts."""

    def __init__(
        self,
        logging_service: LoggingService,
        state_service: StateService,
        reddit_service: RedditServiceABC,
        reddit_post_service: RedditPostService,
    ):
        """Initialize the RedditOrchestrationService."""
        self._logger = logging_service
        self._state_service = state_service
        self._reddit_service = reddit_service
        self._reddit_post_service = reddit_post_service

    def manage_reddit_post(self, changelog: Changelog) -> None:
        """Manage the Reddit post based on the changelog and current state."""
        if not changelog.added and not changelog.updated and not changelog.removed:
            self._logger.info("No changes in the changelog. Nothing to post to Reddit.")
            return

        bot_state = self._state_service.load_bot_state()
        post = self._reddit_post_service.generate_post(changelog)

        self._logger.info(
            f"Checking post status. Active post ID: {bot_state.active_post_id}, Last post timestamp: {bot_state.last_major_post_timestamp}"
        )
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        should_create_new_post = (
            not bot_state.active_post_id
            or not bot_state.last_major_post_timestamp
            or bot_state.last_major_post_timestamp < seven_days_ago
        )
        self._logger.info(f"Should create new post? {should_create_new_post}")

        if should_create_new_post:
            self._logger.info("Creating a new Reddit post.")
            new_post_id = self._reddit_service.create_post(post)
            bot_state.active_post_id = new_post_id
            bot_state.last_major_post_timestamp = datetime.now(timezone.utc)
        elif bot_state.active_post_id:
            self._logger.info(f"Updating existing Reddit post: {bot_state.active_post_id}")
            self._reddit_service.update_post(bot_state.active_post_id, post)

        self._state_service.save_bot_state(bot_state)
        self._logger.info("Reddit post management complete.")
