"""
Day 11, Task 2 -- Python: token-bucket rate limiter.

THE PROBLEM
------------
Implement class TokenBucket(capacity, refill_rate, clock):

  - capacity: max tokens the bucket holds (int > 0). Starts FULL.
  - refill_rate: tokens added per second (float > 0), added continuously.
  - clock: a zero-argument callable returning the current time in
    seconds (injected so tests can fake time; do NOT call time.time()).

  allow(n=1) -> bool
      If at least n tokens are available (after refilling for elapsed
      time, capped at capacity) consume them and return True. Otherwise
      consume nothing and return False. Raise ValueError if n <= 0 or
      n > capacity.

  tokens() -> float
      Current token count after refilling.

HOW TO WORK THROUGH THIS
-------------------------
Store the token count and the time of the last update. Refill lazily
inside a private _refill() that both methods call.

Run: python3 token_bucket.py
"""


class TokenBucket:
    def __init__(self, capacity, refill_rate, clock):
        raise NotImplementedError

    def allow(self, n=1):
        raise NotImplementedError

    def tokens(self):
        raise NotImplementedError


def _run_tests() -> None:
    now = [0.0]
    b = TokenBucket(5, 1.0, lambda: now[0])
    assert b.tokens() == 5
    assert b.allow(3) is True
    assert abs(b.tokens() - 2) < 1e-9
    assert b.allow(3) is False          # only 2 left, nothing consumed
    assert abs(b.tokens() - 2) < 1e-9
    now[0] += 2.0                       # +2 tokens -> 4
    assert abs(b.tokens() - 4) < 1e-9
    assert b.allow(4) is True
    assert b.allow() is False
    now[0] += 0.5
    assert b.allow() is False           # 0.5 tokens, not enough
    now[0] += 0.5
    assert b.allow() is True            # exactly 1 token
    now[0] += 1000                      # refill is capped at capacity
    assert b.tokens() == 5
    for bad in (0, -1, 6):
        try:
            b.allow(bad)
            assert False, f"should reject n={bad}"
        except ValueError:
            pass
    print("All token_bucket tests passed.")


if __name__ == "__main__":
    _run_tests()
