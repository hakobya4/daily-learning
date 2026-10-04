"""
Day 13, Task 8 -- CS fundamentals: 0/1 knapsack.

THE PROBLEM
------------
items is a list of (weight, value) pairs; each item can be used at most
once. knapsack(items, capacity) returns the maximum total value whose
total weight is <= capacity.

    items = [(1, 1), (3, 4), (4, 5), (5, 7)], capacity = 7  ->  9
    (take weights 3 and 4 -> value 4 + 5)

Also implement knapsack_items(items, capacity) -> sorted list of the
chosen item INDICES for one optimal solution (the tests only check that
the total weight fits and the total value is optimal).

Hint: dp[w] = best value with capacity w; iterate capacity DOWNWARD per
item for the 1-D version. For the item list keep the full 2-D table and
backtrack.

Run: python3 knapsack.py
"""


def knapsack(items: list[tuple[int, int]], capacity: int) -> int:
    dp = [0] * (capacity + 1)
    for w, v in items:
        for c in range(capacity, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]


def knapsack_items(items: list[tuple[int, int]], capacity: int) -> list[int]:
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i, (w, v) in enumerate(items, 1):
        for c in range(capacity + 1):
            dp[i][c] = dp[i - 1][c]
            if c >= w:
                dp[i][c] = max(dp[i][c], dp[i - 1][c - w] + v)
    chosen = []
    c = capacity
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            chosen.append(i - 1)
            c -= items[i - 1][0]
    return sorted(chosen)


def _run_tests() -> None:
    assert knapsack([], 10) == 0
    assert knapsack([(5, 10)], 4) == 0
    assert knapsack([(5, 10)], 5) == 10
    assert knapsack([(1, 1), (3, 4), (4, 5), (5, 7)], 7) == 9
    assert knapsack([(2, 3), (3, 4), (4, 5), (5, 6)], 5) == 7
    assert knapsack([(1, 5), (1, 5)], 1) == 5        # each item only once
    assert knapsack([(3, 0), (2, 0)], 10) == 0
    import random
    from itertools import combinations
    random.seed(13)
    for _ in range(100):
        items = [(random.randint(1, 8), random.randint(0, 20))
                 for _ in range(random.randint(0, 7))]
        cap = random.randint(0, 20)
        best = 0
        for r in range(len(items) + 1):
            for c in combinations(items, r):
                if sum(w for w, _ in c) <= cap:
                    best = max(best, sum(v for _, v in c))
        assert knapsack(items, cap) == best, (items, cap)
        idx = knapsack_items(items, cap)
        assert len(set(idx)) == len(idx)
        assert sum(items[i][0] for i in idx) <= cap
        assert sum(items[i][1] for i in idx) == best
    print("All knapsack tests passed.")


if __name__ == "__main__":
    _run_tests()
