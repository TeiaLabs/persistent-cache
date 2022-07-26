from __future__ import annotations

from abc import abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class CacheBase(Generic[T]):
    @abstractmethod
    async def get(self, key: str) -> T | None:
        pass

    @abstractmethod
    async def multi_get(self, *keys: str) -> T:
        pass

    @abstractmethod
    async def set(self, key: str, value: T):
        pass

    @abstractmethod
    def __str__(self):
        pass