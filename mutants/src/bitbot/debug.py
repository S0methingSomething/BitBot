"""This module provides debugging utilities for the BitBot application."""

import logging

from .logging import get_logger
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


def x_enable_debug_mode__mutmut_orig() -> None:
    """Enable debug logging for the application."""
    get_logger("bitbot").setLevel(logging.DEBUG)
    logger = get_logger(__name__)
    logger.debug("Debug mode enabled.")


def x_enable_debug_mode__mutmut_1() -> None:
    """Enable debug logging for the application."""
    get_logger("bitbot").setLevel(None)
    logger = get_logger(__name__)
    logger.debug("Debug mode enabled.")


def x_enable_debug_mode__mutmut_2() -> None:
    """Enable debug logging for the application."""
    get_logger(None).setLevel(logging.DEBUG)
    logger = get_logger(__name__)
    logger.debug("Debug mode enabled.")


def x_enable_debug_mode__mutmut_3() -> None:
    """Enable debug logging for the application."""
    get_logger("XXbitbotXX").setLevel(logging.DEBUG)
    logger = get_logger(__name__)
    logger.debug("Debug mode enabled.")


def x_enable_debug_mode__mutmut_4() -> None:
    """Enable debug logging for the application."""
    get_logger("BITBOT").setLevel(logging.DEBUG)
    logger = get_logger(__name__)
    logger.debug("Debug mode enabled.")


def x_enable_debug_mode__mutmut_5() -> None:
    """Enable debug logging for the application."""
    get_logger("Bitbot").setLevel(logging.DEBUG)
    logger = get_logger(__name__)
    logger.debug("Debug mode enabled.")


def x_enable_debug_mode__mutmut_6() -> None:
    """Enable debug logging for the application."""
    get_logger("bitbot").setLevel(logging.DEBUG)
    logger = None
    logger.debug("Debug mode enabled.")


def x_enable_debug_mode__mutmut_7() -> None:
    """Enable debug logging for the application."""
    get_logger("bitbot").setLevel(logging.DEBUG)
    logger = get_logger(None)
    logger.debug("Debug mode enabled.")


def x_enable_debug_mode__mutmut_8() -> None:
    """Enable debug logging for the application."""
    get_logger("bitbot").setLevel(logging.DEBUG)
    logger = get_logger(__name__)
    logger.debug(None)


def x_enable_debug_mode__mutmut_9() -> None:
    """Enable debug logging for the application."""
    get_logger("bitbot").setLevel(logging.DEBUG)
    logger = get_logger(__name__)
    logger.debug("XXDebug mode enabled.XX")


def x_enable_debug_mode__mutmut_10() -> None:
    """Enable debug logging for the application."""
    get_logger("bitbot").setLevel(logging.DEBUG)
    logger = get_logger(__name__)
    logger.debug("debug mode enabled.")


def x_enable_debug_mode__mutmut_11() -> None:
    """Enable debug logging for the application."""
    get_logger("bitbot").setLevel(logging.DEBUG)
    logger = get_logger(__name__)
    logger.debug("DEBUG MODE ENABLED.")


x_enable_debug_mode__mutmut_mutants: ClassVar[MutantDict] = {
    "x_enable_debug_mode__mutmut_1": x_enable_debug_mode__mutmut_1,
    "x_enable_debug_mode__mutmut_2": x_enable_debug_mode__mutmut_2,
    "x_enable_debug_mode__mutmut_3": x_enable_debug_mode__mutmut_3,
    "x_enable_debug_mode__mutmut_4": x_enable_debug_mode__mutmut_4,
    "x_enable_debug_mode__mutmut_5": x_enable_debug_mode__mutmut_5,
    "x_enable_debug_mode__mutmut_6": x_enable_debug_mode__mutmut_6,
    "x_enable_debug_mode__mutmut_7": x_enable_debug_mode__mutmut_7,
    "x_enable_debug_mode__mutmut_8": x_enable_debug_mode__mutmut_8,
    "x_enable_debug_mode__mutmut_9": x_enable_debug_mode__mutmut_9,
    "x_enable_debug_mode__mutmut_10": x_enable_debug_mode__mutmut_10,
    "x_enable_debug_mode__mutmut_11": x_enable_debug_mode__mutmut_11,
}


def enable_debug_mode(*args, **kwargs):
    result = _mutmut_trampoline(
        x_enable_debug_mode__mutmut_orig,
        x_enable_debug_mode__mutmut_mutants,
        args,
        kwargs,
    )
    return result


enable_debug_mode.__signature__ = _mutmut_signature(x_enable_debug_mode__mutmut_orig)
x_enable_debug_mode__mutmut_orig.__name__ = "x_enable_debug_mode"
