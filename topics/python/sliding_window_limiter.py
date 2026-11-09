"""
Day 48, Task 3 -- Python: sliding-window-log rate limiter.

THE PROBLEM
------------
Implement class SlidingWindowLimiter(limit, window).
allow(key, ts) -> bool: ts is a non-decreasing timestamp (seconds). A request is
allowed if fewer than `limit` ALLOWED requests for that key have a timestamp t with
ts - window < t <= ts. Allowed requests are recorded; rejected ones are NOT.
Keys are independent. Aim for amortized O(1): keep a deque of timestamps per key and
pop expired ones from the left.

Run: python3 sliding_window_limiter.py
"""


class SlidingWindowLimiter:
    def __init__(self, limit, window):
        from collections import deque
        self.limit = limit
        self.window = window
        self._deque = deque
        self.log = {}

    def allow(self, key, ts):
        q = self.log.setdefault(key, self._deque())
        while q and q[0] <= ts - self.window:
            q.popleft()
        if len(q) < self.limit:
            q.append(ts)
            return True
        return False


def _run_tests():
    lim = SlidingWindowLimiter(2, 10)
    assert lim.allow("a", 1) is True
    assert lim.allow("a", 2) is True
    assert lim.allow("a", 3) is False      # rejected, not recorded
    assert lim.allow("b", 3) is True       # independent key
    assert lim.allow("a", 11) is True      # ts=1 expired (11-10=1 is not > 1)
    assert lim.allow("a", 12) is True      # ts=2 expired
    assert lim.allow("a", 13) is False     # 11 and 12 still in window
    assert lim.allow("a", 22) is True      # 12 expired (22-10=12), 11 expired
    one = SlidingWindowLimiter(1, 5)
    assert one.allow("k", 0) is True
    assert one.allow("k", 4) is False
    assert one.allow("k", 5) is True
    assert one.allow("k", 9) is False
    assert one.allow("k", 10) is True
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
