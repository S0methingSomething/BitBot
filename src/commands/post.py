"""Post command for BitBot CLI."""

import sys
from datetime import datetime, timezone
from pathlib import Path

import typer
from beartype import beartype
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import load_config
from core.error_context import error_context
from core.error_logger import LogLevel, get_logger
from core.errors import BitBotError
from core.release_queue import load_pending_releases
from core.state import load_bot_state, save_bot_state
from reddit.client import init_reddit
from reddit.posting.poster import post_new_release

app = typer.Typer()
console = Console()
logger = get_logger(console=console)


@beartype
@app.command()
def run(
    page_url: str = typer.Option(None, "--page-url", help="Landing page URL to post"),
) -> None:
    """Post new releases to Reddit."""
    with error_context(command="post", page_url=page_url):
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                progress.add_task(description="Posting to Reddit...", total=None)

                # Load config
                config_result = load_config()
                if config_result.is_err():
                    error = BitBotError(f"Config error: {config_result.error}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {config_result.error}")
                    raise typer.Exit(code=1) from None
                config = config_result.unwrap()

                # Check for pending releases
                queue_result = load_pending_releases()
                if queue_result.is_err():
                    error = BitBotError(f"Queue error: {queue_result.error}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {queue_result.error}")
                    raise typer.Exit(code=1) from None
                pending = queue_result.unwrap()

                if not pending:
                    console.print("[yellow][i] No releases to post[/yellow]")
                    return

                # Generate title
                post_identifier = config["reddit"].get("postIdentifier", "[BitBot]")
                date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                title = f"{post_identifier} New Updates - {date_str}"

                # Generate body
                if page_url:
                    body = f"New updates available!\n\n[Download Page]({page_url})"
                else:
                    body = "New updates available! Check the releases page for downloads."

                # Init Reddit
                reddit_result = init_reddit(config)
                if reddit_result.is_err():
                    error = BitBotError(f"Reddit error: {reddit_result.error}")
                    logger.log_error(error, LogLevel.ERROR)
                    console.print(f"[red]✗ Error:[/red] {reddit_result.error}")
                    raise typer.Exit(code=1) from None
                reddit = reddit_result.unwrap()

                # Post
                submission = post_new_release(reddit, title, body, config)

                # Update state with post ID tracking
                state_result = load_bot_state()
                if state_result.is_ok():
                    state = state_result.unwrap()
                    state.active_post_id = submission.id
                    # Track all post IDs for robust detection
                    if submission.id not in state.all_post_ids:
                        state.all_post_ids.append(submission.id)
                    save_result = save_bot_state(state)
                    if save_result.is_err():
                        console.print("[yellow]⚠[/yellow] Failed to update state")

                console.print(f"[green]✓[/green] Posted to Reddit: {submission.url}")

        except BitBotError as e:
            logger.log_error(e, LogLevel.ERROR)
            console.print(f"[red]✗ Error:[/red] {e.message}")
            raise typer.Exit(code=1) from None
        except Exception as e:
            error = BitBotError(f"Unexpected error: {e}")
            logger.log_error(error, LogLevel.CRITICAL)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
