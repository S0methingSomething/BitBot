"""BitBot unified CLI using Typer + Rich."""

import logging

import typer
from rich.logging import RichHandler
from rich.traceback import install

# Install rich traceback handler
install(show_locals=True)

from bitbot.commands import check, gather, maintain, page, patch, post, release, sync
from bitbot.core.container import Container

__version__ = "1.0.0"

# Create CLI app
app = typer.Typer(
    name="bitbot",
    help="BitBot - Automated release management and Reddit posting",
    add_completion=False,
)

# Create container
container = Container()


def configure_logging(*, verbose: bool = False) -> None:
    """Configure logging with RichHandler."""
    level = logging.DEBUG if verbose else logging.INFO
    console = container.console()
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[RichHandler(console=console, rich_tracebacks=True, show_path=False)],
    )


# Register commands
app.add_typer(post.app, name="post", help="Post releases to Reddit")
app.add_typer(check.app, name="check", help="Check Reddit comments for feedback")
app.add_typer(release.app, name="release", help="Manage GitHub releases")
app.add_typer(sync.app, name="sync", help="Sync Reddit state")
app.add_typer(patch.app, name="patch", help="Patch asset files")
app.add_typer(page.app, name="page", help="Generate landing page")
app.add_typer(gather.app, name="gather", help="Gather post data")
app.add_typer(maintain.app, name="maintain", help="Maintain releases")


@app.command()
def version() -> None:
    """Show BitBot version."""
    console = container.console()
    console.print(f"BitBot v{__version__}")


@app.callback()
def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
) -> None:
    """BitBot CLI - Automated release management and Reddit posting."""
    # Configure logging
    configure_logging(verbose=verbose)

    # Store container in context for commands
    ctx.ensure_object(dict)
    ctx.obj["container"] = container
    ctx.obj["console"] = container.console()


if __name__ == "__main__":
    app()
