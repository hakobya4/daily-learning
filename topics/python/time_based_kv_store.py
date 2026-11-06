"""
Day 47, Task 2 -- Python: time-based key-value store (binary search).

THE PROBLEM
------------
Implement TimeMap:
  set(key, value, timestamp)  -- store value for key at timestamp. For a given
                                 key, timestamps are passed in strictly increasing order.
  get(key, timestamp)         -- return the value stored with the LARGEST
                                 timestamp' <= timestamp, or "" if there is none
                                 (unknown key, or all stored timestamps are later).
get must be O(log n) per call.
Hint: per key keep two parallel lists (timestamps, values) and use bisect_right.

Run: python3 time_based_kv_store.py
"""


class TimeMap:
    def __init__(self):
        raise NotImplementedError

    def set(self, key, value, timestamp):
        raise NotImplementedError

    def get(self, key, timestamp):
        raise NotImplementedError


def _run_tests():
    tm = TimeMap()
    tm.set("foo", "bar", 1)
    assert tm.get("foo", 1) == "bar"
    assert tm.get("foo", 3) == "bar"
    tm.set("foo", "bar2", 4)
    assert tm.get("foo", 4) == "bar2"
    assert tm.get("foo", 5) == "bar2"
    assert tm.get("foo", 3) == "bar"
    assert tm.get("foo", 0) == ""
    assert tm.get("missing", 10) == ""
    tm.set("a", "x", 10)
    tm.set("a", "y", 20)
    tm.set("a", "z", 30)
    assert tm.get("a", 9) == ""
    assert tm.get("a", 10) == "x"
    assert tm.get("a", 25) == "y"
    assert tm.get("a", 10**9) == "z"
    big = TimeMap()
    for t in range(1, 50001):
        big.set("k", str(t), t)
    assert big.get("k", 25000) == "25000"
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
