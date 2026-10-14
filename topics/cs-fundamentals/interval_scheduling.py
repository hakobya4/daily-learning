"""
Day 24, Task 10 -- CS fundamentals: weighted job scheduling (DP + binary search).

THE PROBLEM
------------
Each job is a tuple (start, end, profit) with start < end. Two jobs are
compatible if one ends at or before the other starts (end <= start). Return
the MAXIMUM total profit of a set of pairwise compatible jobs.

  max_profit([(1, 3, 50), (2, 5, 20), (3, 6, 100), (5, 8, 60)]) == 150
  (jobs (1,3) and (3,6): touching endpoints are fine)

max_profit([]) == 0. The input is not mutated. Target O(n log n).

HOW TO WORK THROUGH THIS
-------------------------
Sort by end time. dp[i] = best profit using the first i jobs. For job i find
(bisect_right on the end times, with job i's start) how many earlier jobs end
<= its start, then dp[i] = max(dp[i-1], profit_i + dp[that count]).

Run: python3 interval_scheduling.py
"""


def max_profit(jobs: list) -> int:
    raise NotImplementedError


def _run_tests():
    assert max_profit([]) == 0
    assert max_profit([(1, 2, 5)]) == 5
    assert max_profit([(1, 3, 50), (3, 6, 100)]) == 150  # touching is fine
    assert max_profit([(1, 3, 50), (2, 5, 20), (3, 6, 100), (5, 8, 60)]) == 150
    assert max_profit([(1, 10, 100), (1, 3, 40), (3, 6, 40), (6, 10, 40)]) == 120
    assert max_profit([(1, 10, 100), (1, 3, 40), (3, 6, 40), (6, 10, 10)]) == 100
    jobs = [(3, 5, 1), (1, 2, 1)]
    max_profit(jobs)
    assert jobs == [(3, 5, 1), (1, 2, 1)]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
