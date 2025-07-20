"""A service for managing the bot's state."""

import json
from pathlib import Path

from ..data.models import BotState
from ..interfaces.state_protocol import StateManagerProtocol
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


class FileStateManager(StateManagerProtocol):
    """Manages the bot's state."""

    def xǁFileStateManagerǁ__init____mutmut_orig(self, state_path: Path) -> None:
        """Initializes the FileStateManager."""
        self.state_path = state_path

    def xǁFileStateManagerǁ__init____mutmut_1(self, state_path: Path) -> None:
        """Initializes the FileStateManager."""
        self.state_path = None

    xǁFileStateManagerǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFileStateManagerǁ__init____mutmut_1": xǁFileStateManagerǁ__init____mutmut_1
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFileStateManagerǁ__init____mutmut_orig"),
            object.__getattribute__(
                self, "xǁFileStateManagerǁ__init____mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁFileStateManagerǁ__init____mutmut_orig)
    xǁFileStateManagerǁ__init____mutmut_orig.__name__ = "xǁFileStateManagerǁ__init__"

    async def xǁFileStateManagerǁload_state__mutmut_orig(self) -> BotState:
        """Loads the bot's state from a file."""
        if not self.state_path.exists():
            return BotState()
        with self.state_path.open("r") as f:
            state_data = json.load(f)
        return BotState(**state_data)

    async def xǁFileStateManagerǁload_state__mutmut_1(self) -> BotState:
        """Loads the bot's state from a file."""
        if self.state_path.exists():
            return BotState()
        with self.state_path.open("r") as f:
            state_data = json.load(f)
        return BotState(**state_data)

    async def xǁFileStateManagerǁload_state__mutmut_2(self) -> BotState:
        """Loads the bot's state from a file."""
        if not self.state_path.exists():
            return BotState()
        with self.state_path.open(None) as f:
            state_data = json.load(f)
        return BotState(**state_data)

    async def xǁFileStateManagerǁload_state__mutmut_3(self) -> BotState:
        """Loads the bot's state from a file."""
        if not self.state_path.exists():
            return BotState()
        with self.state_path.open("XXrXX") as f:
            state_data = json.load(f)
        return BotState(**state_data)

    async def xǁFileStateManagerǁload_state__mutmut_4(self) -> BotState:
        """Loads the bot's state from a file."""
        if not self.state_path.exists():
            return BotState()
        with self.state_path.open("R") as f:
            state_data = json.load(f)
        return BotState(**state_data)

    async def xǁFileStateManagerǁload_state__mutmut_5(self) -> BotState:
        """Loads the bot's state from a file."""
        if not self.state_path.exists():
            return BotState()
        with self.state_path.open("R") as f:
            state_data = json.load(f)
        return BotState(**state_data)

    async def xǁFileStateManagerǁload_state__mutmut_6(self) -> BotState:
        """Loads the bot's state from a file."""
        if not self.state_path.exists():
            return BotState()
        with self.state_path.open("r") as f:
            state_data = None
        return BotState(**state_data)

    async def xǁFileStateManagerǁload_state__mutmut_7(self) -> BotState:
        """Loads the bot's state from a file."""
        if not self.state_path.exists():
            return BotState()
        with self.state_path.open("r") as f:
            state_data = json.load(None)
        return BotState(**state_data)

    xǁFileStateManagerǁload_state__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFileStateManagerǁload_state__mutmut_1": xǁFileStateManagerǁload_state__mutmut_1,
        "xǁFileStateManagerǁload_state__mutmut_2": xǁFileStateManagerǁload_state__mutmut_2,
        "xǁFileStateManagerǁload_state__mutmut_3": xǁFileStateManagerǁload_state__mutmut_3,
        "xǁFileStateManagerǁload_state__mutmut_4": xǁFileStateManagerǁload_state__mutmut_4,
        "xǁFileStateManagerǁload_state__mutmut_5": xǁFileStateManagerǁload_state__mutmut_5,
        "xǁFileStateManagerǁload_state__mutmut_6": xǁFileStateManagerǁload_state__mutmut_6,
        "xǁFileStateManagerǁload_state__mutmut_7": xǁFileStateManagerǁload_state__mutmut_7,
    }

    def load_state(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFileStateManagerǁload_state__mutmut_orig"),
            object.__getattribute__(
                self, "xǁFileStateManagerǁload_state__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    load_state.__signature__ = _mutmut_signature(
        xǁFileStateManagerǁload_state__mutmut_orig
    )
    xǁFileStateManagerǁload_state__mutmut_orig.__name__ = (
        "xǁFileStateManagerǁload_state"
    )

    async def xǁFileStateManagerǁsave_state__mutmut_orig(self, state: BotState) -> None:
        """Saves the bot's state to a file."""
        with self.state_path.open("w") as f:
            json.dump(state.dict(), f, indent=2)

    async def xǁFileStateManagerǁsave_state__mutmut_1(self, state: BotState) -> None:
        """Saves the bot's state to a file."""
        with self.state_path.open(None) as f:
            json.dump(state.dict(), f, indent=2)

    async def xǁFileStateManagerǁsave_state__mutmut_2(self, state: BotState) -> None:
        """Saves the bot's state to a file."""
        with self.state_path.open("XXwXX") as f:
            json.dump(state.dict(), f, indent=2)

    async def xǁFileStateManagerǁsave_state__mutmut_3(self, state: BotState) -> None:
        """Saves the bot's state to a file."""
        with self.state_path.open("W") as f:
            json.dump(state.dict(), f, indent=2)

    async def xǁFileStateManagerǁsave_state__mutmut_4(self, state: BotState) -> None:
        """Saves the bot's state to a file."""
        with self.state_path.open("W") as f:
            json.dump(state.dict(), f, indent=2)

    async def xǁFileStateManagerǁsave_state__mutmut_5(self, state: BotState) -> None:
        """Saves the bot's state to a file."""
        with self.state_path.open("w") as f:
            json.dump(None, f, indent=2)

    async def xǁFileStateManagerǁsave_state__mutmut_6(self, state: BotState) -> None:
        """Saves the bot's state to a file."""
        with self.state_path.open("w") as f:
            json.dump(state.dict(), None, indent=2)

    async def xǁFileStateManagerǁsave_state__mutmut_7(self, state: BotState) -> None:
        """Saves the bot's state to a file."""
        with self.state_path.open("w") as f:
            json.dump(state.dict(), f, indent=None)

    async def xǁFileStateManagerǁsave_state__mutmut_8(self, state: BotState) -> None:
        """Saves the bot's state to a file."""
        with self.state_path.open("w") as f:
            json.dump(f, indent=2)

    async def xǁFileStateManagerǁsave_state__mutmut_9(self, state: BotState) -> None:
        """Saves the bot's state to a file."""
        with self.state_path.open("w") as f:
            json.dump(state.dict(), indent=2)

    async def xǁFileStateManagerǁsave_state__mutmut_10(self, state: BotState) -> None:
        """Saves the bot's state to a file."""
        with self.state_path.open("w") as f:
            json.dump(
                state.dict(),
                f,
            )

    async def xǁFileStateManagerǁsave_state__mutmut_11(self, state: BotState) -> None:
        """Saves the bot's state to a file."""
        with self.state_path.open("w") as f:
            json.dump(state.dict(), f, indent=3)

    xǁFileStateManagerǁsave_state__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFileStateManagerǁsave_state__mutmut_1": xǁFileStateManagerǁsave_state__mutmut_1,
        "xǁFileStateManagerǁsave_state__mutmut_2": xǁFileStateManagerǁsave_state__mutmut_2,
        "xǁFileStateManagerǁsave_state__mutmut_3": xǁFileStateManagerǁsave_state__mutmut_3,
        "xǁFileStateManagerǁsave_state__mutmut_4": xǁFileStateManagerǁsave_state__mutmut_4,
        "xǁFileStateManagerǁsave_state__mutmut_5": xǁFileStateManagerǁsave_state__mutmut_5,
        "xǁFileStateManagerǁsave_state__mutmut_6": xǁFileStateManagerǁsave_state__mutmut_6,
        "xǁFileStateManagerǁsave_state__mutmut_7": xǁFileStateManagerǁsave_state__mutmut_7,
        "xǁFileStateManagerǁsave_state__mutmut_8": xǁFileStateManagerǁsave_state__mutmut_8,
        "xǁFileStateManagerǁsave_state__mutmut_9": xǁFileStateManagerǁsave_state__mutmut_9,
        "xǁFileStateManagerǁsave_state__mutmut_10": xǁFileStateManagerǁsave_state__mutmut_10,
        "xǁFileStateManagerǁsave_state__mutmut_11": xǁFileStateManagerǁsave_state__mutmut_11,
    }

    def save_state(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFileStateManagerǁsave_state__mutmut_orig"),
            object.__getattribute__(
                self, "xǁFileStateManagerǁsave_state__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    save_state.__signature__ = _mutmut_signature(
        xǁFileStateManagerǁsave_state__mutmut_orig
    )
    xǁFileStateManagerǁsave_state__mutmut_orig.__name__ = (
        "xǁFileStateManagerǁsave_state"
    )
