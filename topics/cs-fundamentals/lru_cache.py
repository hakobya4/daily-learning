"""
Day 9, Task 8 -- CS fundamentals: LRU cache.

THE PROBLEM
------------
Implement class LRUCache(capacity) with:
  get(key)        -> value, or -1 if missing; marks key most-recently used
  put(key, value) -> insert/update; marks most-recently used; if size
                     exceeds capacity, evict the LEAST recently used key
Both operations should be O(1) average.

HOW TO WORK THROUGH THIS
-------------------------
Classic design: a hash map for lookup + a doubly linked list for
recency order. In Python you may use collections.OrderedDict
(move_to_end / popitem(last=False)) -- but for the real learning, try
the dict + hand-written doubly linked list version (sentinel head/tail
nodes make edge cases vanish) after you get the OrderedDict one working.

Run: python3 lru_cache.py
"""


class LRUCache:
    def __init__(self, capacity: int) -> None:
        raise NotImplementedError

    def get(self, key: int) -> int:
        raise NotImplementedError

    def put(self, key: int, value: int) -> None:
        raise NotImplementedError


def _run_tests() -> None:
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)            # evicts key 2
    assert c.get(2) == -1
    c.put(4, 4)            # evicts key 1
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4

    c2 = LRUCache(1)
    c2.put(5, 5)
    c2.put(5, 50)          # update, no eviction
    assert c2.get(5) == 50
    c2.put(6, 6)
    assert c2.get(5) == -1
    assert c2.get(6) == 6

    c3 = LRUCache(2)
    c3.put(1, 1)
    c3.put(2, 2)
    c3.get(1)              # 1 becomes most recent
    c3.put(1, 11)          # update also refreshes
    c3.put(3, 3)           # evicts 2
    assert c3.get(2) == -1
    assert c3.get(1) == 11
    print("All lru_cache tests passed.")


if __name__ == "__main__":
    _run_tests()
