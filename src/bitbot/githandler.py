"""Core logic for handling GitHub releases."""

from typing import Optional

from bitbot.data.models import AppConfig, GitHubRelease
from bitbot.interfaces.github_manager import GitHubManagerProtocol
from bitbot.interfaces.state_manager import StateManagerProtocol


async def check_new_release(
    app: AppConfig,
    github_manager: GitHubManagerProtocol,
    state_manager: StateManagerProtocol,
) -> Optional[GitHubRelease]:
    """
    Checks for a new release of an application.

    Args:
        app: The application to check.
        github_manager: The GitHub manager to use.
        state_manager: The state manager to use.

    Returns:
        The new release, or None if no new release is found.
    """
    latest_release = await github_manager.get_latest_release(app.github_repo)
    if not latest_release:
        return None

    state = await state_manager.load_state()
    if latest_release.version in state.processed_releases:
        return None

    state.processed_releases.append(latest_release.version)
    await state_manager.save_state(state)

    return latest_release
