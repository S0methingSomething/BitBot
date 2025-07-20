"""A service for managing Reddit interactions."""

from typing import Any, List, Optional

import asyncpraw

from ..data.models import RedditPost
from ..interfaces.reddit_protocol import RedditManagerProtocol


class PrawManager(RedditManagerProtocol):
    """Manages Reddit interactions using PRAW."""

    def __init__(
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

    async def get_post_by_id(self, post_id: str) -> Optional[RedditPost]:
        """Gets a Reddit post by its ID."""
        submission = await self.reddit.submission(submission_id=post_id)
        return RedditPost(
            id=submission.id,
            title=submission.title,
            body=submission.selftext,
            url=submission.shortlink,
        )

    async def get_comments(self, post: RedditPost) -> List[Any]:
        """Gets the comments from a Reddit post."""
        submission = await self.reddit.submission(submission_id=post.id)
        await submission.comments.replace_more(limit=0)
        comments = await submission.comments.list()
        return list(comments)

    async def get_recent_bot_posts(self, limit: int) -> List[RedditPost]:
        """Gets a list of recent posts made by the bot."""
        bot_user = await self.reddit.user.me()
        if not bot_user:
            return []
        submissions = bot_user.submissions.new(limit=limit)
        return [
            RedditPost(id=s.id, title=s.title, body=s.selftext, url=s.shortlink)
            async for s in submissions
        ]

    async def update_post_body(self, post_id: str, new_body: str) -> None:
        """Updates the body of a Reddit post."""
        submission = await self.reddit.submission(submission_id=post_id)
        await submission.edit(body=new_body)

    async def submit_post(self, title: str, body: str) -> RedditPost:
        """Submits a new post to Reddit."""
        subreddit = await self.reddit.subreddit("test")
        submission = await subreddit.submit(title, selftext=body)
        return RedditPost(
            id=submission.id,
            title=submission.title,
            body=submission.selftext,
            url=submission.shortlink,
        )

    async def close(self) -> None:
        """Closes the Reddit session."""
        await self.reddit.close()
