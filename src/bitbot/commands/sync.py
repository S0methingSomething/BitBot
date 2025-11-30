"""Sync command for BitBot CLI."""

from typing import TYPE_CHECKING

import typer
from beartype import beartype
from returns.result import Failure
from rich.progress import Progress, SpinnerColumn, TextColumn

from bitbot.core import db
from bitbot.core.credentials import get_reddit_username
from bitbot.core.error_context import error_context
from bitbot.core.error_logger import LogLevel
from bitbot.core.errors import BitBotError
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
    """Sync Reddit state with local database."""
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

                # Initialize database
                db.init()

                # Get account
                username = get_reddit_username()
                account_result = db.get_or_create_account(username, config.reddit.subreddit)
                if isinstance(account_result, Failure):
                    error = BitBotError(f"DB error: {account_result.failure()}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {error.message}")
                    raise typer.Exit(code=1) from None
                account_id = account_result.unwrap()

                # Initialize Reddit client
                reddit_result = init_reddit(config)
                if isinstance(reddit_result, Failure):
                    error = BitBotError(f"Reddit init failed: {reddit_result.failure()}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {error.message}")
                    raise typer.Exit(code=1) from None

                reddit = reddit_result.unwrap()

                # Get bot posts
                posts_result = get_bot_posts(reddit, config)
                if isinstance(posts_result, Failure):
                    error = BitBotError(f"Failed to get posts: {posts_result.failure()}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {error.message}")
                    raise typer.Exit(code=1) from None

                bot_posts = posts_result.unwrap()

                if not bot_posts:
                    console.print("[yellow]⚠ No posts found on Reddit[/yellow]")
                    return

                # Get latest post
                latest_post = bot_posts[0]

                # Parse versions from post
                versions = parse_versions_from_post(latest_post, config)

                # Update database
                db.update_account(account_id, active_post_id=latest_post.id)
                db.add_post_id(account_id, latest_post.id)

                for app_id, version in versions.items():
                    db.set_posted_version(account_id, app_id, version)

                if versions:
                    msg = f"Synced {len(versions)} version(s) from post {latest_post.id}"
                    console.print(f"[green]✓[/green] {msg}")
                else:
                    msg = f"Synced post {latest_post.id} (no versions parsed)"
                    console.print(f"[yellow]⚠[/yellow] {msg}")

        except Exception as e:
            error = BitBotError(f"Unexpected error: {e}")
            logger.log_error(error, LogLevel.CRITICAL)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
