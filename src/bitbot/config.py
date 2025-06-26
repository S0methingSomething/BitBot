from pydantic import BaseModel, Field
from typing import List, Dict

# Define sub-models for clarity and strictness
class GitHubConfig(BaseModel):
    sourceRepo: str
    botRepo: str
    assetFileName: str

class RedditConfig(BaseModel):
    subreddit: str
    creator: str
    botName: str
    state_issue_number: int

class FeedbackConfig(BaseModel):
    statusLineRegex: str
    labels: Dict[str, str]
    workingKeywords: List[str]
    notWorkingKeywords: List[str]
    minFeedbackCount: int = Field(gt=0)

class TimingConfig(BaseModel):
    firstCheck: int = Field(gt=0)
    maxWait: int = Field(gt=0)
    increaseBy: int = Field(gt=0)

class Config(BaseModel):
    """The main application configuration model."""
    github: GitHubConfig
    reddit: RedditConfig
    outdatedPostHandling: Dict
    messages: Dict[str, str]
    feedback: FeedbackConfig
    timing: TimingConfig
    skipContent: Dict[str, str]
    templates: Dict[str, str]

class BotState(BaseModel):
    """A model for the bot's persistent state."""
    activePostId: str | None = None
    lastCheckTimestamp: str
    currentIntervalSeconds: int
    lastCommentCount: int
