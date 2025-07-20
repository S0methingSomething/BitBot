"""A service for managing GitHub interactions."""

from typing import Optional

import aiohttp

from ..data.models import GitHubRelease
from ..interfaces.github_protocol import GitHubManagerProtocol
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


class GitHubManager(GitHubManagerProtocol):
    """Manages GitHub interactions."""

    def xǁGitHubManagerǁ__init____mutmut_orig(self, token: str) -> None:
        """Initializes the GitHubManager."""
        self.token = token
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github+json",
            }
        )

    def xǁGitHubManagerǁ__init____mutmut_1(self, token: str) -> None:
        """Initializes the GitHubManager."""
        self.token = None
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github+json",
            }
        )

    def xǁGitHubManagerǁ__init____mutmut_2(self, token: str) -> None:
        """Initializes the GitHubManager."""
        self.token = token
        self.session = None

    def xǁGitHubManagerǁ__init____mutmut_3(self, token: str) -> None:
        """Initializes the GitHubManager."""
        self.token = token
        self.session = aiohttp.ClientSession(headers=None)

    def xǁGitHubManagerǁ__init____mutmut_4(self, token: str) -> None:
        """Initializes the GitHubManager."""
        self.token = token
        self.session = aiohttp.ClientSession(
            headers={
                "XXAuthorizationXX": f"Bearer {self.token}",
                "Accept": "application/vnd.github+json",
            }
        )

    def xǁGitHubManagerǁ__init____mutmut_5(self, token: str) -> None:
        """Initializes the GitHubManager."""
        self.token = token
        self.session = aiohttp.ClientSession(
            headers={
                "authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github+json",
            }
        )

    def xǁGitHubManagerǁ__init____mutmut_6(self, token: str) -> None:
        """Initializes the GitHubManager."""
        self.token = token
        self.session = aiohttp.ClientSession(
            headers={
                "AUTHORIZATION": f"Bearer {self.token}",
                "Accept": "application/vnd.github+json",
            }
        )

    def xǁGitHubManagerǁ__init____mutmut_7(self, token: str) -> None:
        """Initializes the GitHubManager."""
        self.token = token
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.token}",
                "XXAcceptXX": "application/vnd.github+json",
            }
        )

    def xǁGitHubManagerǁ__init____mutmut_8(self, token: str) -> None:
        """Initializes the GitHubManager."""
        self.token = token
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/vnd.github+json",
            }
        )

    def xǁGitHubManagerǁ__init____mutmut_9(self, token: str) -> None:
        """Initializes the GitHubManager."""
        self.token = token
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.token}",
                "ACCEPT": "application/vnd.github+json",
            }
        )

    def xǁGitHubManagerǁ__init____mutmut_10(self, token: str) -> None:
        """Initializes the GitHubManager."""
        self.token = token
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "XXapplication/vnd.github+jsonXX",
            }
        )

    def xǁGitHubManagerǁ__init____mutmut_11(self, token: str) -> None:
        """Initializes the GitHubManager."""
        self.token = token
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "APPLICATION/VND.GITHUB+JSON",
            }
        )

    def xǁGitHubManagerǁ__init____mutmut_12(self, token: str) -> None:
        """Initializes the GitHubManager."""
        self.token = token
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "Application/vnd.github+json",
            }
        )

    xǁGitHubManagerǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁGitHubManagerǁ__init____mutmut_1": xǁGitHubManagerǁ__init____mutmut_1,
        "xǁGitHubManagerǁ__init____mutmut_2": xǁGitHubManagerǁ__init____mutmut_2,
        "xǁGitHubManagerǁ__init____mutmut_3": xǁGitHubManagerǁ__init____mutmut_3,
        "xǁGitHubManagerǁ__init____mutmut_4": xǁGitHubManagerǁ__init____mutmut_4,
        "xǁGitHubManagerǁ__init____mutmut_5": xǁGitHubManagerǁ__init____mutmut_5,
        "xǁGitHubManagerǁ__init____mutmut_6": xǁGitHubManagerǁ__init____mutmut_6,
        "xǁGitHubManagerǁ__init____mutmut_7": xǁGitHubManagerǁ__init____mutmut_7,
        "xǁGitHubManagerǁ__init____mutmut_8": xǁGitHubManagerǁ__init____mutmut_8,
        "xǁGitHubManagerǁ__init____mutmut_9": xǁGitHubManagerǁ__init____mutmut_9,
        "xǁGitHubManagerǁ__init____mutmut_10": xǁGitHubManagerǁ__init____mutmut_10,
        "xǁGitHubManagerǁ__init____mutmut_11": xǁGitHubManagerǁ__init____mutmut_11,
        "xǁGitHubManagerǁ__init____mutmut_12": xǁGitHubManagerǁ__init____mutmut_12,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁGitHubManagerǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁGitHubManagerǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁGitHubManagerǁ__init____mutmut_orig)
    xǁGitHubManagerǁ__init____mutmut_orig.__name__ = "xǁGitHubManagerǁ__init__"

    async def xǁGitHubManagerǁget_latest_release__mutmut_orig(
        self, repo_slug: str
    ) -> Optional[GitHubRelease]:
        """Gets the latest release from a GitHub repository."""
        api_url = f"https://api.github.com/repos/{repo_slug}/releases/latest"
        async with self.session.get(api_url) as response:
            response.raise_for_status()
            release_data = await response.json()
            return GitHubRelease(**release_data)

    async def xǁGitHubManagerǁget_latest_release__mutmut_1(
        self, repo_slug: str
    ) -> Optional[GitHubRelease]:
        """Gets the latest release from a GitHub repository."""
        api_url = None
        async with self.session.get(api_url) as response:
            response.raise_for_status()
            release_data = await response.json()
            return GitHubRelease(**release_data)

    async def xǁGitHubManagerǁget_latest_release__mutmut_2(
        self, repo_slug: str
    ) -> Optional[GitHubRelease]:
        """Gets the latest release from a GitHub repository."""
        api_url = f"https://api.github.com/repos/{repo_slug}/releases/latest"
        async with self.session.get(None) as response:
            response.raise_for_status()
            release_data = await response.json()
            return GitHubRelease(**release_data)

    async def xǁGitHubManagerǁget_latest_release__mutmut_3(
        self, repo_slug: str
    ) -> Optional[GitHubRelease]:
        """Gets the latest release from a GitHub repository."""
        api_url = f"https://api.github.com/repos/{repo_slug}/releases/latest"
        async with self.session.get(api_url) as response:
            response.raise_for_status()
            release_data = None
            return GitHubRelease(**release_data)

    xǁGitHubManagerǁget_latest_release__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁGitHubManagerǁget_latest_release__mutmut_1": xǁGitHubManagerǁget_latest_release__mutmut_1,
        "xǁGitHubManagerǁget_latest_release__mutmut_2": xǁGitHubManagerǁget_latest_release__mutmut_2,
        "xǁGitHubManagerǁget_latest_release__mutmut_3": xǁGitHubManagerǁget_latest_release__mutmut_3,
    }

    def get_latest_release(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁGitHubManagerǁget_latest_release__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁGitHubManagerǁget_latest_release__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    get_latest_release.__signature__ = _mutmut_signature(
        xǁGitHubManagerǁget_latest_release__mutmut_orig
    )
    xǁGitHubManagerǁget_latest_release__mutmut_orig.__name__ = (
        "xǁGitHubManagerǁget_latest_release"
    )

    async def close(self) -> None:
        """Closes the GitHub session."""
        await self.session.close()
