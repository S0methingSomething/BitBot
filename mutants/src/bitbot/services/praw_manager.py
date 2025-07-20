"""A service for managing Reddit interactions."""

from typing import Any, List, Optional

import asyncpraw

from ..data.models import RedditPost
from ..interfaces.reddit_protocol import RedditManagerProtocol
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


class PrawManager(RedditManagerProtocol):
    """Manages Reddit interactions using PRAW."""

    def xǁPrawManagerǁ__init____mutmut_orig(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        username: str,
        password: str,
    ) -> None:
        """Initializes the PrawManager."""
        self.reddit = asyncpraw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password,
        )

    def xǁPrawManagerǁ__init____mutmut_1(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        username: str,
        password: str,
    ) -> None:
        """Initializes the PrawManager."""
        self.reddit = None

    def xǁPrawManagerǁ__init____mutmut_2(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        username: str,
        password: str,
    ) -> None:
        """Initializes the PrawManager."""
        self.reddit = asyncpraw.Reddit(
            client_id=None,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password,
        )

    def xǁPrawManagerǁ__init____mutmut_3(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        username: str,
        password: str,
    ) -> None:
        """Initializes the PrawManager."""
        self.reddit = asyncpraw.Reddit(
            client_id=client_id,
            client_secret=None,
            user_agent=user_agent,
            username=username,
            password=password,
        )

    def xǁPrawManagerǁ__init____mutmut_4(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        username: str,
        password: str,
    ) -> None:
        """Initializes the PrawManager."""
        self.reddit = asyncpraw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=None,
            username=username,
            password=password,
        )

    def xǁPrawManagerǁ__init____mutmut_5(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        username: str,
        password: str,
    ) -> None:
        """Initializes the PrawManager."""
        self.reddit = asyncpraw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=None,
            password=password,
        )

    def xǁPrawManagerǁ__init____mutmut_6(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        username: str,
        password: str,
    ) -> None:
        """Initializes the PrawManager."""
        self.reddit = asyncpraw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=None,
        )

    def xǁPrawManagerǁ__init____mutmut_7(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        username: str,
        password: str,
    ) -> None:
        """Initializes the PrawManager."""
        self.reddit = asyncpraw.Reddit(
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password,
        )

    def xǁPrawManagerǁ__init____mutmut_8(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        username: str,
        password: str,
    ) -> None:
        """Initializes the PrawManager."""
        self.reddit = asyncpraw.Reddit(
            client_id=client_id,
            user_agent=user_agent,
            username=username,
            password=password,
        )

    def xǁPrawManagerǁ__init____mutmut_9(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        username: str,
        password: str,
    ) -> None:
        """Initializes the PrawManager."""
        self.reddit = asyncpraw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
        )

    def xǁPrawManagerǁ__init____mutmut_10(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        username: str,
        password: str,
    ) -> None:
        """Initializes the PrawManager."""
        self.reddit = asyncpraw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            password=password,
        )

    def xǁPrawManagerǁ__init____mutmut_11(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        username: str,
        password: str,
    ) -> None:
        """Initializes the PrawManager."""
        self.reddit = asyncpraw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
        )

    xǁPrawManagerǁ__init____mutmut_mutants: ClassVar[MutantDict] = {
        "xǁPrawManagerǁ__init____mutmut_1": xǁPrawManagerǁ__init____mutmut_1,
        "xǁPrawManagerǁ__init____mutmut_2": xǁPrawManagerǁ__init____mutmut_2,
        "xǁPrawManagerǁ__init____mutmut_3": xǁPrawManagerǁ__init____mutmut_3,
        "xǁPrawManagerǁ__init____mutmut_4": xǁPrawManagerǁ__init____mutmut_4,
        "xǁPrawManagerǁ__init____mutmut_5": xǁPrawManagerǁ__init____mutmut_5,
        "xǁPrawManagerǁ__init____mutmut_6": xǁPrawManagerǁ__init____mutmut_6,
        "xǁPrawManagerǁ__init____mutmut_7": xǁPrawManagerǁ__init____mutmut_7,
        "xǁPrawManagerǁ__init____mutmut_8": xǁPrawManagerǁ__init____mutmut_8,
        "xǁPrawManagerǁ__init____mutmut_9": xǁPrawManagerǁ__init____mutmut_9,
        "xǁPrawManagerǁ__init____mutmut_10": xǁPrawManagerǁ__init____mutmut_10,
        "xǁPrawManagerǁ__init____mutmut_11": xǁPrawManagerǁ__init____mutmut_11,
    }

    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁPrawManagerǁ__init____mutmut_orig"),
            object.__getattribute__(self, "xǁPrawManagerǁ__init____mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    __init__.__signature__ = _mutmut_signature(xǁPrawManagerǁ__init____mutmut_orig)
    xǁPrawManagerǁ__init____mutmut_orig.__name__ = "xǁPrawManagerǁ__init__"

    async def xǁPrawManagerǁget_post_by_id__mutmut_orig(
        self, post_id: str
    ) -> Optional[RedditPost]:
        """Gets a Reddit post by its ID."""
        submission = await self.reddit.submission(submission_id=post_id)
        return RedditPost(
            id=submission.id,
            title=submission.title,
            body=submission.selftext,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁget_post_by_id__mutmut_1(
        self, post_id: str
    ) -> Optional[RedditPost]:
        """Gets a Reddit post by its ID."""
        submission = None
        return RedditPost(
            id=submission.id,
            title=submission.title,
            body=submission.selftext,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁget_post_by_id__mutmut_2(
        self, post_id: str
    ) -> Optional[RedditPost]:
        """Gets a Reddit post by its ID."""
        submission = await self.reddit.submission(submission_id=None)
        return RedditPost(
            id=submission.id,
            title=submission.title,
            body=submission.selftext,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁget_post_by_id__mutmut_3(
        self, post_id: str
    ) -> Optional[RedditPost]:
        """Gets a Reddit post by its ID."""
        submission = await self.reddit.submission(submission_id=post_id)
        return RedditPost(
            id=None,
            title=submission.title,
            body=submission.selftext,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁget_post_by_id__mutmut_4(
        self, post_id: str
    ) -> Optional[RedditPost]:
        """Gets a Reddit post by its ID."""
        submission = await self.reddit.submission(submission_id=post_id)
        return RedditPost(
            id=submission.id,
            title=None,
            body=submission.selftext,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁget_post_by_id__mutmut_5(
        self, post_id: str
    ) -> Optional[RedditPost]:
        """Gets a Reddit post by its ID."""
        submission = await self.reddit.submission(submission_id=post_id)
        return RedditPost(
            id=submission.id,
            title=submission.title,
            body=None,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁget_post_by_id__mutmut_6(
        self, post_id: str
    ) -> Optional[RedditPost]:
        """Gets a Reddit post by its ID."""
        submission = await self.reddit.submission(submission_id=post_id)
        return RedditPost(
            id=submission.id,
            title=submission.title,
            body=submission.selftext,
            url=None,
        )

    async def xǁPrawManagerǁget_post_by_id__mutmut_7(
        self, post_id: str
    ) -> Optional[RedditPost]:
        """Gets a Reddit post by its ID."""
        submission = await self.reddit.submission(submission_id=post_id)
        return RedditPost(
            title=submission.title,
            body=submission.selftext,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁget_post_by_id__mutmut_8(
        self, post_id: str
    ) -> Optional[RedditPost]:
        """Gets a Reddit post by its ID."""
        submission = await self.reddit.submission(submission_id=post_id)
        return RedditPost(
            id=submission.id,
            body=submission.selftext,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁget_post_by_id__mutmut_9(
        self, post_id: str
    ) -> Optional[RedditPost]:
        """Gets a Reddit post by its ID."""
        submission = await self.reddit.submission(submission_id=post_id)
        return RedditPost(
            id=submission.id,
            title=submission.title,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁget_post_by_id__mutmut_10(
        self, post_id: str
    ) -> Optional[RedditPost]:
        """Gets a Reddit post by its ID."""
        submission = await self.reddit.submission(submission_id=post_id)
        return RedditPost(
            id=submission.id,
            title=submission.title,
            body=submission.selftext,
        )

    xǁPrawManagerǁget_post_by_id__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁPrawManagerǁget_post_by_id__mutmut_1": xǁPrawManagerǁget_post_by_id__mutmut_1,
        "xǁPrawManagerǁget_post_by_id__mutmut_2": xǁPrawManagerǁget_post_by_id__mutmut_2,
        "xǁPrawManagerǁget_post_by_id__mutmut_3": xǁPrawManagerǁget_post_by_id__mutmut_3,
        "xǁPrawManagerǁget_post_by_id__mutmut_4": xǁPrawManagerǁget_post_by_id__mutmut_4,
        "xǁPrawManagerǁget_post_by_id__mutmut_5": xǁPrawManagerǁget_post_by_id__mutmut_5,
        "xǁPrawManagerǁget_post_by_id__mutmut_6": xǁPrawManagerǁget_post_by_id__mutmut_6,
        "xǁPrawManagerǁget_post_by_id__mutmut_7": xǁPrawManagerǁget_post_by_id__mutmut_7,
        "xǁPrawManagerǁget_post_by_id__mutmut_8": xǁPrawManagerǁget_post_by_id__mutmut_8,
        "xǁPrawManagerǁget_post_by_id__mutmut_9": xǁPrawManagerǁget_post_by_id__mutmut_9,
        "xǁPrawManagerǁget_post_by_id__mutmut_10": xǁPrawManagerǁget_post_by_id__mutmut_10,
    }

    def get_post_by_id(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁPrawManagerǁget_post_by_id__mutmut_orig"),
            object.__getattribute__(
                self, "xǁPrawManagerǁget_post_by_id__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    get_post_by_id.__signature__ = _mutmut_signature(
        xǁPrawManagerǁget_post_by_id__mutmut_orig
    )
    xǁPrawManagerǁget_post_by_id__mutmut_orig.__name__ = "xǁPrawManagerǁget_post_by_id"

    async def xǁPrawManagerǁget_comments__mutmut_orig(
        self, post: RedditPost
    ) -> List[Any]:
        """Gets the comments from a Reddit post."""
        submission = await self.reddit.submission(submission_id=post.id)
        await submission.comments.replace_more(limit=0)
        comments = await submission.comments.list()
        return list(comments)

    async def xǁPrawManagerǁget_comments__mutmut_1(self, post: RedditPost) -> List[Any]:
        """Gets the comments from a Reddit post."""
        submission = None
        await submission.comments.replace_more(limit=0)
        comments = await submission.comments.list()
        return list(comments)

    async def xǁPrawManagerǁget_comments__mutmut_2(self, post: RedditPost) -> List[Any]:
        """Gets the comments from a Reddit post."""
        submission = await self.reddit.submission(submission_id=None)
        await submission.comments.replace_more(limit=0)
        comments = await submission.comments.list()
        return list(comments)

    async def xǁPrawManagerǁget_comments__mutmut_3(self, post: RedditPost) -> List[Any]:
        """Gets the comments from a Reddit post."""
        submission = await self.reddit.submission(submission_id=post.id)
        await submission.comments.replace_more(limit=None)
        comments = await submission.comments.list()
        return list(comments)

    async def xǁPrawManagerǁget_comments__mutmut_4(self, post: RedditPost) -> List[Any]:
        """Gets the comments from a Reddit post."""
        submission = await self.reddit.submission(submission_id=post.id)
        await submission.comments.replace_more(limit=1)
        comments = await submission.comments.list()
        return list(comments)

    async def xǁPrawManagerǁget_comments__mutmut_5(self, post: RedditPost) -> List[Any]:
        """Gets the comments from a Reddit post."""
        submission = await self.reddit.submission(submission_id=post.id)
        await submission.comments.replace_more(limit=0)
        comments = None
        return list(comments)

    async def xǁPrawManagerǁget_comments__mutmut_6(self, post: RedditPost) -> List[Any]:
        """Gets the comments from a Reddit post."""
        submission = await self.reddit.submission(submission_id=post.id)
        await submission.comments.replace_more(limit=0)
        comments = await submission.comments.list()
        return list(None)

    xǁPrawManagerǁget_comments__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁPrawManagerǁget_comments__mutmut_1": xǁPrawManagerǁget_comments__mutmut_1,
        "xǁPrawManagerǁget_comments__mutmut_2": xǁPrawManagerǁget_comments__mutmut_2,
        "xǁPrawManagerǁget_comments__mutmut_3": xǁPrawManagerǁget_comments__mutmut_3,
        "xǁPrawManagerǁget_comments__mutmut_4": xǁPrawManagerǁget_comments__mutmut_4,
        "xǁPrawManagerǁget_comments__mutmut_5": xǁPrawManagerǁget_comments__mutmut_5,
        "xǁPrawManagerǁget_comments__mutmut_6": xǁPrawManagerǁget_comments__mutmut_6,
    }

    def get_comments(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁPrawManagerǁget_comments__mutmut_orig"),
            object.__getattribute__(self, "xǁPrawManagerǁget_comments__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    get_comments.__signature__ = _mutmut_signature(
        xǁPrawManagerǁget_comments__mutmut_orig
    )
    xǁPrawManagerǁget_comments__mutmut_orig.__name__ = "xǁPrawManagerǁget_comments"

    async def xǁPrawManagerǁget_recent_bot_posts__mutmut_orig(
        self, limit: int
    ) -> List[RedditPost]:
        """Gets a list of recent posts made by the bot."""
        bot_user = await self.reddit.user.me()
        if not bot_user:
            return []
        submissions = bot_user.submissions.new(limit=limit)
        return [
            RedditPost(id=s.id, title=s.title, body=s.selftext, url=s.shortlink)
            async for s in submissions
        ]

    async def xǁPrawManagerǁget_recent_bot_posts__mutmut_1(
        self, limit: int
    ) -> List[RedditPost]:
        """Gets a list of recent posts made by the bot."""
        bot_user = None
        if not bot_user:
            return []
        submissions = bot_user.submissions.new(limit=limit)
        return [
            RedditPost(id=s.id, title=s.title, body=s.selftext, url=s.shortlink)
            async for s in submissions
        ]

    async def xǁPrawManagerǁget_recent_bot_posts__mutmut_2(
        self, limit: int
    ) -> List[RedditPost]:
        """Gets a list of recent posts made by the bot."""
        bot_user = await self.reddit.user.me()
        if bot_user:
            return []
        submissions = bot_user.submissions.new(limit=limit)
        return [
            RedditPost(id=s.id, title=s.title, body=s.selftext, url=s.shortlink)
            async for s in submissions
        ]

    async def xǁPrawManagerǁget_recent_bot_posts__mutmut_3(
        self, limit: int
    ) -> List[RedditPost]:
        """Gets a list of recent posts made by the bot."""
        bot_user = await self.reddit.user.me()
        if not bot_user:
            return []
        submissions = None
        return [
            RedditPost(id=s.id, title=s.title, body=s.selftext, url=s.shortlink)
            async for s in submissions
        ]

    async def xǁPrawManagerǁget_recent_bot_posts__mutmut_4(
        self, limit: int
    ) -> List[RedditPost]:
        """Gets a list of recent posts made by the bot."""
        bot_user = await self.reddit.user.me()
        if not bot_user:
            return []
        submissions = bot_user.submissions.new(limit=None)
        return [
            RedditPost(id=s.id, title=s.title, body=s.selftext, url=s.shortlink)
            async for s in submissions
        ]

    async def xǁPrawManagerǁget_recent_bot_posts__mutmut_5(
        self, limit: int
    ) -> List[RedditPost]:
        """Gets a list of recent posts made by the bot."""
        bot_user = await self.reddit.user.me()
        if not bot_user:
            return []
        submissions = bot_user.submissions.new(limit=limit)
        return [
            RedditPost(id=None, title=s.title, body=s.selftext, url=s.shortlink)
            async for s in submissions
        ]

    async def xǁPrawManagerǁget_recent_bot_posts__mutmut_6(
        self, limit: int
    ) -> List[RedditPost]:
        """Gets a list of recent posts made by the bot."""
        bot_user = await self.reddit.user.me()
        if not bot_user:
            return []
        submissions = bot_user.submissions.new(limit=limit)
        return [
            RedditPost(id=s.id, title=None, body=s.selftext, url=s.shortlink)
            async for s in submissions
        ]

    async def xǁPrawManagerǁget_recent_bot_posts__mutmut_7(
        self, limit: int
    ) -> List[RedditPost]:
        """Gets a list of recent posts made by the bot."""
        bot_user = await self.reddit.user.me()
        if not bot_user:
            return []
        submissions = bot_user.submissions.new(limit=limit)
        return [
            RedditPost(id=s.id, title=s.title, body=None, url=s.shortlink)
            async for s in submissions
        ]

    async def xǁPrawManagerǁget_recent_bot_posts__mutmut_8(
        self, limit: int
    ) -> List[RedditPost]:
        """Gets a list of recent posts made by the bot."""
        bot_user = await self.reddit.user.me()
        if not bot_user:
            return []
        submissions = bot_user.submissions.new(limit=limit)
        return [
            RedditPost(id=s.id, title=s.title, body=s.selftext, url=None)
            async for s in submissions
        ]

    async def xǁPrawManagerǁget_recent_bot_posts__mutmut_9(
        self, limit: int
    ) -> List[RedditPost]:
        """Gets a list of recent posts made by the bot."""
        bot_user = await self.reddit.user.me()
        if not bot_user:
            return []
        submissions = bot_user.submissions.new(limit=limit)
        return [
            RedditPost(title=s.title, body=s.selftext, url=s.shortlink)
            async for s in submissions
        ]

    async def xǁPrawManagerǁget_recent_bot_posts__mutmut_10(
        self, limit: int
    ) -> List[RedditPost]:
        """Gets a list of recent posts made by the bot."""
        bot_user = await self.reddit.user.me()
        if not bot_user:
            return []
        submissions = bot_user.submissions.new(limit=limit)
        return [
            RedditPost(id=s.id, body=s.selftext, url=s.shortlink)
            async for s in submissions
        ]

    async def xǁPrawManagerǁget_recent_bot_posts__mutmut_11(
        self, limit: int
    ) -> List[RedditPost]:
        """Gets a list of recent posts made by the bot."""
        bot_user = await self.reddit.user.me()
        if not bot_user:
            return []
        submissions = bot_user.submissions.new(limit=limit)
        return [
            RedditPost(id=s.id, title=s.title, url=s.shortlink)
            async for s in submissions
        ]

    async def xǁPrawManagerǁget_recent_bot_posts__mutmut_12(
        self, limit: int
    ) -> List[RedditPost]:
        """Gets a list of recent posts made by the bot."""
        bot_user = await self.reddit.user.me()
        if not bot_user:
            return []
        submissions = bot_user.submissions.new(limit=limit)
        return [
            RedditPost(
                id=s.id,
                title=s.title,
                body=s.selftext,
            )
            async for s in submissions
        ]

    xǁPrawManagerǁget_recent_bot_posts__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁPrawManagerǁget_recent_bot_posts__mutmut_1": xǁPrawManagerǁget_recent_bot_posts__mutmut_1,
        "xǁPrawManagerǁget_recent_bot_posts__mutmut_2": xǁPrawManagerǁget_recent_bot_posts__mutmut_2,
        "xǁPrawManagerǁget_recent_bot_posts__mutmut_3": xǁPrawManagerǁget_recent_bot_posts__mutmut_3,
        "xǁPrawManagerǁget_recent_bot_posts__mutmut_4": xǁPrawManagerǁget_recent_bot_posts__mutmut_4,
        "xǁPrawManagerǁget_recent_bot_posts__mutmut_5": xǁPrawManagerǁget_recent_bot_posts__mutmut_5,
        "xǁPrawManagerǁget_recent_bot_posts__mutmut_6": xǁPrawManagerǁget_recent_bot_posts__mutmut_6,
        "xǁPrawManagerǁget_recent_bot_posts__mutmut_7": xǁPrawManagerǁget_recent_bot_posts__mutmut_7,
        "xǁPrawManagerǁget_recent_bot_posts__mutmut_8": xǁPrawManagerǁget_recent_bot_posts__mutmut_8,
        "xǁPrawManagerǁget_recent_bot_posts__mutmut_9": xǁPrawManagerǁget_recent_bot_posts__mutmut_9,
        "xǁPrawManagerǁget_recent_bot_posts__mutmut_10": xǁPrawManagerǁget_recent_bot_posts__mutmut_10,
        "xǁPrawManagerǁget_recent_bot_posts__mutmut_11": xǁPrawManagerǁget_recent_bot_posts__mutmut_11,
        "xǁPrawManagerǁget_recent_bot_posts__mutmut_12": xǁPrawManagerǁget_recent_bot_posts__mutmut_12,
    }

    def get_recent_bot_posts(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁPrawManagerǁget_recent_bot_posts__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁPrawManagerǁget_recent_bot_posts__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    get_recent_bot_posts.__signature__ = _mutmut_signature(
        xǁPrawManagerǁget_recent_bot_posts__mutmut_orig
    )
    xǁPrawManagerǁget_recent_bot_posts__mutmut_orig.__name__ = (
        "xǁPrawManagerǁget_recent_bot_posts"
    )

    async def xǁPrawManagerǁupdate_post_body__mutmut_orig(
        self, post_id: str, new_body: str
    ) -> None:
        """Updates the body of a Reddit post."""
        submission = await self.reddit.submission(submission_id=post_id)
        await submission.edit(body=new_body)

    async def xǁPrawManagerǁupdate_post_body__mutmut_1(
        self, post_id: str, new_body: str
    ) -> None:
        """Updates the body of a Reddit post."""
        submission = None
        await submission.edit(body=new_body)

    async def xǁPrawManagerǁupdate_post_body__mutmut_2(
        self, post_id: str, new_body: str
    ) -> None:
        """Updates the body of a Reddit post."""
        submission = await self.reddit.submission(submission_id=None)
        await submission.edit(body=new_body)

    async def xǁPrawManagerǁupdate_post_body__mutmut_3(
        self, post_id: str, new_body: str
    ) -> None:
        """Updates the body of a Reddit post."""
        submission = await self.reddit.submission(submission_id=post_id)
        await submission.edit(body=None)

    xǁPrawManagerǁupdate_post_body__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁPrawManagerǁupdate_post_body__mutmut_1": xǁPrawManagerǁupdate_post_body__mutmut_1,
        "xǁPrawManagerǁupdate_post_body__mutmut_2": xǁPrawManagerǁupdate_post_body__mutmut_2,
        "xǁPrawManagerǁupdate_post_body__mutmut_3": xǁPrawManagerǁupdate_post_body__mutmut_3,
    }

    def update_post_body(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(
                self, "xǁPrawManagerǁupdate_post_body__mutmut_orig"
            ),
            object.__getattribute__(
                self, "xǁPrawManagerǁupdate_post_body__mutmut_mutants"
            ),
            args,
            kwargs,
            self,
        )
        return result

    update_post_body.__signature__ = _mutmut_signature(
        xǁPrawManagerǁupdate_post_body__mutmut_orig
    )
    xǁPrawManagerǁupdate_post_body__mutmut_orig.__name__ = (
        "xǁPrawManagerǁupdate_post_body"
    )

    async def xǁPrawManagerǁsubmit_post__mutmut_orig(
        self, title: str, body: str
    ) -> RedditPost:
        """Submits a new post to Reddit."""
        subreddit = await self.reddit.subreddit("test")
        submission = await subreddit.submit(title, selftext=body)
        return RedditPost(
            id=submission.id,
            title=submission.title,
            body=submission.selftext,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁsubmit_post__mutmut_1(
        self, title: str, body: str
    ) -> RedditPost:
        """Submits a new post to Reddit."""
        subreddit = None
        submission = await subreddit.submit(title, selftext=body)
        return RedditPost(
            id=submission.id,
            title=submission.title,
            body=submission.selftext,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁsubmit_post__mutmut_2(
        self, title: str, body: str
    ) -> RedditPost:
        """Submits a new post to Reddit."""
        subreddit = await self.reddit.subreddit(None)
        submission = await subreddit.submit(title, selftext=body)
        return RedditPost(
            id=submission.id,
            title=submission.title,
            body=submission.selftext,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁsubmit_post__mutmut_3(
        self, title: str, body: str
    ) -> RedditPost:
        """Submits a new post to Reddit."""
        subreddit = await self.reddit.subreddit("XXtestXX")
        submission = await subreddit.submit(title, selftext=body)
        return RedditPost(
            id=submission.id,
            title=submission.title,
            body=submission.selftext,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁsubmit_post__mutmut_4(
        self, title: str, body: str
    ) -> RedditPost:
        """Submits a new post to Reddit."""
        subreddit = await self.reddit.subreddit("TEST")
        submission = await subreddit.submit(title, selftext=body)
        return RedditPost(
            id=submission.id,
            title=submission.title,
            body=submission.selftext,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁsubmit_post__mutmut_5(
        self, title: str, body: str
    ) -> RedditPost:
        """Submits a new post to Reddit."""
        subreddit = await self.reddit.subreddit("Test")
        submission = await subreddit.submit(title, selftext=body)
        return RedditPost(
            id=submission.id,
            title=submission.title,
            body=submission.selftext,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁsubmit_post__mutmut_6(
        self, title: str, body: str
    ) -> RedditPost:
        """Submits a new post to Reddit."""
        subreddit = await self.reddit.subreddit("test")
        submission = None
        return RedditPost(
            id=submission.id,
            title=submission.title,
            body=submission.selftext,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁsubmit_post__mutmut_7(
        self, title: str, body: str
    ) -> RedditPost:
        """Submits a new post to Reddit."""
        subreddit = await self.reddit.subreddit("test")
        submission = await subreddit.submit(None, selftext=body)
        return RedditPost(
            id=submission.id,
            title=submission.title,
            body=submission.selftext,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁsubmit_post__mutmut_8(
        self, title: str, body: str
    ) -> RedditPost:
        """Submits a new post to Reddit."""
        subreddit = await self.reddit.subreddit("test")
        submission = await subreddit.submit(title, selftext=None)
        return RedditPost(
            id=submission.id,
            title=submission.title,
            body=submission.selftext,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁsubmit_post__mutmut_9(
        self, title: str, body: str
    ) -> RedditPost:
        """Submits a new post to Reddit."""
        subreddit = await self.reddit.subreddit("test")
        submission = await subreddit.submit(selftext=body)
        return RedditPost(
            id=submission.id,
            title=submission.title,
            body=submission.selftext,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁsubmit_post__mutmut_10(
        self, title: str, body: str
    ) -> RedditPost:
        """Submits a new post to Reddit."""
        subreddit = await self.reddit.subreddit("test")
        submission = await subreddit.submit(
            title,
        )
        return RedditPost(
            id=submission.id,
            title=submission.title,
            body=submission.selftext,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁsubmit_post__mutmut_11(
        self, title: str, body: str
    ) -> RedditPost:
        """Submits a new post to Reddit."""
        subreddit = await self.reddit.subreddit("test")
        submission = await subreddit.submit(title, selftext=body)
        return RedditPost(
            id=None,
            title=submission.title,
            body=submission.selftext,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁsubmit_post__mutmut_12(
        self, title: str, body: str
    ) -> RedditPost:
        """Submits a new post to Reddit."""
        subreddit = await self.reddit.subreddit("test")
        submission = await subreddit.submit(title, selftext=body)
        return RedditPost(
            id=submission.id,
            title=None,
            body=submission.selftext,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁsubmit_post__mutmut_13(
        self, title: str, body: str
    ) -> RedditPost:
        """Submits a new post to Reddit."""
        subreddit = await self.reddit.subreddit("test")
        submission = await subreddit.submit(title, selftext=body)
        return RedditPost(
            id=submission.id,
            title=submission.title,
            body=None,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁsubmit_post__mutmut_14(
        self, title: str, body: str
    ) -> RedditPost:
        """Submits a new post to Reddit."""
        subreddit = await self.reddit.subreddit("test")
        submission = await subreddit.submit(title, selftext=body)
        return RedditPost(
            id=submission.id,
            title=submission.title,
            body=submission.selftext,
            url=None,
        )

    async def xǁPrawManagerǁsubmit_post__mutmut_15(
        self, title: str, body: str
    ) -> RedditPost:
        """Submits a new post to Reddit."""
        subreddit = await self.reddit.subreddit("test")
        submission = await subreddit.submit(title, selftext=body)
        return RedditPost(
            title=submission.title,
            body=submission.selftext,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁsubmit_post__mutmut_16(
        self, title: str, body: str
    ) -> RedditPost:
        """Submits a new post to Reddit."""
        subreddit = await self.reddit.subreddit("test")
        submission = await subreddit.submit(title, selftext=body)
        return RedditPost(
            id=submission.id,
            body=submission.selftext,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁsubmit_post__mutmut_17(
        self, title: str, body: str
    ) -> RedditPost:
        """Submits a new post to Reddit."""
        subreddit = await self.reddit.subreddit("test")
        submission = await subreddit.submit(title, selftext=body)
        return RedditPost(
            id=submission.id,
            title=submission.title,
            url=submission.shortlink,
        )

    async def xǁPrawManagerǁsubmit_post__mutmut_18(
        self, title: str, body: str
    ) -> RedditPost:
        """Submits a new post to Reddit."""
        subreddit = await self.reddit.subreddit("test")
        submission = await subreddit.submit(title, selftext=body)
        return RedditPost(
            id=submission.id,
            title=submission.title,
            body=submission.selftext,
        )

    xǁPrawManagerǁsubmit_post__mutmut_mutants: ClassVar[MutantDict] = {
        "xǁPrawManagerǁsubmit_post__mutmut_1": xǁPrawManagerǁsubmit_post__mutmut_1,
        "xǁPrawManagerǁsubmit_post__mutmut_2": xǁPrawManagerǁsubmit_post__mutmut_2,
        "xǁPrawManagerǁsubmit_post__mutmut_3": xǁPrawManagerǁsubmit_post__mutmut_3,
        "xǁPrawManagerǁsubmit_post__mutmut_4": xǁPrawManagerǁsubmit_post__mutmut_4,
        "xǁPrawManagerǁsubmit_post__mutmut_5": xǁPrawManagerǁsubmit_post__mutmut_5,
        "xǁPrawManagerǁsubmit_post__mutmut_6": xǁPrawManagerǁsubmit_post__mutmut_6,
        "xǁPrawManagerǁsubmit_post__mutmut_7": xǁPrawManagerǁsubmit_post__mutmut_7,
        "xǁPrawManagerǁsubmit_post__mutmut_8": xǁPrawManagerǁsubmit_post__mutmut_8,
        "xǁPrawManagerǁsubmit_post__mutmut_9": xǁPrawManagerǁsubmit_post__mutmut_9,
        "xǁPrawManagerǁsubmit_post__mutmut_10": xǁPrawManagerǁsubmit_post__mutmut_10,
        "xǁPrawManagerǁsubmit_post__mutmut_11": xǁPrawManagerǁsubmit_post__mutmut_11,
        "xǁPrawManagerǁsubmit_post__mutmut_12": xǁPrawManagerǁsubmit_post__mutmut_12,
        "xǁPrawManagerǁsubmit_post__mutmut_13": xǁPrawManagerǁsubmit_post__mutmut_13,
        "xǁPrawManagerǁsubmit_post__mutmut_14": xǁPrawManagerǁsubmit_post__mutmut_14,
        "xǁPrawManagerǁsubmit_post__mutmut_15": xǁPrawManagerǁsubmit_post__mutmut_15,
        "xǁPrawManagerǁsubmit_post__mutmut_16": xǁPrawManagerǁsubmit_post__mutmut_16,
        "xǁPrawManagerǁsubmit_post__mutmut_17": xǁPrawManagerǁsubmit_post__mutmut_17,
        "xǁPrawManagerǁsubmit_post__mutmut_18": xǁPrawManagerǁsubmit_post__mutmut_18,
    }

    def submit_post(self, *args, **kwargs):
        result = _mutmut_trampoline(
            object.__getattribute__(self, "xǁPrawManagerǁsubmit_post__mutmut_orig"),
            object.__getattribute__(self, "xǁPrawManagerǁsubmit_post__mutmut_mutants"),
            args,
            kwargs,
            self,
        )
        return result

    submit_post.__signature__ = _mutmut_signature(
        xǁPrawManagerǁsubmit_post__mutmut_orig
    )
    xǁPrawManagerǁsubmit_post__mutmut_orig.__name__ = "xǁPrawManagerǁsubmit_post"

    async def close(self) -> None:
        """Closes the Reddit session."""
        await self.reddit.close()
