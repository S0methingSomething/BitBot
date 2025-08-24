#!/usr/bin/env python3
"""Main entry point for BitBot - runs the complete production workflow."""

import sys
import traceback
from pathlib import Path
from typing import Any

# Add the src directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from broker import ComponentBroker
from check_comments import main as comment_checker_main
from config_loader import load_config
from credentials import setup_credentials
from dry_run import is_dry_run, log_dry_run_status
from logging_config import get_logger, print_panel, print_rich
from page_generator import main as page_generator_main
from post_to_reddit import run_poster
from reddit_release_manager import main as release_manager_main

console = Console()
logger = get_logger(__name__)


def _run_workflow_components() -> None:
    """Run the actual workflow components."""
    # Run the actual workflow components
    print_rich("\n[bold]📥 Step 1: Checking for new source releases...[/bold]")
    print_rich("[blue]   • Running release manager...[/blue]")
    release_manager_main()

    # Import and run page generator
    print_rich("\n[bold]📄 Step 2: Generating landing page...[/bold]")
    print_rich("[blue]   • Running page generator...[/blue]")
    page_generator_main()

    # Import and run Reddit poster
    print_rich("\n[bold]📢 Step 3: Posting to Reddit...[/bold]")
    print_rich("[blue]   • Running Reddit poster...[/blue]")
    run_poster()

    # Import and run comment checker
    print_rich("\n[bold]👀 Step 4: Starting comment monitoring...[/bold]")
    print_rich("[blue]   • Running comment checker...[/blue]")
    comment_checker_main()


def run_complete_workflow() -> None:
    """Run the complete BitBot workflow."""
    print_panel("[bold blue]🚀 BitBot Workflow[/bold blue]")

    # Load configuration and setup credentials
    try:
        config = load_config()
        auto_save = getattr(config.auth, "auto_save", False)
        auto_load = getattr(config.auth, "auto_load", False)
        setup_credentials(auto_save=auto_save, auto_load=auto_load)
        log_dry_run_status()
    except Exception as e:
        print_rich(f"[bold red]❌ Configuration error:[/bold red] {e}")
        sys.exit(1)

    # Check dry-run status
    if is_dry_run():
        print_rich(
            "[yellow]⚠️  Dry-run mode is enabled - no actual posts will be made[/yellow]"
        )
    else:
        print_rich(
            "[green]✅ Production mode - all operations will be performed[/green]"
        )

    try:
        _run_workflow_components()
        print_rich("\n[bold green]✅ BitBot workflow completed![/bold green]")
    except Exception as e:
        print_rich(f"[bold red]❌ Workflow error:[/bold red] {e}")
        print_rich(f"[red]{traceback.format_exc()}[/red]")
        sys.exit(1)


def run_actual_workflow() -> None:
    """Run the actual BitBot workflow with real operations."""
    print_panel("[bold blue]🚀 BitBot Production Workflow[/bold blue]")

    # Load configuration and setup credentials
    try:
        config = load_config()
        auto_save = getattr(config.auth, "auto_save", False)
        auto_load = getattr(config.auth, "auto_load", False)
        setup_credentials(auto_save=auto_save, auto_load=auto_load)
        log_dry_run_status()
    except Exception as e:
        print_rich(f"[bold red]❌ Configuration error:[/bold red] {e}")
        sys.exit(1)

    # Check dry-run status
    if is_dry_run():
        print_rich(
            "[yellow]⚠️  Dry-run mode is enabled - no actual posts will be made[/yellow]"
        )
    else:
        print_rich(
            "[green]✅ Production mode - all operations will be performed[/green]"
        )

    try:
        _run_workflow_components()
        print_rich("\n[bold green]✅ BitBot workflow completed![/bold green]")
    except Exception as e:
        print_rich(f"[bold red]❌ Workflow error:[/bold red] {e}")
        print_rich(f"[red]{traceback.format_exc()}[/red]")
        sys.exit(1)


def _show_communication_log(broker: Any) -> None:
    """Show the communication log."""
    console.print("\n[bold]📋 Communication Log:[/bold]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Component", style="dim")
    table.add_column("Method")
    table.add_column("Service")
    table.add_column("Reason")
    table.add_column("Time", style="dim")

    for entry in broker.get_communication_log():
        table.add_row(
            f"{entry['component']}",
            entry["method"],
            entry["service"],
            entry["reason"],
            entry["timestamp"].split("T")[1].split(".")[0],  # Just show time part
        )

    console.print(table)


def _show_next_steps() -> None:
    """Show next steps."""
    console.print("\n[bold blue]Foundation is ready![/bold blue]")
    console.print("• Pydantic configuration validation working")
    console.print("• Component broker with communication tracing working")
    console.print("• Service factory for extensibility working")
    console.print("• Rich CLI interface working")
    console.print("\nNext steps:")
    console.print("• Implement Reddit comment commands")
    console.print("• Add Cloudflare Pages deployment")
    console.print("• Implement weekly digest feature")


def _show_credential_help() -> None:
    """Show credential help."""
    console.print("\n[bold]🔐 Credential Management:[/bold]")
    console.print("• Set BITBOT_SAVE_CREDS=1 to save current environment variables")
    console.print("• Set BITBOT_LOAD_CREDS=1 to load saved credentials")
    console.print("• Or configure in config.toml:")
    console.print("  [auth]")
    console.print("  auto_save = true")
    console.print("  auto_load = true")
    console.print("• Credentials saved to: credentials.toml")


def run_demo() -> None:
    """Run the original foundation demo (kept for backward compatibility)."""
    console.print(Panel("[bold]BitFields Foundation Demo[/bold]"))

    # Load config with Pydantic validation
    try:
        config = load_config()
        auto_save = getattr(config.auth, "auto_save", False)
        auto_load = getattr(config.auth, "auto_load", False)
        setup_credentials(auto_save=auto_save, auto_load=auto_load)
        log_dry_run_status()
        console.print(
            "[bold green]✅ Configuration loaded and validated successfully[/bold green]"
        )
        console.print(f"   Source repo: {config.github.source_repo}")
        console.print(f"   Bot repo: {config.github.bot_repo}")
        console.print(f"   Subreddit: {config.reddit.subreddit}")
    except Exception as e:
        console.print(f"[bold red]❌ Configuration error:[/bold red] {e}")
        return

    # Create broker
    broker = ComponentBroker(config.model_dump())

    # Demonstrate service creation and communication logging
    console.print("\n[bold]🔧 Creating services...[/bold]")

    # Get GitHub service
    _ = broker.get_service("github")
    broker.log_communication(
        component="Main",
        method="main",
        service="github",
        reason="demonstrate service creation",
        content={"action": "create_service"},
    )
    console.print("[green]✅ GitHub service created[/green]")

    # Get Reddit service
    _ = broker.get_service("reddit")
    broker.log_communication(
        component="Main",
        method="main",
        service="reddit",
        reason="demonstrate service creation",
        content={"action": "create_service"},
    )
    console.print("[green]✅ Reddit service created[/green]")

    # Get deployment services
    _ = broker.get_service("deploy_github")
    broker.log_communication(
        component="Main",
        method="main",
        service="deploy_github",
        reason="demonstrate service creation",
        content={"action": "create_service"},
    )
    console.print("[green]✅ GitHub Pages deployment service created[/green]")

    # Show communication log
    _show_communication_log(broker)
    _show_next_steps()
    _show_credential_help()


def main() -> None:
    """Main entry point for BitBot."""
    # Check if this is a demo request
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        # Run the original demo
        run_demo()
    elif len(sys.argv) > 1 and sys.argv[1] == "--actual":
        # Run the actual workflow
        run_actual_workflow()
    else:
        # Run the complete workflow (currently a test version)
        run_complete_workflow()


if __name__ == "__main__":
    main()
