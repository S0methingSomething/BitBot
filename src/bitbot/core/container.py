"""The central Service Container for Dependency Injection."""

from functools import cache

from ..services.config_service import ConfigService
from ..services.file_patcher_service import FilePatcherService
from ..services.github_service import GitHubService
from ..services.logging_service import LoggingService
from ..services.parsing_service import ParsingService
from ..services.praw_reddit_service import PrawRedditService
from ..services.release_management_service import ReleaseManagementService
from ..services.state_service import StateService
from ..services.abstract.reddit_service_abc import RedditServiceABC


class ServiceContainer:
    """A simple service container for managing application services.

    Uses lru_cache to ensure services are singletons.
    """

    @cache
    def logging_service(self) -> LoggingService:
        """Provide the LoggingService."""
        return LoggingService()

    @cache
    def config_service(self) -> ConfigService:
        """Provide the ConfigService."""
        return ConfigService(logging_service=self.logging_service())

    @cache
    def state_service(self) -> StateService:
        """Provide the StateService."""
        return StateService()

    @cache
    def github_service(self) -> GitHubService:
        """Provide the GitHubService."""
        config = self.config_service().get_config()
        return GitHubService(config.github)

    @cache
    def reddit_service(self) -> RedditServiceABC:
        """Provide the RedditService."""
        config = self.config_service().get_config()
        return PrawRedditService(config.reddit, self.logging_service())

    @cache
    def parsing_service(self) -> ParsingService:
        """Provide the ParsingService."""
        return ParsingService()

    @cache
    def file_patcher_service(self) -> FilePatcherService:
        """Provide the FilePatcherService."""
        return FilePatcherService()

    @cache
    def release_management_service(self) -> ReleaseManagementService:
        """Provide the ReleaseManagementService."""
        return ReleaseManagementService(
            logging_service=self.logging_service(),
            config_service=self.config_service(),
            github_service=self.github_service(),
            state_service=self.state_service(),
            parsing_service=self.parsing_service(),
            file_patcher_service=self.file_patcher_service(),
        )


# A global instance of the container
container = ServiceContainer()
