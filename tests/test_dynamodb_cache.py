
from persistent_cache import DynamoDBCache
from torch import tensor

def test_multi_get():
    cache = DynamoDBCache('tab_test')
    print('->' , cache)
    cache.set('a', tensor([1,2,3]))
    cache.set('b', tensor([4,5,6]))
    cache.set('c', tensor([7,8,9]))


    print(cache.get('a'))
    print(cache.get('b'))
    print(cache.get('c'))
    print(cache.get('z'))
    print(cache.multi_get("a", "b", "c"))

test_multi_get()