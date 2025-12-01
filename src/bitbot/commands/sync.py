"""Sync command for BitBot CLI.

This command verifies Reddit state and reports issues.
It does NOT parse versions from Reddit - local DB is the source of truth
for what we've announced.
"""

from typing import TYPE_CHECKING

import typer
from beartype import beartype
from returns.result import Failure, Success
from rich.progress import Progress, SpinnerColumn, TextColumn

from bitbot.core import db
from bitbot.core.credentials import get_reddit_username
from bitbot.core.error_context import error_context
from bitbot.core.error_logger import LogLevel
from bitbot.core.errors import BitBotError
from bitbot.reddit.client import init_reddit
from bitbot.reddit.state import get_current_post, verify_state

if TYPE_CHECKING:
    from rich.console import Console

    from bitbot.core.container import Container

app = typer.Typer()


@beartype
@app.command()
def run(
    ctx: typer.Context,
    fix: bool = typer.Option(  # noqa: FBT001
        default=False, help="Auto-fix issues (clear invalid post ID)"
    ),
) -> None:
    """Verify Reddit state and report issues.

    This checks:
    - Does the active post exist on Reddit?
    - Is it accessible (not removed)?
    - Does content hash match what we stored?

    Use --fix to automatically clear invalid state.
    """
    with error_context(operation="sync"):
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
                progress.add_task(description="Verifying Reddit state...", total=None)

                # Initialize
                db.init()
                username = get_reddit_username()
                account_result = db.get_or_create_account(username, config.reddit.subreddit)
                if isinstance(account_result, Failure):
                    raise BitBotError(f"DB error: {account_result.failure()}")
                account_id = account_result.unwrap()

                # Init Reddit
                reddit_result = init_reddit(config)
                if isinstance(reddit_result, Failure):
                    raise BitBotError(f"Reddit error: {reddit_result.failure()}")
                reddit = reddit_result.unwrap()

                # Get local state
                meta_result = db.get_account(account_id)
                if isinstance(meta_result, Failure):
                    raise BitBotError(f"Failed to get account: {meta_result.failure()}")

                meta = meta_result.unwrap()
                active_post_id = meta.get("active_post_id")
                stored_hash = meta.get("content_hash")

                versions_result = db.get_posted_versions(account_id)
                announced = versions_result.unwrap() if isinstance(versions_result, Success) else {}

                # Report local state
                console.print("\n[bold]Local State:[/bold]")
                console.print(f"  Active post ID: {active_post_id or '(none)'}")
                console.print(f"  Content hash: {stored_hash or '(none)'}")
                console.print(f"  Announced versions: {len(announced)}")
                for app_id, version in sorted(announced.items()):
                    console.print(f"    - {app_id}: v{version}")

                if not active_post_id:
                    console.print("\n[green]✓[/green] No active post - state is clean")
                    return

                # Verify against Reddit
                console.print("\n[bold]Reddit State:[/bold]")
                state_check = verify_state(reddit, account_id)

                if state_check.post_ok:
                    console.print(f"  Post exists: [green]Yes[/green]")
                else:
                    console.print(f"  Post exists: [red]No[/red]")

                if state_check.current_hash:
                    console.print(f"  Current hash: {state_check.current_hash}")

                if state_check.content_matches:
                    console.print(f"  Content matches: [green]Yes[/green]")
                else:
                    console.print(f"  Content matches: [yellow]No[/yellow]")

                # Report issues
                if state_check.issues:
                    console.print("\n[bold yellow]Issues:[/bold yellow]")
                    for issue in state_check.issues:
                        console.print(f"  ⚠ {issue}")

                    if fix:
                        console.print("\n[bold]Fixing issues...[/bold]")
                        if not state_check.post_ok:
                            # Clear invalid post ID
                            db.update_account(account_id, active_post_id="", content_hash="")
                            console.print("  [green]✓[/green] Cleared invalid post ID")
                        console.print("\n[green]✓[/green] Issues fixed - run 'post' to create new post")
                    else:
                        console.print("\n[dim]Use --fix to auto-fix issues, or 'post --reset' to start fresh[/dim]")
                else:
                    console.print("\n[green]✓[/green] State is consistent")

                # Also show what's on Reddit
                post_result = get_current_post(reddit, config)
                if isinstance(post_result, Success) and post_result.unwrap():
                    status = post_result.unwrap()
                    console.print(f"\n[bold]Latest Reddit Post:[/bold]")
                    console.print(f"  ID: {status.post_id}")
                    console.print(f"  URL: {status.post_url}")
                    console.print(f"  Accessible: {'Yes' if status.accessible else 'No'}")

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
