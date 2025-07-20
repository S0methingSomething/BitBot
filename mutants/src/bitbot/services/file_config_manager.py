"""A service for managing the bot's configuration."""

from pathlib import Path

import toml

from ..data.models import Config
from ..interfaces.config_protocol import ConfigManagerProtocol
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


class FileConfigManager(ConfigManagerProtocol):
    """Manages the bot's configuration."""

    def xǁFileConfigManagerǁ__init____mutmut_orig(self, config_path: Path) -> None:
        """Initializes the FileConfigManager."""
        self.config_path = config_path

    def xǁFileConfigManagerǁ__init____mutmut_1(self, config_path: Path) -> None:
        """Initializes the FileConfigManager."""
        self.config_path = None

    xǁFileConfigManagerǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFileConfigManagerǁ__init____mutmut_1": xǁFileConfigManagerǁ__init____mutmut_1
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁFileConfigManagerǁ__init____mutmut_orig"),
            object.__getattribute__(
                self, "xǁFileConfigManagerǁ__init____mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(
        xǁFileConfigManagerǁ__init____mutmut_orig
    )
    xǁFileConfigManagerǁ__init____mutmut_orig.__name__ = "xǁFileConfigManagerǁ__init__"

    async def xǁFileConfigManagerǁload_config__mutmut_orig(self) -> Config:
        """Loads the configuration from a file."""
        with self.config_path.open("r") as f:
            config_data = toml.load(f)
        return Config(**config_data)

    async def xǁFileConfigManagerǁload_config__mutmut_1(self) -> Config:
        """Loads the configuration from a file."""
        with self.config_path.open(None) as f:
            config_data = toml.load(f)
        return Config(**config_data)

    async def xǁFileConfigManagerǁload_config__mutmut_2(self) -> Config:
        """Loads the configuration from a file."""
        with self.config_path.open("XXrXX") as f:
            config_data = toml.load(f)
        return Config(**config_data)

    async def xǁFileConfigManagerǁload_config__mutmut_3(self) -> Config:
        """Loads the configuration from a file."""
        with self.config_path.open("R") as f:
            config_data = toml.load(f)
        return Config(**config_data)

    async def xǁFileConfigManagerǁload_config__mutmut_4(self) -> Config:
        """Loads the configuration from a file."""
        with self.config_path.open("R") as f:
            config_data = toml.load(f)
        return Config(**config_data)

    async def xǁFileConfigManagerǁload_config__mutmut_5(self) -> Config:
        """Loads the configuration from a file."""
        with self.config_path.open("r") as f:
            config_data = None
        return Config(**config_data)

    async def xǁFileConfigManagerǁload_config__mutmut_6(self) -> Config:
        """Loads the configuration from a file."""
        with self.config_path.open("r") as f:
            config_data = toml.load(None)
        return Config(**config_data)

    xǁFileConfigManagerǁload_config__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFileConfigManagerǁload_config__mutmut_1": xǁFileConfigManagerǁload_config__mutmut_1,
        "xǁFileConfigManagerǁload_config__mutmut_2": xǁFileConfigManagerǁload_config__mutmut_2,
        "xǁFileConfigManagerǁload_config__mutmut_3": xǁFileConfigManagerǁload_config__mutmut_3,
        "xǁFileConfigManagerǁload_config__mutmut_4": xǁFileConfigManagerǁload_config__mutmut_4,
        "xǁFileConfigManagerǁload_config__mutmut_5": xǁFileConfigManagerǁload_config__mutmut_5,
        "xǁFileConfigManagerǁload_config__mutmut_6": xǁFileConfigManagerǁload_config__mutmut_6,
    }

    def load_config(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁFileConfigManagerǁload_config__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁFileConfigManagerǁload_config__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    load_config.__signature__ = _mutmut_signature(
        xǁFileConfigManagerǁload_config__mutmut_orig
    )
    xǁFileConfigManagerǁload_config__mutmut_orig.__name__ = (
        "xǁFileConfigManagerǁload_config"
    )
