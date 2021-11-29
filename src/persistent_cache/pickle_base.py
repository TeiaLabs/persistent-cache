from __future__ import annotations
import pickle

from pathlib import Path

from .mem_cache import CacheBase
from typing import Generic, TypeVar

T = TypeVar("T")


class PickleCache(CacheBase, Generic[T]):

    def __init__(self, pickle_file_path) -> None:
        super().__init__()
        self.pickle_file = Path(pickle_file_path)
        self.hash_dict = {}

        if self.pickle_file.exists() and self.pickle_file.stat().st_size > 0:
            with self.pickle_file.open('rb') as f:
                self.hash_dict = pickle.load(f)

    def get(self, key: str) -> T | None:
        if key in self.hash_dict:
            return self.hash_dict[key]
        else:
            return None

    def multi_get(self, *keys: str) -> list[T | None]:        
        return [self.hash_dict[k] for k in keys]

    def set(self, key: str, value: T):
        self.hash_dict[key] = value
        with self.pickle_file.open('wb') as f:
            pickle.dump(self.hash_dict, f)

    def __str__(self):
        return "".join(self.hash_dict.keys())

