"""
Day 36, Task 9 -- CS fundamentals: min cost climbing stairs (1-D DP).

THE PROBLEM
------------
cost[i] is the price of stepping ON stair i. From a stair you may climb 1
or 2 stairs up. You may start on stair 0 or stair 1. The "top" is one step
past the last stair. Return the minimum total cost to reach the top.

  [10, 15, 20]                     -> 15   (start at 1, jump to top)
  [1,100,1,1,1,100,1,1,100,1]      -> 6
  []  or  [x]                      -> 0

HOW TO WORK THROUGH THIS
-------------------------
Let best[i] = min cost to have paid for stair i and be standing on it:
best[i] = cost[i] + min(best[i-1], best[i-2]). The answer is
min(best[n-1], best[n-2]). Only the last two values are needed (O(1) space).

Run: python3 min_cost_climbing_stairs.py
"""


def min_cost(cost: list[int]) -> int:
    if len(cost) < 2:
        return 0
    prev2, prev1 = cost[0], cost[1]
    for i in range(2, len(cost)):
        prev2, prev1 = prev1, cost[i] + min(prev1, prev2)
    return min(prev1, prev2)


def _run_tests():
    assert min_cost([10, 15, 20]) == 15
    assert min_cost([1, 100, 1, 1, 1, 100, 1, 1, 100, 1]) == 6
    assert min_cost([]) == 0
    assert min_cost([7]) == 0
    assert min_cost([5, 3]) == 3
    assert min_cost([0, 0, 0, 0]) == 0
    assert min_cost([1, 2, 3, 4, 5, 6]) == 9
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
