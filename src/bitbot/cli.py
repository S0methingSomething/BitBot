"""BitBot unified CLI using Typer + Rich."""

import typer
from rich.console import Console
from rich.traceback import install

# Install rich traceback handler
install(show_locals=True)

from bitbot.commands import check, gather, maintain, page, patch, post, release, sync
from bitbot.core.container import setup_container

# Create CLI app
app = typer.Typer(
    name="bitbot",
    help="BitBot - Automated release management and Reddit posting",
    add_completion=False,
)

# Create console for rich output
console = Console()

# Register commands
app.add_typer(post.app, name="post", help="Post releases to Reddit")
app.add_typer(check.app, name="check", help="Check Reddit comments for feedback")
app.add_typer(release.app, name="release", help="Manage GitHub releases")
app.add_typer(sync.app, name="sync", help="Sync Reddit state")
app.add_typer(patch.app, name="patch", help="Patch asset files")
app.add_typer(page.app, name="page", help="Generate landing page")
app.add_typer(gather.app, name="gather", help="Gather post data")
app.add_typer(maintain.app, name="maintain", help="Maintain releases")


@app.callback()
def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
) -> None:
    """BitBot CLI - Automated release management and Reddit posting."""
    # Initialize DI container
    container_result = setup_container()
    if container_result.is_err():
        console.print(f"[red]✗ Error:[/red] {container_result.error}")
        raise typer.Exit(code=1)

    # Store container and console in context for commands
    ctx.obj = {
        "container": container_result.unwrap(),
        "console": console,
        "verbose": verbose,
    }


if __name__ == "__main__":
    app()
