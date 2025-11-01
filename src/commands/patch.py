"""Patch command for BitBot CLI."""

import sys
from pathlib import Path

import typer
from beartype import beartype
from rich.console import Console

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.error_context import error_context
from core.error_logger import get_logger
from patch_file import process_file

app = typer.Typer()
console = Console()
logger = get_logger(__name__)


@beartype
@app.command()
def run(
    input_file: Path = typer.Argument(..., help="Input file to patch"),
    output_file: Path = typer.Argument(..., help="Output file path"),
) -> None:
    """Patch an asset file by decrypting, modifying, and re-encrypting."""
    with error_context("patch_file", input_file=str(input_file), output_file=str(output_file)):
        logger.info("Patching file: %s → %s", input_file, output_file)
        console.print(f"[cyan]Patching file:[/cyan] {input_file} → {output_file}")

        result = process_file(input_file, output_file)

        if result.is_err():
            logger.error("Patch failed: %s", result.error)
            console.print(f"[red]✗ Error:[/red] {result.error}")
            raise typer.Exit(code=1) from None

        logger.info("Successfully patched file")
        console.print("[green]✓ Successfully patched file[/green]")


if __name__ == "__main__":
    app()
