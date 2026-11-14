"""
Day 55, Task 2 -- Python: shortest subarray with sum at least K (negatives allowed).

THE PROBLEM
------------
Given a list of integers nums (which MAY contain negative numbers) and an integer k > 0,
return the length of the shortest non-empty CONTIGUOUS subarray whose sum is >= k.
Return -1 if there is no such subarray.

Why the usual sliding window fails: with negative numbers, shrinking the window from the
left can INCREASE the sum, so the two-pointer trick is no longer valid.

Example:
  nums = [2, -1, 2], k = 3   -> 3        (the whole array)
  nums = [1, 2], k = 4       -> -1
  nums = [84, -37, 32, 40, 95], k = 167 -> 3   ([32, 40, 95])

Hint: build prefix sums P[0..n] (P[0] = 0). You want the smallest j - i with
P[j] - P[i] >= k. Keep a deque of indices with INCREASING P values:
  * while P[j] - P[deque[0]] >= k: record j - deque[0] and pop it from the LEFT
    (no later j can use that i for a shorter answer);
  * while P[j] <= P[deque[-1]]: pop from the RIGHT (index j is a better start: later and
    no larger);
  * append j.
Overall O(n). Raise ValueError if k <= 0.

Run: python3 shortest_subarray_sum_at_least_k.py
"""


def shortest_subarray(nums, k):
    raise NotImplementedError


def _brute(nums, k):
    best = -1
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if s >= k:
                if best == -1 or j - i + 1 < best:
                    best = j - i + 1
                break
    return best


def _run_tests():
    assert shortest_subarray([1], 1) == 1
    assert shortest_subarray([1, 2], 4) == -1
    assert shortest_subarray([2, -1, 2], 3) == 3
    assert shortest_subarray([84, -37, 32, 40, 95], 167) == 3
    assert shortest_subarray([], 1) == -1
    assert shortest_subarray([-5, -1, -2], 1) == -1
    assert shortest_subarray([1, 1, 1, 10], 10) == 1
    assert shortest_subarray([5, -10, 3, 3], 6) == 2        # negative splits the array
    assert shortest_subarray([-28, 81, -20, 28, -29], 89) == 3
    assert shortest_subarray([48, 99, 37, 4, -31], 140) == 2

    # Randomised cross-check against the O(n^2) brute force.
    import random
    rng = random.Random(55)
    for _ in range(500):
        n = rng.randint(0, 25)
        nums = [rng.randint(-20, 30) for _ in range(n)]
        k = rng.randint(1, 80)
        assert shortest_subarray(nums, k) == _brute(nums, k), (nums, k)

    # Large input must be linear-ish.
    big = [1] * 300_000
    assert shortest_subarray(big, 150_000) == 150_000

    for bad_k in (0, -3):
        try:
            shortest_subarray([1, 2, 3], bad_k)
        except ValueError:
            pass
        else:
            raise AssertionError("k <= 0 must raise ValueError")

    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
