"""
Day 54, Task 7 -- CS fundamentals: burst balloons (interval DP, "last one to go").

THE PROBLEM
------------
There are n balloons in a row with non-negative values nums[0..n-1]. Bursting balloon i
earns nums[left] * nums[i] * nums[right], where left and right are its CURRENT neighbours
(balloons already burst are gone, so neighbours change). A missing neighbour past either end
counts as 1. Burst all balloons; return the maximum total coins.

Example: nums = [3, 1, 5, 8] -> 167
  burst 1: 3*1*5 = 15  -> [3,5,8]
  burst 5: 3*5*8 = 120 -> [3,8]
  burst 3: 1*3*8 = 24  -> [8]
  burst 8: 1*8*1 = 8   -> total 167

Trying every order is O(n!). Aim for O(n^3).
Hint: thinking about the FIRST balloon to burst gives subproblems that are not independent.
Think about the LAST balloon k to burst inside an open interval (i, j) instead: when it
goes, its neighbours are exactly i and j. Pad the list as [1] + nums + [1] and let
dp[i][j] = best coins from bursting everything strictly between i and j:
  dp[i][j] = max over i<k<j of dp[i][k] + vals[i]*vals[k]*vals[j] + dp[k][j]
Fill by increasing interval length. An empty list returns 0.
Raise ValueError if any value is negative.

Run: python3 burst_balloons.py
"""


def max_coins(nums):
    raise NotImplementedError


def _brute(nums):
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def go(t):
        if not t:
            return 0
        best = 0
        for i in range(len(t)):
            left = t[i - 1] if i > 0 else 1
            right = t[i + 1] if i + 1 < len(t) else 1
            best = max(best, left * t[i] * right + go(t[:i] + t[i + 1:]))
        return best

    return go(tuple(nums))


def _run_tests():
    assert max_coins([3, 1, 5, 8]) == 167
    assert max_coins([1, 5]) == 10
    assert max_coins([]) == 0
    assert max_coins([7]) == 7
    assert max_coins([0, 0, 0]) == 0
    assert max_coins([2, 3]) == 9                  # burst 2 (1*2*3=6) then 3 (1*3*1=3)

    import random
    rng = random.Random(54)
    for _ in range(150):
        nums = [rng.randint(0, 9) for _ in range(rng.randint(0, 7))]
        assert max_coins(nums) == _brute(nums), nums

    # n = 120 must finish in a second or two with the O(n^3) DP.
    big = [(i * 37) % 10 for i in range(120)]
    assert max_coins(big) > 0

    try:
        max_coins([1, -2])
    except ValueError:
        pass
    else:
        raise AssertionError("negative value must raise ValueError")

    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
