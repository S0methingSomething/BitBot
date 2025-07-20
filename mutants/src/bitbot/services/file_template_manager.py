"""A service for managing the bot's templates."""

from pathlib import Path

from ..interfaces.template_protocol import TemplateManagerProtocol
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


class FileTemplateManager(TemplateManagerProtocol):
    """Manages the bot's templates."""

    def xǁFileTemplateManagerǁ__init____mutmut_orig(self, template_dir: Path) -> None:
        """Initializes the FileTemplateManager."""
        self.template_dir = template_dir

    def xǁFileTemplateManagerǁ__init____mutmut_1(self, template_dir: Path) -> None:
        """Initializes the FileTemplateManager."""
        self.template_dir = None

    xǁFileTemplateManagerǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFileTemplateManagerǁ__init____mutmut_1": xǁFileTemplateManagerǁ__init____mutmut_1
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁFileTemplateManagerǁ__init____mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁFileTemplateManagerǁ__init____mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(
        xǁFileTemplateManagerǁ__init____mutmut_orig
    )
    xǁFileTemplateManagerǁ__init____mutmut_orig.__name__ = (
        "xǁFileTemplateManagerǁ__init__"
    )

    async def xǁFileTemplateManagerǁget_template__mutmut_orig(self, name: str) -> str:
        """Gets a template by name."""
        with (self.template_dir / name).open("r") as f:
            return f.read()

    async def xǁFileTemplateManagerǁget_template__mutmut_1(self, name: str) -> str:
        """Gets a template by name."""
        with (self.template_dir / name).open(None) as f:
            return f.read()

    async def xǁFileTemplateManagerǁget_template__mutmut_2(self, name: str) -> str:
        """Gets a template by name."""
        with (self.template_dir * name).open("r") as f:
            return f.read()

    async def xǁFileTemplateManagerǁget_template__mutmut_3(self, name: str) -> str:
        """Gets a template by name."""
        with (self.template_dir / name).open("XXrXX") as f:
            return f.read()

    async def xǁFileTemplateManagerǁget_template__mutmut_4(self, name: str) -> str:
        """Gets a template by name."""
        with (self.template_dir / name).open("R") as f:
            return f.read()

    async def xǁFileTemplateManagerǁget_template__mutmut_5(self, name: str) -> str:
        """Gets a template by name."""
        with (self.template_dir / name).open("R") as f:
            return f.read()

    xǁFileTemplateManagerǁget_template__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁFileTemplateManagerǁget_template__mutmut_1": xǁFileTemplateManagerǁget_template__mutmut_1,
        "xǁFileTemplateManagerǁget_template__mutmut_2": xǁFileTemplateManagerǁget_template__mutmut_2,
        "xǁFileTemplateManagerǁget_template__mutmut_3": xǁFileTemplateManagerǁget_template__mutmut_3,
        "xǁFileTemplateManagerǁget_template__mutmut_4": xǁFileTemplateManagerǁget_template__mutmut_4,
        "xǁFileTemplateManagerǁget_template__mutmut_5": xǁFileTemplateManagerǁget_template__mutmut_5,
    }

    def get_template(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁFileTemplateManagerǁget_template__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁFileTemplateManagerǁget_template__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    get_template.__signature__ = _mutmut_signature(
        xǁFileTemplateManagerǁget_template__mutmut_orig
    )
    xǁFileTemplateManagerǁget_template__mutmut_orig.__name__ = (
        "xǁFileTemplateManagerǁget_template"
    )
