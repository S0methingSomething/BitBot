"""Post command for BitBot CLI."""

import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

app = typer.Typer()
console = Console()


@app.command()
def run(
    page_url: str = typer.Option(None, "--page-url", help="Custom landing page URL"),
) -> None:
    """Post new releases to Reddit."""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(description="Posting to Reddit...", total=None)
            
            # Import here to avoid circular imports
            from post_to_reddit import main as post_main
            
            # Temporarily override sys.argv for the old script
            old_argv = sys.argv
            sys.argv = ["post_to_reddit"]
            if page_url:
                sys.argv.extend(["--page-url", page_url])
            
            try:
                post_main()
                console.print("[green]✓ Successfully posted to Reddit[/green]")
            except SystemExit as e:
                if e.code != 0:
                    console.print("[red]✗ Failed to post to Reddit[/red]")
                    raise typer.Exit(code=e.code)
            finally:
                sys.argv = old_argv
                
    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
