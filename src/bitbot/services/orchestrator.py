# src/bitbot/services/orchestrator.py
"""
The main service for orchestrating high-level workflows.
"""

from ..core import ApplicationCore
from .api_clients import ApiClientService
from .workspace import WorkspaceService
from .patcher import PatcherService
from ..domain.models import RedditPost


class OrchestrationService:
    """
    The "brain" of the application, responsible for executing the main
    release workflow.
    """

    def __init__(
        self,
        core: ApplicationCore,
        api_clients: ApiClientService,
        workspace: WorkspaceService,
        patcher: PatcherService,
    ):
        self._core = core
        self._api_clients = api_clients
        self._workspace = workspace
        self._patcher = patcher

    async def manage_releases(self) -> None:
        """
        Executes the full workflow to check for, patch, and post new releases.
        """
        self._core.logger.info("Starting release management workflow.")

        # 1. Get latest releases from source
        source_releases = await self._api_clients.github.get_latest_releases()
        if not source_releases:
            self._core.logger.info("No releases found in source repository.")
            return

        # 2. Get last known release from state
        # This is a simplified state management. A real implementation would be more robust.
        try:
            state = await self._workspace.get_state()
            last_known_tag = state.get("last_known_release_tag")
        except FileNotFoundError:
            last_known_tag = None
        self._core.logger.info(f"Last known release tag: {last_known_tag}")

        # 3. Filter to new releases
        new_releases = []
        if last_known_tag:
            for release in source_releases:
                if release.tag_name == last_known_tag:
                    break
                new_releases.append(release)
            new_releases.reverse()  # Process oldest to newest
        else:
            # If no state, consider the latest release as the only new one
            new_releases.append(source_releases[0])
        
        if not new_releases:
            self._core.logger.info("No new releases to process.")
            return
        
        self._core.logger.info(f"Found {len(new_releases)} new releases.")

        # 4. Process each new release
        for release in new_releases:
            # In a real implementation, we would patch the release body here.
            patched_body = self._patcher.patch_file_content(release.body)
            release.body = patched_body
            
            # 4a. Create the consolidated GitHub release
            new_github_release = await self._api_clients.github.create_release(release)
            self._core.logger.info(f"Created GitHub release: {new_github_release.html_url}")

            # 4b. Create and submit the Reddit post
            post_title = self._core.settings.reddit.post_title_template.format(
                version=new_github_release.tag_name
            )
            post_body = f"New release {new_github_release.tag_name} is out! Find it here: {new_github_release.html_url}"
            
            reddit_post = RedditPost(title=post_title, selftext=post_body, url=new_github_release.html_url)
            
            submitted_post = await self._api_clients.reddit.submit_post(reddit_post)
            self._core.logger.info(f"Submitted Reddit post: {submitted_post.id}")

            # 5. Save the new state
            await self._workspace.save_state({"last_known_release_tag": new_github_release.tag_name})
            self._core.logger.info(f"Updated state with new release tag: {new_github_release.tag_name}")

        self._core.logger.info("Release management workflow finished.")
