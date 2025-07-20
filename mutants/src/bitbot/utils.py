"""This module contains utility functions for the BitBot application."""

import json
from pathlib import Path
from typing import Any, Dict, cast
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


def x_load_config__mutmut_orig() -> Dict[str, Any]:
    """Load the main configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path("config.json")
    with config_path.open("r") as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_config__mutmut_1() -> Dict[str, Any]:
    """Load the main configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = None
    with config_path.open("r") as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_config__mutmut_2() -> Dict[str, Any]:
    """Load the main configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path(None)
    with config_path.open("r") as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_config__mutmut_3() -> Dict[str, Any]:
    """Load the main configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path("XXconfig.jsonXX")
    with config_path.open("r") as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_config__mutmut_4() -> Dict[str, Any]:
    """Load the main configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path("CONFIG.JSON")
    with config_path.open("r") as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_config__mutmut_5() -> Dict[str, Any]:
    """Load the main configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path("Config.json")
    with config_path.open("r") as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_config__mutmut_6() -> Dict[str, Any]:
    """Load the main configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path("config.json")
    with config_path.open(None) as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_config__mutmut_7() -> Dict[str, Any]:
    """Load the main configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path("config.json")
    with config_path.open("XXrXX") as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_config__mutmut_8() -> Dict[str, Any]:
    """Load the main configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path("config.json")
    with config_path.open("R") as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_config__mutmut_9() -> Dict[str, Any]:
    """Load the main configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path("config.json")
    with config_path.open("R") as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_config__mutmut_10() -> Dict[str, Any]:
    """Load the main configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path("config.json")
    with config_path.open("r") as f:
        return cast(None, json.load(f))


def x_load_config__mutmut_11() -> Dict[str, Any]:
    """Load the main configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path("config.json")
    with config_path.open("r") as f:
        return cast(Dict[str, Any], None)


def x_load_config__mutmut_12() -> Dict[str, Any]:
    """Load the main configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path("config.json")
    with config_path.open("r") as f:
        return cast(json.load(f))


def x_load_config__mutmut_13() -> Dict[str, Any]:
    """Load the main configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path("config.json")
    with config_path.open("r") as f:
        return cast(
            Dict[str, Any],
        )


def x_load_config__mutmut_14() -> Dict[str, Any]:
    """Load the main configuration file.

    Returns:
        The configuration dictionary.
    """
    config_path = Path("config.json")
    with config_path.open("r") as f:
        return cast(Dict[str, Any], json.load(None))


x_load_config__mutmut_mutants: ClassVar[MutantDict] = {
    "x_load_config__mutmut_1": x_load_config__mutmut_1,
    "x_load_config__mutmut_2": x_load_config__mutmut_2,
    "x_load_config__mutmut_3": x_load_config__mutmut_3,
    "x_load_config__mutmut_4": x_load_config__mutmut_4,
    "x_load_config__mutmut_5": x_load_config__mutmut_5,
    "x_load_config__mutmut_6": x_load_config__mutmut_6,
    "x_load_config__mutmut_7": x_load_config__mutmut_7,
    "x_load_config__mutmut_8": x_load_config__mutmut_8,
    "x_load_config__mutmut_9": x_load_config__mutmut_9,
    "x_load_config__mutmut_10": x_load_config__mutmut_10,
    "x_load_config__mutmut_11": x_load_config__mutmut_11,
    "x_load_config__mutmut_12": x_load_config__mutmut_12,
    "x_load_config__mutmut_13": x_load_config__mutmut_13,
    "x_load_config__mutmut_14": x_load_config__mutmut_14,
}


def load_config(*args, **kwargs):
    result = _mutmut_trampoline(
        x_load_config__mutmut_orig, x_load_config__mutmut_mutants, args, kwargs
    )
    return result


load_config.__signature__ = _mutmut_signature(x_load_config__mutmut_orig)
x_load_config__mutmut_orig.__name__ = "x_load_config"


def x_load_state__mutmut_orig() -> Dict[str, Any]:
    """Load the bot's current monitoring state.

    Returns:
        The state dictionary.
    """
    state_path = Path("bot_state.json")
    with state_path.open("r") as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_state__mutmut_1() -> Dict[str, Any]:
    """Load the bot's current monitoring state.

    Returns:
        The state dictionary.
    """
    state_path = None
    with state_path.open("r") as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_state__mutmut_2() -> Dict[str, Any]:
    """Load the bot's current monitoring state.

    Returns:
        The state dictionary.
    """
    state_path = Path(None)
    with state_path.open("r") as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_state__mutmut_3() -> Dict[str, Any]:
    """Load the bot's current monitoring state.

    Returns:
        The state dictionary.
    """
    state_path = Path("XXbot_state.jsonXX")
    with state_path.open("r") as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_state__mutmut_4() -> Dict[str, Any]:
    """Load the bot's current monitoring state.

    Returns:
        The state dictionary.
    """
    state_path = Path("BOT_STATE.JSON")
    with state_path.open("r") as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_state__mutmut_5() -> Dict[str, Any]:
    """Load the bot's current monitoring state.

    Returns:
        The state dictionary.
    """
    state_path = Path("Bot_state.json")
    with state_path.open("r") as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_state__mutmut_6() -> Dict[str, Any]:
    """Load the bot's current monitoring state.

    Returns:
        The state dictionary.
    """
    state_path = Path("bot_state.json")
    with state_path.open(None) as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_state__mutmut_7() -> Dict[str, Any]:
    """Load the bot's current monitoring state.

    Returns:
        The state dictionary.
    """
    state_path = Path("bot_state.json")
    with state_path.open("XXrXX") as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_state__mutmut_8() -> Dict[str, Any]:
    """Load the bot's current monitoring state.

    Returns:
        The state dictionary.
    """
    state_path = Path("bot_state.json")
    with state_path.open("R") as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_state__mutmut_9() -> Dict[str, Any]:
    """Load the bot's current monitoring state.

    Returns:
        The state dictionary.
    """
    state_path = Path("bot_state.json")
    with state_path.open("R") as f:
        return cast(Dict[str, Any], json.load(f))


def x_load_state__mutmut_10() -> Dict[str, Any]:
    """Load the bot's current monitoring state.

    Returns:
        The state dictionary.
    """
    state_path = Path("bot_state.json")
    with state_path.open("r") as f:
        return cast(None, json.load(f))


def x_load_state__mutmut_11() -> Dict[str, Any]:
    """Load the bot's current monitoring state.

    Returns:
        The state dictionary.
    """
    state_path = Path("bot_state.json")
    with state_path.open("r") as f:
        return cast(Dict[str, Any], None)


def x_load_state__mutmut_12() -> Dict[str, Any]:
    """Load the bot's current monitoring state.

    Returns:
        The state dictionary.
    """
    state_path = Path("bot_state.json")
    with state_path.open("r") as f:
        return cast(json.load(f))


def x_load_state__mutmut_13() -> Dict[str, Any]:
    """Load the bot's current monitoring state.

    Returns:
        The state dictionary.
    """
    state_path = Path("bot_state.json")
    with state_path.open("r") as f:
        return cast(
            Dict[str, Any],
        )


def x_load_state__mutmut_14() -> Dict[str, Any]:
    """Load the bot's current monitoring state.

    Returns:
        The state dictionary.
    """
    state_path = Path("bot_state.json")
    with state_path.open("r") as f:
        return cast(Dict[str, Any], json.load(None))


x_load_state__mutmut_mutants: ClassVar[MutantDict] = {
    "x_load_state__mutmut_1": x_load_state__mutmut_1,
    "x_load_state__mutmut_2": x_load_state__mutmut_2,
    "x_load_state__mutmut_3": x_load_state__mutmut_3,
    "x_load_state__mutmut_4": x_load_state__mutmut_4,
    "x_load_state__mutmut_5": x_load_state__mutmut_5,
    "x_load_state__mutmut_6": x_load_state__mutmut_6,
    "x_load_state__mutmut_7": x_load_state__mutmut_7,
    "x_load_state__mutmut_8": x_load_state__mutmut_8,
    "x_load_state__mutmut_9": x_load_state__mutmut_9,
    "x_load_state__mutmut_10": x_load_state__mutmut_10,
    "x_load_state__mutmut_11": x_load_state__mutmut_11,
    "x_load_state__mutmut_12": x_load_state__mutmut_12,
    "x_load_state__mutmut_13": x_load_state__mutmut_13,
    "x_load_state__mutmut_14": x_load_state__mutmut_14,
}


def load_state(*args, **kwargs):
    result = _mutmut_trampoline(
        x_load_state__mutmut_orig, x_load_state__mutmut_mutants, args, kwargs
    )
    return result


load_state.__signature__ = _mutmut_signature(x_load_state__mutmut_orig)
x_load_state__mutmut_orig.__name__ = "x_load_state"


def x_save_state__mutmut_orig(data: Dict[str, Any]) -> None:
    """Save the bot's monitoring state.

    Args:
        data: The state dictionary to save.
    """
    state_path = Path("bot_state.json")
    with state_path.open("w") as f:
        json.dump(data, f, indent=2)


def x_save_state__mutmut_1(data: Dict[str, Any]) -> None:
    """Save the bot's monitoring state.

    Args:
        data: The state dictionary to save.
    """
    state_path = None
    with state_path.open("w") as f:
        json.dump(data, f, indent=2)


def x_save_state__mutmut_2(data: Dict[str, Any]) -> None:
    """Save the bot's monitoring state.

    Args:
        data: The state dictionary to save.
    """
    state_path = Path(None)
    with state_path.open("w") as f:
        json.dump(data, f, indent=2)


def x_save_state__mutmut_3(data: Dict[str, Any]) -> None:
    """Save the bot's monitoring state.

    Args:
        data: The state dictionary to save.
    """
    state_path = Path("XXbot_state.jsonXX")
    with state_path.open("w") as f:
        json.dump(data, f, indent=2)


def x_save_state__mutmut_4(data: Dict[str, Any]) -> None:
    """Save the bot's monitoring state.

    Args:
        data: The state dictionary to save.
    """
    state_path = Path("BOT_STATE.JSON")
    with state_path.open("w") as f:
        json.dump(data, f, indent=2)


def x_save_state__mutmut_5(data: Dict[str, Any]) -> None:
    """Save the bot's monitoring state.

    Args:
        data: The state dictionary to save.
    """
    state_path = Path("Bot_state.json")
    with state_path.open("w") as f:
        json.dump(data, f, indent=2)


def x_save_state__mutmut_6(data: Dict[str, Any]) -> None:
    """Save the bot's monitoring state.

    Args:
        data: The state dictionary to save.
    """
    state_path = Path("bot_state.json")
    with state_path.open(None) as f:
        json.dump(data, f, indent=2)


def x_save_state__mutmut_7(data: Dict[str, Any]) -> None:
    """Save the bot's monitoring state.

    Args:
        data: The state dictionary to save.
    """
    state_path = Path("bot_state.json")
    with state_path.open("XXwXX") as f:
        json.dump(data, f, indent=2)


def x_save_state__mutmut_8(data: Dict[str, Any]) -> None:
    """Save the bot's monitoring state.

    Args:
        data: The state dictionary to save.
    """
    state_path = Path("bot_state.json")
    with state_path.open("W") as f:
        json.dump(data, f, indent=2)


def x_save_state__mutmut_9(data: Dict[str, Any]) -> None:
    """Save the bot's monitoring state.

    Args:
        data: The state dictionary to save.
    """
    state_path = Path("bot_state.json")
    with state_path.open("W") as f:
        json.dump(data, f, indent=2)


def x_save_state__mutmut_10(data: Dict[str, Any]) -> None:
    """Save the bot's monitoring state.

    Args:
        data: The state dictionary to save.
    """
    state_path = Path("bot_state.json")
    with state_path.open("w") as f:
        json.dump(None, f, indent=2)


def x_save_state__mutmut_11(data: Dict[str, Any]) -> None:
    """Save the bot's monitoring state.

    Args:
        data: The state dictionary to save.
    """
    state_path = Path("bot_state.json")
    with state_path.open("w") as f:
        json.dump(data, None, indent=2)


def x_save_state__mutmut_12(data: Dict[str, Any]) -> None:
    """Save the bot's monitoring state.

    Args:
        data: The state dictionary to save.
    """
    state_path = Path("bot_state.json")
    with state_path.open("w") as f:
        json.dump(data, f, indent=None)


def x_save_state__mutmut_13(data: Dict[str, Any]) -> None:
    """Save the bot's monitoring state.

    Args:
        data: The state dictionary to save.
    """
    state_path = Path("bot_state.json")
    with state_path.open("w") as f:
        json.dump(f, indent=2)


def x_save_state__mutmut_14(data: Dict[str, Any]) -> None:
    """Save the bot's monitoring state.

    Args:
        data: The state dictionary to save.
    """
    state_path = Path("bot_state.json")
    with state_path.open("w") as f:
        json.dump(data, indent=2)


def x_save_state__mutmut_15(data: Dict[str, Any]) -> None:
    """Save the bot's monitoring state.

    Args:
        data: The state dictionary to save.
    """
    state_path = Path("bot_state.json")
    with state_path.open("w") as f:
        json.dump(
            data,
            f,
        )


def x_save_state__mutmut_16(data: Dict[str, Any]) -> None:
    """Save the bot's monitoring state.

    Args:
        data: The state dictionary to save.
    """
    state_path = Path("bot_state.json")
    with state_path.open("w") as f:
        json.dump(data, f, indent=3)


x_save_state__mutmut_mutants: ClassVar[MutantDict] = {
    "x_save_state__mutmut_1": x_save_state__mutmut_1,
    "x_save_state__mutmut_2": x_save_state__mutmut_2,
    "x_save_state__mutmut_3": x_save_state__mutmut_3,
    "x_save_state__mutmut_4": x_save_state__mutmut_4,
    "x_save_state__mutmut_5": x_save_state__mutmut_5,
    "x_save_state__mutmut_6": x_save_state__mutmut_6,
    "x_save_state__mutmut_7": x_save_state__mutmut_7,
    "x_save_state__mutmut_8": x_save_state__mutmut_8,
    "x_save_state__mutmut_9": x_save_state__mutmut_9,
    "x_save_state__mutmut_10": x_save_state__mutmut_10,
    "x_save_state__mutmut_11": x_save_state__mutmut_11,
    "x_save_state__mutmut_12": x_save_state__mutmut_12,
    "x_save_state__mutmut_13": x_save_state__mutmut_13,
    "x_save_state__mutmut_14": x_save_state__mutmut_14,
    "x_save_state__mutmut_15": x_save_state__mutmut_15,
    "x_save_state__mutmut_16": x_save_state__mutmut_16,
}


def save_state(*args, **kwargs):
    result = _mutmut_trampoline(
        x_save_state__mutmut_orig, x_save_state__mutmut_mutants, args, kwargs
    )
    return result


save_state.__signature__ = _mutmut_signature(x_save_state__mutmut_orig)
x_save_state__mutmut_orig.__name__ = "x_save_state"
