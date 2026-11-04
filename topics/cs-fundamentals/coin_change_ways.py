"""
Day 44, Task 9 -- CS fundamentals: coin change, number of combinations.

THE PROBLEM
------------
coin_change_ways(amount, coins) returns the number of DISTINCT combinations
(order does not matter: 1+2 and 2+1 count once) of the given coins that sum
to amount. Each coin may be used unlimited times. amount 0 has exactly 1
combination (the empty one).
Hint: 1-D DP; loop over coins in the OUTER loop, amounts in the inner loop.

Run: python3 coin_change_ways.py
"""


def coin_change_ways(amount, coins):
    dp = [0] * (amount + 1)
    dp[0] = 1
    for c in coins:
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
    return dp[amount]


def _run_tests():
    assert coin_change_ways(5, [1, 2, 5]) == 4
    assert coin_change_ways(3, [2]) == 0
    assert coin_change_ways(10, [10]) == 1
    assert coin_change_ways(0, [1, 2]) == 1
    assert coin_change_ways(100, [1, 5, 10, 25]) == 242
    assert coin_change_ways(4, [1, 2, 3]) == 4
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
