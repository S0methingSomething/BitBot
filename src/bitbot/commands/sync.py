"""Sync command for BitBot CLI."""

from typing import TYPE_CHECKING

import typer
from beartype import beartype
from rich.progress import Progress, SpinnerColumn, TextColumn

from bitbot.core.error_context import error_context
from bitbot.core.error_logger import LogLevel
from bitbot.core.errors import BitBotError
from bitbot.core.state import load_bot_state, save_bot_state
from bitbot.reddit.client import init_reddit
from bitbot.reddit.parser import parse_versions_from_post
from bitbot.reddit.posts import get_bot_posts

if TYPE_CHECKING:
    from rich.console import Console

    from bitbot.core.container import Container

app = typer.Typer()


@beartype
@app.command()
def run(ctx: typer.Context) -> None:
    """Sync Reddit state with local bot_state.json."""
    with error_context(operation="sync_reddit_history"):
        try:
            container: Container = ctx.obj["container"]
            console: Console = container.console()
            logger = container.logger()
            config = container.config()

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                progress.add_task(description="Syncing Reddit state...", total=None)

                # Initialize Reddit client
                reddit_result = init_reddit(config)
                if reddit_result.is_err():
                    error = BitBotError(f"Reddit init failed: {reddit_result.unwrap_err()}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {error.message}")
                    raise typer.Exit(code=1) from None

                reddit = reddit_result.unwrap()

                # Get bot posts
                posts_result = get_bot_posts(reddit, config)
                if posts_result.is_err():
                    error = BitBotError(f"Failed to get posts: {posts_result.unwrap_err()}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {error.message}")
                    raise typer.Exit(code=1) from None

                bot_posts = posts_result.unwrap()

                # Exit gracefully if no posts
                if not bot_posts:
                    console.print("[yellow]⚠ No posts found on Reddit[/yellow]")
                    return

                # Get latest post
                latest_post = bot_posts[0]

                # Parse versions from post
                versions = parse_versions_from_post(latest_post, config)

                if not isinstance(versions, dict):
                    error = BitBotError("Invalid versions data from post")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {error.message}")
                    raise typer.Exit(code=1) from None

                # Load bot state
                state_result = load_bot_state()
                if state_result.is_err():
                    error = BitBotError(f"Failed to load state: {state_result.unwrap_err()}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {error.message}")
                    raise typer.Exit(code=1) from None

                bot_state = state_result.unwrap()

                # Update state - preserve existing online fields, update versions
                if not isinstance(bot_state.online, dict):
                    bot_state.online = {}
                bot_state.online.update(versions)
                bot_state.active_post_id = latest_post.id

                # Add to all_post_ids if not present
                if latest_post.id not in bot_state.all_post_ids:
                    bot_state.all_post_ids.append(latest_post.id)

                # Save state
                save_result = save_bot_state(bot_state)
                if save_result.is_err():
                    error = BitBotError(f"Failed to save state: {save_result.unwrap_err()}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {error.message}")
                    raise typer.Exit(code=1) from None

                if versions:
                    msg = f"Synced {len(versions)} version(s) from post {latest_post.id}"
                    console.print(f"[green]✓[/green] {msg}")
                else:
                    msg = f"Synced post {latest_post.id} (no versions parsed - check post format)"
                    console.print(f"[yellow]⚠[/yellow] {msg}")

        except Exception as e:
            error = BitBotError(f"Unexpected error: {e}")
            logger.log_error(error, LogLevel.CRITICAL)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
