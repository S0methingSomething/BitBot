"""Service for orchestrating Reddit posts.

This service is responsible for the high-level logic of deciding whether to create
a new Reddit post or update an existing one based on the provided changelog and
the bot's current state. It uses a state-machine-like approach to separate
the decision-making logic from the action-taking logic.
"""

from datetime import datetime, timedelta, timezone

from ..models.changelog import Changelog
from ..models.post_action import CreatePost, NoAction, PostAction, UpdatePost
from ..models.state import BotState
from .abstract.reddit_service_abc import RedditServiceABC
from .logging_service import LoggingService
from .reddit_post_service import RedditPostService
from .state_service import StateService


class RedditOrchestrationService:
    """Orchestrates the creation and updating of Reddit posts."""

    _POST_TTL_DAYS = 7

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

    def _determine_action(self, state: BotState) -> PostAction:
        """
        Determines the action to take based on the current state. This is the
        core decision-making logic of the service.
        """
        print("\n\n--- ENTERING _determine_action ---")
        print(f"RECEIVED STATE OBJECT: {state}")
        print(f"  --> state.active_post_id: {state.active_post_id} (type: {type(state.active_post_id)})")
        print(
            f"  --> state.last_major_post_timestamp: {state.last_major_post_timestamp} (type: {type(state.last_major_post_timestamp)})"
        )

        print("\nCHECK 1: Checking for missing data...")
        if not state.active_post_id or not state.last_major_post_timestamp:
            print("  --> RESULT: TRUE. One or more values are missing.")
            print("DECISION: CREATE POST")
            print("--- EXITING _determine_action ---\n")
            return CreatePost()
        print("  --> RESULT: FALSE. All data is present.")

        print("\nCHECK 2: Checking timestamp against TTL...")
        now = datetime.now(timezone.utc)
        ttl_limit = now - timedelta(days=self._POST_TTL_DAYS)
        print(f"  --> Current time (UTC): {now.isoformat()}")
        print(f"  --> TTL limit ({self._POST_TTL_DAYS} days ago): {ttl_limit.isoformat()}")
        print(f"  --> Post timestamp:       {state.last_major_post_timestamp.isoformat()}")

        is_older = state.last_major_post_timestamp < ttl_limit
        print(f"  --> IS post_timestamp < ttl_limit?: {is_older}")

        if is_older:
            print("  --> RESULT: TRUE. Post is older than TTL.")
            print("DECISION: CREATE POST")
            print("--- EXITING _determine_action ---\n")
            return CreatePost()

        print("  --> RESULT: FALSE. Post is recent.")
        print("DECISION: UPDATE POST")
        print("--- EXITING _determine_action ---\n")
        return UpdatePost(post_id=state.active_post_id)

    def manage_reddit_post(self, changelog: Changelog) -> None:
        """
        Manages the Reddit post based on the changelog and current state.
        This method acts as a dispatcher, executing the action determined by
        the internal state.
        """
        if not changelog.added and not changelog.updated and not changelog.removed:
            self._logger.info("No changes in changelog, taking no action.")
            return

        bot_state = self._state_service.load_bot_state()
        action = self._determine_action(bot_state)

        match action:
            case CreatePost():
                self._logger.info("Executing action: Create new post.")
                post = self._reddit_post_service.generate_post(changelog)
                new_post_id = self._reddit_service.create_post(post)
                bot_state.active_post_id = new_post_id
                bot_state.last_major_post_timestamp = datetime.now(timezone.utc)
                self._state_service.save_bot_state(bot_state)
                self._logger.info(f"Successfully created post {new_post_id} and saved state.")

            case UpdatePost(post_id=post_id):
                self._logger.info(f"Executing action: Update existing post {post_id}.")
                post = self._reddit_post_service.generate_post(changelog)
                self._reddit_service.update_post(post_id, post)
                self._logger.info(f"Successfully updated post {post_id}.")

            case NoAction():
                self._logger.info("Executing action: None.")
                pass
