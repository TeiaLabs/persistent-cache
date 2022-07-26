from __future__ import annotations

import io
import pymongo
import torch
import zlib

from bson import Binary
from mongow import BaseMixin
from torch import Tensor
from typing import Generic, TypeVar

from .mem_cache import CacheBase


T = TypeVar("T")


class CacheItem(BaseMixin):
    key: str
    data: Binary

    __collection__: str = 'cache_item'
    __indices__ = [
        pymongo.IndexModel(
            [("key", pymongo.ASCENDING)],
            unique=True,
        )
    ]

class MongoCache(CacheBase, Generic[T]):

    def __init__(self) -> None:
        super().__init__()
        self.hash_dict = {}

    async def get(self, key: str) -> T | None:
        item = await CacheItem.read(filters=dict(key=key))
        if item:
            cache = CacheItem(**item[0])
            read_buffer = io.BytesIO(zlib.decompress(bytes(cache.data)))
            return torch.load(read_buffer)

        return None

    async def multi_get(self, *keys: str) -> list[T | None]:
        return None

    async def set(self, key: str, value: Tensor):
        item_buffer = io.BytesIO()
        torch.save(value, item_buffer)
        item_buffer.seek(0)
        item_buffer = item_buffer.read()
        item_buffer = zlib.compress(item_buffer)
        item_buffer = Binary(item_buffer)

        item = CacheItem(key=key, data=item_buffer)
        try:
            await CacheItem.create(item)
        except Exception as e:
            print(e)
            print(f'Error saving {key} to mongo')
