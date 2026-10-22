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
        from collections import OrderedDict, defaultdict
        self.capacity = capacity
        self.vals = {}          # key -> (value, freq)
        self.buckets = defaultdict(OrderedDict)  # freq -> keys, oldest first
        self.min_freq = 0

    def _touch(self, key):
        value, f = self.vals[key]
        del self.buckets[f][key]
        if not self.buckets[f]:
            del self.buckets[f]
            if self.min_freq == f:
                self.min_freq += 1
        self.buckets[f + 1][key] = None
        self.vals[key] = (value, f + 1)

    def get(self, key: int) -> int:
        if key not in self.vals:
            return -1
        self._touch(key)
        return self.vals[key][0]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        if key in self.vals:
            f = self.vals[key][1]
            self.vals[key] = (value, f)
            self._touch(key)
            return
        if len(self.vals) >= self.capacity:
            old, _ = self.buckets[self.min_freq].popitem(last=False)
            if not self.buckets[self.min_freq]:
                del self.buckets[self.min_freq]
            del self.vals[old]
        self.vals[key] = (value, 1)
        self.buckets[1][key] = None
        self.min_freq = 1


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
