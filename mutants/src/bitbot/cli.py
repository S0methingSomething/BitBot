"""The command-line interface for the bot."""

import argparse
import asyncio
import os

from .comments import check_comments
from .history import sync_history
from .services.factory import create_services
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result  # for the yield case
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result  # for the yield case
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_yield_from_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = yield from orig(*call_args, **call_kwargs)
        return result  # for the yield case
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = yield from orig(*call_args, **call_kwargs)
        return result  # for the yield case
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = yield from mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = yield from mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x_main__mutmut_orig() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_1() -> None:
    """The main entry point for the bot."""
    parser = None
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_2() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description=None)
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_3() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="XXA bot for managing Reddit posts.XX")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_4() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="a bot for managing reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_5() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A BOT FOR MANAGING REDDIT POSTS.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_6() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_7() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = None

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_8() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest=None)

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_9() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="XXcommandXX")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_10() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="COMMAND")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_11() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="Command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_12() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser(None, help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_13() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help=None)
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_14() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser(help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_15() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser(
        "sync",
    )
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_16() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("XXsyncXX", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_17() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("SYNC", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_18() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("Sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_19() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="XXSync the Reddit post history.XX")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_20() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="sync the reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_21() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="SYNC THE REDDIT POST HISTORY.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_22() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_23() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser(None, help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_24() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help=None)

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_25() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser(help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_26() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser(
        "pulse",
    )

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_27() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("XXpulseXX", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_28() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("PULSE", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_29() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("Pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_30() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="XXCheck for new comments.XX")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_31() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_32() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="CHECK FOR NEW COMMENTS.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_33() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = None

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_34() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = None

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_35() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(None)

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_36() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(None))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_37() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command != "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_38() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "XXsyncXX":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_39() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "SYNC":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_40() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "Sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_41() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(None)
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_42() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=None,
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_43() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=None,
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_44() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=None,
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_45() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=None,
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_46() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=None,
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_47() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_48() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_49() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_50() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_51() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_52() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["XXconfig_managerXX"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_53() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["CONFIG_MANAGER"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_54() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["Config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_55() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["XXstate_managerXX"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_56() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["STATE_MANAGER"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_57() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["State_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_58() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["XXgithub_managerXX"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_59() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["GITHUB_MANAGER"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_60() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["Github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_61() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["XXreddit_managerXX"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_62() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["REDDIT_MANAGER"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_63() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["Reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_64() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["XXtemplate_managerXX"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_65() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["TEMPLATE_MANAGER"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_66() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["Template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_67() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command != "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_68() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "XXpulseXX":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_69() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "PULSE":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_70() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "Pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_71() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(None)
    else:
        parser.print_help()


def x_main__mutmut_72() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=None,
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_73() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=None,
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_74() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=None,
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_75() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_76() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_77() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_78() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["XXconfig_managerXX"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_79() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["CONFIG_MANAGER"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_80() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["Config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_81() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["XXstate_managerXX"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_82() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["STATE_MANAGER"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_83() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["State_manager"],
                reddit_manager=services["reddit_manager"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_84() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["XXreddit_managerXX"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_85() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["REDDIT_MANAGER"],
            )
        )
    else:
        parser.print_help()


def x_main__mutmut_86() -> None:
    """The main entry point for the bot."""
    parser = argparse.ArgumentParser(description="A bot for managing Reddit posts.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Sync the Reddit post history.")
    subparsers.add_parser("pulse", help="Check for new comments.")

    args = parser.parse_args()

    services = create_services(dict(os.environ))

    if args.command == "sync":
        asyncio.run(
            sync_history(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                github_manager=services["github_manager"],
                reddit_manager=services["reddit_manager"],
                template_manager=services["template_manager"],
            )
        )
    elif args.command == "pulse":
        asyncio.run(
            check_comments(
                config_manager=services["config_manager"],
                state_manager=services["state_manager"],
                reddit_manager=services["Reddit_manager"],
            )
        )
    else:
        parser.print_help()


x_main__mutmut_mutants: ClassVar[MutantDict] = {
    "x_main__mutmut_1": x_main__mutmut_1,
    "x_main__mutmut_2": x_main__mutmut_2,
    "x_main__mutmut_3": x_main__mutmut_3,
    "x_main__mutmut_4": x_main__mutmut_4,
    "x_main__mutmut_5": x_main__mutmut_5,
    "x_main__mutmut_6": x_main__mutmut_6,
    "x_main__mutmut_7": x_main__mutmut_7,
    "x_main__mutmut_8": x_main__mutmut_8,
    "x_main__mutmut_9": x_main__mutmut_9,
    "x_main__mutmut_10": x_main__mutmut_10,
    "x_main__mutmut_11": x_main__mutmut_11,
    "x_main__mutmut_12": x_main__mutmut_12,
    "x_main__mutmut_13": x_main__mutmut_13,
    "x_main__mutmut_14": x_main__mutmut_14,
    "x_main__mutmut_15": x_main__mutmut_15,
    "x_main__mutmut_16": x_main__mutmut_16,
    "x_main__mutmut_17": x_main__mutmut_17,
    "x_main__mutmut_18": x_main__mutmut_18,
    "x_main__mutmut_19": x_main__mutmut_19,
    "x_main__mutmut_20": x_main__mutmut_20,
    "x_main__mutmut_21": x_main__mutmut_21,
    "x_main__mutmut_22": x_main__mutmut_22,
    "x_main__mutmut_23": x_main__mutmut_23,
    "x_main__mutmut_24": x_main__mutmut_24,
    "x_main__mutmut_25": x_main__mutmut_25,
    "x_main__mutmut_26": x_main__mutmut_26,
    "x_main__mutmut_27": x_main__mutmut_27,
    "x_main__mutmut_28": x_main__mutmut_28,
    "x_main__mutmut_29": x_main__mutmut_29,
    "x_main__mutmut_30": x_main__mutmut_30,
    "x_main__mutmut_31": x_main__mutmut_31,
    "x_main__mutmut_32": x_main__mutmut_32,
    "x_main__mutmut_33": x_main__mutmut_33,
    "x_main__mutmut_34": x_main__mutmut_34,
    "x_main__mutmut_35": x_main__mutmut_35,
    "x_main__mutmut_36": x_main__mutmut_36,
    "x_main__mutmut_37": x_main__mutmut_37,
    "x_main__mutmut_38": x_main__mutmut_38,
    "x_main__mutmut_39": x_main__mutmut_39,
    "x_main__mutmut_40": x_main__mutmut_40,
    "x_main__mutmut_41": x_main__mutmut_41,
    "x_main__mutmut_42": x_main__mutmut_42,
    "x_main__mutmut_43": x_main__mutmut_43,
    "x_main__mutmut_44": x_main__mutmut_44,
    "x_main__mutmut_45": x_main__mutmut_45,
    "x_main__mutmut_46": x_main__mutmut_46,
    "x_main__mutmut_47": x_main__mutmut_47,
    "x_main__mutmut_48": x_main__mutmut_48,
    "x_main__mutmut_49": x_main__mutmut_49,
    "x_main__mutmut_50": x_main__mutmut_50,
    "x_main__mutmut_51": x_main__mutmut_51,
    "x_main__mutmut_52": x_main__mutmut_52,
    "x_main__mutmut_53": x_main__mutmut_53,
    "x_main__mutmut_54": x_main__mutmut_54,
    "x_main__mutmut_55": x_main__mutmut_55,
    "x_main__mutmut_56": x_main__mutmut_56,
    "x_main__mutmut_57": x_main__mutmut_57,
    "x_main__mutmut_58": x_main__mutmut_58,
    "x_main__mutmut_59": x_main__mutmut_59,
    "x_main__mutmut_60": x_main__mutmut_60,
    "x_main__mutmut_61": x_main__mutmut_61,
    "x_main__mutmut_62": x_main__mutmut_62,
    "x_main__mutmut_63": x_main__mutmut_63,
    "x_main__mutmut_64": x_main__mutmut_64,
    "x_main__mutmut_65": x_main__mutmut_65,
    "x_main__mutmut_66": x_main__mutmut_66,
    "x_main__mutmut_67": x_main__mutmut_67,
    "x_main__mutmut_68": x_main__mutmut_68,
    "x_main__mutmut_69": x_main__mutmut_69,
    "x_main__mutmut_70": x_main__mutmut_70,
    "x_main__mutmut_71": x_main__mutmut_71,
    "x_main__mutmut_72": x_main__mutmut_72,
    "x_main__mutmut_73": x_main__mutmut_73,
    "x_main__mutmut_74": x_main__mutmut_74,
    "x_main__mutmut_75": x_main__mutmut_75,
    "x_main__mutmut_76": x_main__mutmut_76,
    "x_main__mutmut_77": x_main__mutmut_77,
    "x_main__mutmut_78": x_main__mutmut_78,
    "x_main__mutmut_79": x_main__mutmut_79,
    "x_main__mutmut_80": x_main__mutmut_80,
    "x_main__mutmut_81": x_main__mutmut_81,
    "x_main__mutmut_82": x_main__mutmut_82,
    "x_main__mutmut_83": x_main__mutmut_83,
    "x_main__mutmut_84": x_main__mutmut_84,
    "x_main__mutmut_85": x_main__mutmut_85,
    "x_main__mutmut_86": x_main__mutmut_86,
}


def main(*args, **kwargs):
    result = _mutmut_trampoline(
        x_main__mutmut_orig, x_main__mutmut_mutants, args, kwargs
    )
    return result


main.__signature__ = _mutmut_signature(x_main__mutmut_orig)
x_main__mutmut_orig.__name__ = "x_main"
