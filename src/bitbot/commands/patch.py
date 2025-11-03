"""Patch command for BitBot CLI."""

from pathlib import Path
from typing import TYPE_CHECKING

import typer
from beartype import beartype

from bitbot.core.error_context import error_context
from bitbot.core.error_logger import LogLevel
from bitbot.core.errors import BitBotError
from bitbot.patch_file import process_file

if TYPE_CHECKING:
    from rich.console import Console

    from bitbot.core.container import Container

app = typer.Typer()


@beartype
@app.command()
def run(
    ctx: typer.Context,
    input_file: Path = typer.Argument(..., help="Input file to patch"),
    output_file: Path = typer.Argument(..., help="Output file path"),
) -> None:
    """Patch an asset file by decrypting, modifying, and re-encrypting."""
    container: Container = ctx.obj["container"]
    console: Console = container.console()
    logger = container.logger()

    with error_context(
        operation="patch_file", input_file=str(input_file), output_file=str(output_file)
    ):
        try:
            console.print(f"[cyan]Patching file:[/cyan] {input_file} → {output_file}")

            result = process_file(input_file, output_file)

            if result.is_err():
                error = BitBotError(f"Patch error: {result.error}")
                logger.log_error(error, LogLevel.ERROR)
                console.print(f"[red]✗ Error:[/red] {result.error}")
                raise typer.Exit(code=1) from None

            console.print("[green]✓ Successfully patched file[/green]")

        except Exception as e:
            error = BitBotError(f"Unexpected error: {e}")
            logger.log_error(error, LogLevel.CRITICAL)
            console.print(f"[red]✗ Error:[/red] {e}")
            raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
