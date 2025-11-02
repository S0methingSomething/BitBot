"""Patch command for BitBot CLI."""

import sys
from pathlib import Path

import typer
from beartype import beartype
from rich.console import Console

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.error_context import error_context
from patch_file import process_file

app = typer.Typer()
console = Console()


@beartype
@app.command()
def run(
    input_file: Path = typer.Argument(..., help="Input file to patch"),
    output_file: Path = typer.Argument(..., help="Output file path"),
) -> None:
    """Patch an asset file by decrypting, modifying, and re-encrypting."""
    with error_context(
        operation="patch_file", input_file=str(input_file), output_file=str(output_file)
    ):
        console.print(f"[cyan]Patching file:[/cyan] {input_file} → {output_file}")

        result = process_file(input_file, output_file)

        if result.is_err():
            console.print(f"[red]✗ Error:[/red] {result.error}")
            raise typer.Exit(code=1) from None

        console.print("[green]✓ Successfully patched file[/green]")


if __name__ == "__main__":
    app()
