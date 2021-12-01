from __future__ import annotations

from typing import Generic, TypeVar

from .cache_base import CacheBase

T = TypeVar("T", bound=list)


class MemCache(CacheBase, Generic[T]):
    def __init__(self):
        self.cache = {}

    def get(self, key: str) -> T | None:
        if key in self.cache:
            return self.cache[key]
        
        return None

    def multi_get(self, *keys: str) -> list[T | None]:
        return [self.get(key) for key in keys]

    def set(self, key: str, value: T):
        self.cache[key] = value

    def __str__(self):
        return str(self.cache)