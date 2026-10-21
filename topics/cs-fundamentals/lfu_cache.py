"""
Day 31, Task 9 -- CS fundamentals: LFU cache.

THE PROBLEM
------------
Implement LFUCache(capacity) with:
  get(key)        -> value, or -1 if missing. Counts as a use.
  put(key, value) -> insert or update (an update counts as a use). When the
                     cache is full, first evict the LEAST FREQUENTLY used
                     key; ties are broken by evicting the LEAST RECENTLY
                     used among them. Capacity 0 stores nothing.
Both operations should be O(1) average.

HOW TO WORK THROUGH THIS
-------------------------
Keep key -> (value, freq), plus freq -> OrderedDict of keys (oldest first),
and a min_freq counter. On every use move the key from bucket f to f+1;
if bucket f was min_freq and is now empty, min_freq += 1. A brand-new key
resets min_freq to 1.

Run: python3 lfu_cache.py
"""


class LFUCache:
    def __init__(self, capacity: int):
        raise NotImplementedError

    def get(self, key: int) -> int:
        raise NotImplementedError

    def put(self, key: int, value: int) -> None:
        raise NotImplementedError


def _run_tests():
    c = LFUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)            # evicts 2 (freq 1)
    assert c.get(2) == -1
    assert c.get(3) == 3
    c.put(4, 4)            # 1 and 3 both freq 2 -> evict LRU = 1
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4

    z = LFUCache(0)
    z.put(1, 1)
    assert z.get(1) == -1

    u = LFUCache(2)
    u.put(1, 1)
    u.put(2, 2)
    u.put(1, 10)           # update counts as a use
    u.put(3, 3)            # evicts 2
    assert u.get(2) == -1
    assert u.get(1) == 10
    assert u.get(3) == 3

    t = LFUCache(2)
    t.put(1, 1)
    t.put(2, 2)            # both freq 1, 1 is older
    t.put(3, 3)            # evicts 1
    assert t.get(1) == -1
    assert t.get(2) == 2
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
