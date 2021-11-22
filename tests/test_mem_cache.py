
from persistent_cache import MemCache


def test_multi_get():
    cache = MemCache()
    cache.set("a", 1)
    cache.set("b", 2)
    cache.set("c", 3)
    assert cache.multi_get("a", "b", "c") == [1, 2, 3]
