"""This module provides a configured logger for the application."""

import logging
import sys
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


def x_get_logger__mutmut_orig(name: str, level: int = logging.INFO) -> logging.Logger:
    """Return a configured logger.

    Args:
        name: The name of the logger.
        level: The logging level.

    Returns:
        A configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def x_get_logger__mutmut_1(name: str, level: int = logging.INFO) -> logging.Logger:
    """Return a configured logger.

    Args:
        name: The name of the logger.
        level: The logging level.

    Returns:
        A configured logger.
    """
    logger = None
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def x_get_logger__mutmut_2(name: str, level: int = logging.INFO) -> logging.Logger:
    """Return a configured logger.

    Args:
        name: The name of the logger.
        level: The logging level.

    Returns:
        A configured logger.
    """
    logger = logging.getLogger(None)
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def x_get_logger__mutmut_3(name: str, level: int = logging.INFO) -> logging.Logger:
    """Return a configured logger.

    Args:
        name: The name of the logger.
        level: The logging level.

    Returns:
        A configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(None)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def x_get_logger__mutmut_4(name: str, level: int = logging.INFO) -> logging.Logger:
    """Return a configured logger.

    Args:
        name: The name of the logger.
        level: The logging level.

    Returns:
        A configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = None
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def x_get_logger__mutmut_5(name: str, level: int = logging.INFO) -> logging.Logger:
    """Return a configured logger.

    Args:
        name: The name of the logger.
        level: The logging level.

    Returns:
        A configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler(None)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def x_get_logger__mutmut_6(name: str, level: int = logging.INFO) -> logging.Logger:
    """Return a configured logger.

    Args:
        name: The name of the logger.
        level: The logging level.

    Returns:
        A configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    formatter = None
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def x_get_logger__mutmut_7(name: str, level: int = logging.INFO) -> logging.Logger:
    """Return a configured logger.

    Args:
        name: The name of the logger.
        level: The logging level.

    Returns:
        A configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(None)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def x_get_logger__mutmut_8(name: str, level: int = logging.INFO) -> logging.Logger:
    """Return a configured logger.

    Args:
        name: The name of the logger.
        level: The logging level.

    Returns:
        A configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "XX%(asctime)s - %(name)s - %(levelname)s - %(message)sXX"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def x_get_logger__mutmut_9(name: str, level: int = logging.INFO) -> logging.Logger:
    """Return a configured logger.

    Args:
        name: The name of the logger.
        level: The logging level.

    Returns:
        A configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(ASCTIME)S - %(NAME)S - %(LEVELNAME)S - %(MESSAGE)S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def x_get_logger__mutmut_10(name: str, level: int = logging.INFO) -> logging.Logger:
    """Return a configured logger.

    Args:
        name: The name of the logger.
        level: The logging level.

    Returns:
        A configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(None)
    logger.addHandler(handler)
    return logger


def x_get_logger__mutmut_11(name: str, level: int = logging.INFO) -> logging.Logger:
    """Return a configured logger.

    Args:
        name: The name of the logger.
        level: The logging level.

    Returns:
        A configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(None)
    return logger


x_get_logger__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_logger__mutmut_1": x_get_logger__mutmut_1,
    "x_get_logger__mutmut_2": x_get_logger__mutmut_2,
    "x_get_logger__mutmut_3": x_get_logger__mutmut_3,
    "x_get_logger__mutmut_4": x_get_logger__mutmut_4,
    "x_get_logger__mutmut_5": x_get_logger__mutmut_5,
    "x_get_logger__mutmut_6": x_get_logger__mutmut_6,
    "x_get_logger__mutmut_7": x_get_logger__mutmut_7,
    "x_get_logger__mutmut_8": x_get_logger__mutmut_8,
    "x_get_logger__mutmut_9": x_get_logger__mutmut_9,
    "x_get_logger__mutmut_10": x_get_logger__mutmut_10,
    "x_get_logger__mutmut_11": x_get_logger__mutmut_11,
}


def get_logger(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_logger__mutmut_orig, x_get_logger__mutmut_mutants, args, kwargs
    )
    return result


get_logger.__signature__ = _mutmut_signature(x_get_logger__mutmut_orig)
x_get_logger__mutmut_orig.__name__ = "x_get_logger"
