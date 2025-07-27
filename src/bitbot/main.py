# src/bitbot/main.py
"""
The command-line interface for BitBot.
"""

import asyncio
import typer
from rich import print

from .core import ApplicationCore
from .services.api_clients import ApiClientService
from .services.workspace import WorkspaceService
from .services.orchestrator import OrchestrationService
from .services.patcher import PatcherService

app = typer.Typer(
    name="bitbot",
    help="A Reddit bot for managing and posting GitHub releases.",
    add_completion=False,
    no_args_is_help=True,
)


@app.command("check-config")
def check_config(
    config_path: str = typer.Option(
        "config.toml", "--config", "-c", help="Path to the configuration file."
    ),
):
    """
    Loads and validates the configuration file, then prints it.
    This serves as the "Vertical Slice" prototype.
    """

    print(
        "[bold green]Attempting to load configuration from"
        f" '{config_path}'...[/bold green]"
    )
    try:
        core = ApplicationCore(config_path=config_path)
        print("[bold green]✅ Config loaded and validated successfully![/bold green]")
        print(core.settings.model_dump())
    except Exception as e:
        print(f"[bold red]❌ Error loading configuration: {e}[/bold red]")
        raise typer.Exit(1) from e


@app.command("manage-releases")
def manage_releases_command(
    config_path: str = typer.Option(
        "config.toml", "--config", "-c", help="Path to the configuration file."
    ),
):
    """
    Runs the main release management workflow.
    """
    print("[bold green]Starting BitBot release management...[/bold green]")
    try:
        core = ApplicationCore(config_path=config_path)
        api_clients = ApiClientService(core)
        workspace = WorkspaceService(core)
        patcher = PatcherService()
        orchestrator = OrchestrationService(core, api_clients, workspace, patcher)
        
        asyncio.run(orchestrator.manage_releases())
        
        print("[bold green]✅ Release management workflow completed successfully![/bold green]")
    except Exception as e:
        print(f"[bold red]❌ Error during release management: {e}[/bold red]")
        raise typer.Exit(1) from e


if __name__ == "__main__":
    app()
