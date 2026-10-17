"""
Day 26, Task 4 -- Python: subarray sum equals k.

THE PROBLEM
------------
count_subarrays(nums, k) returns the number of contiguous, non-empty
subarrays whose sum equals k. nums may contain negatives and zeros, so a
plain sliding window does NOT work.

  count_subarrays([1, 1, 1], 2)  -> 2
  count_subarrays([1, 2, 3], 3)  -> 2   ([1,2] and [3])

HOW TO WORK THROUGH THIS
-------------------------
Prefix sums + a dict: at each position, the number of earlier prefixes
equal to (prefix - k) is the number of subarrays ending here. Seed the
dict with {0: 1}. O(n).

Run: python3 subarray_sum_k.py
"""


def count_subarrays(nums: list, k: int) -> int:
    seen = {0: 1}
    prefix = 0
    total = 0
    for x in nums:
        prefix += x
        total += seen.get(prefix - k, 0)
        seen[prefix] = seen.get(prefix, 0) + 1
    return total


def _run_tests():
    assert count_subarrays([1, 1, 1], 2) == 2
    assert count_subarrays([1, 2, 3], 3) == 2
    assert count_subarrays([], 0) == 0
    assert count_subarrays([0, 0, 0], 0) == 6
    assert count_subarrays([-1, -1, 1], 0) == 1
    assert count_subarrays([1, -1, 0], 0) == 3
    assert count_subarrays([3, 4, 7, 2, -3, 1, 4, 2], 7) == 4
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
