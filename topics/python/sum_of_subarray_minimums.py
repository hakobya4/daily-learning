"""
Day 54, Task 2 -- Python: sum of subarray minimums (contribution technique + monotonic stack).

THE PROBLEM
------------
Given a list of integers arr, return the sum of min(sub) over EVERY contiguous non-empty
subarray sub of arr, modulo 1_000_000_007.

Example: arr = [3, 1, 2, 4]. Subarrays and their minimums:
  [3]=3 [1]=1 [2]=2 [4]=4 [3,1]=1 [1,2]=1 [2,4]=2 [3,1,2]=1 [1,2,4]=1 [3,1,2,4]=1
  total = 17.

Enumerating all O(n^2) subarrays is too slow for n = 100_000. Think per element instead:
arr[i] is the minimum of left[i] * right[i] subarrays, where left[i] = how many start
positions it can extend to on the left and right[i] = how many end positions on the right.
Hint: compute "previous smaller" and "next smaller" indices with a monotonic stack. With
DUPLICATE values, use strict < on one side and <= on the other so every subarray's minimum
is counted exactly once. Answer = sum(arr[i] * left[i] * right[i]) mod 1e9+7.
An empty list returns 0. Values may be 0 or negative (Python's % keeps the result in 0..mod-1).

Run: python3 sum_of_subarray_minimums.py
"""

MOD = 1_000_000_007


def sum_subarray_mins(arr):
    n = len(arr)
    left = [0] * n   # distance to previous strictly smaller element
    right = [0] * n  # distance to next smaller-or-equal element
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        left[i] = i - stack[-1] if stack else i + 1
        stack.append(i)
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]:
            stack.pop()
        right[i] = stack[-1] - i if stack else n - i
        stack.append(i)
    total = 0
    for i in range(n):
        total += arr[i] * left[i] * right[i]
    return total % MOD


def _brute(arr):
    total = 0
    for i in range(len(arr)):
        m = arr[i]
        for j in range(i, len(arr)):
            m = min(m, arr[j])
            total += m
    return total % MOD


def _run_tests():
    assert sum_subarray_mins([3, 1, 2, 4]) == 17
    assert sum_subarray_mins([11, 81, 94, 43, 3]) == 444
    assert sum_subarray_mins([]) == 0
    assert sum_subarray_mins([5]) == 5
    assert sum_subarray_mins([2, 2, 2]) == 12            # duplicates counted exactly once
    assert sum_subarray_mins([1, 2, 3]) == 10
    assert sum_subarray_mins([3, 2, 1]) == 10
    assert sum_subarray_mins([0, 0]) == 0
    assert sum_subarray_mins([-1, 2]) == (-1 + 2 + -1) % MOD

    import random
    rng = random.Random(54)
    for _ in range(300):
        arr = [rng.randint(-5, 9) for _ in range(rng.randint(0, 12))]
        assert sum_subarray_mins(arr) == _brute(arr), arr

    # Large input must be fast and reduced modulo 1e9+7.
    big = [30_000] * 100_000
    n = len(big)
    assert sum_subarray_mins(big) == (30_000 * n * (n + 1) // 2) % MOD

    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
