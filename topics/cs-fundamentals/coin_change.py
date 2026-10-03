"""
Day 12, Task 8 -- CS fundamentals: coin change (dynamic programming).

THE PROBLEM
------------
Implement two functions; coins is a list of distinct positive ints with
unlimited supply of each.

  min_coins(coins, amount) -> int
      Fewest coins summing exactly to amount, or -1 if impossible.
      amount 0 needs 0 coins. Raise ValueError if amount < 0.

  count_ways(coins, amount) -> int
      Number of distinct COMBINATIONS (order does not matter) summing to
      amount. count_ways(any, 0) == 1.

HOW TO WORK THROUGH THIS
-------------------------
min_coins: dp[x] = 1 + min(dp[x - c]) over coins c <= x.
count_ways: loop coins in the OUTER loop and amounts in the inner loop
(that ordering counts combinations; swapping the loops counts
permutations -- try both to see the difference).

Run: python3 coin_change.py
"""


def min_coins(coins, amount):
    if amount < 0:
        raise ValueError("amount must be >= 0")
    INF = float("inf")
    dp = [0] + [INF] * amount
    for x in range(1, amount + 1):
        for c in coins:
            if c <= x and dp[x - c] + 1 < dp[x]:
                dp[x] = dp[x - c] + 1
    return -1 if dp[amount] == INF else dp[amount]


def count_ways(coins, amount):
    if amount < 0:
        return 0
    dp = [1] + [0] * amount
    for c in coins:
        for x in range(c, amount + 1):
            dp[x] += dp[x - c]
    return dp[amount]


def _run_tests() -> None:
    assert min_coins([1, 2, 5], 11) == 3
    assert min_coins([2], 3) == -1
    assert min_coins([1], 0) == 0
    assert min_coins([186, 419, 83, 408], 6249) == 20
    assert min_coins([5, 10], 7) == -1
    assert min_coins([1, 3, 4], 6) == 2             # greedy would say 3
    assert count_ways([1, 2, 5], 5) == 4
    assert count_ways([2], 3) == 0
    assert count_ways([10], 10) == 1
    assert count_ways([1, 2, 3], 4) == 4
    assert count_ways([5, 3], 0) == 1
    assert count_ways([1, 5, 10, 25, 50], 100) == 292
    try:
        min_coins([1], -1)
        assert False
    except ValueError:
        pass
    print("All coin_change tests passed.")


if __name__ == "__main__":
    _run_tests()
