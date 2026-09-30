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


class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: int = 0, value: int = 0) -> None:
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.map = {}
        self.head = _Node()   # sentinel: most recent side
        self.tail = _Node()   # sentinel: least recent side
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: _Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node: _Node) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        node = self.map.get(key)
        if node is None:
            return -1
        self._remove(node)
        self._add_front(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        node = self.map.get(key)
        if node is not None:
            node.value = value
            self._remove(node)
            self._add_front(node)
            return
        if self.capacity <= 0:
            return
        if len(self.map) >= self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]
        node = _Node(key, value)
        self.map[key] = node
        self._add_front(node)


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
