# Basic type stubs for pydantic_settings
from typing import TypeVar

T = TypeVar("T")

class BaseSettings:
    def __init__(self, **kwargs: T) -> None: ...

class SettingsConfigDict:
    def __init__(self, **kwargs: T) -> None: ...
