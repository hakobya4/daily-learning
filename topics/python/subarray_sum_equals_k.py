"""
Day 45, Task 3 -- Python: count subarrays with sum k (prefix sums).

THE PROBLEM
------------
subarray_sum(nums, k) returns how many CONTIGUOUS, non-empty subarrays of
nums sum to k. nums may contain negatives and zeros. Target O(n).
Hint: running prefix sum plus a dict counting earlier prefix sums
(look up prefix - k).

Run: python3 subarray_sum_equals_k.py
"""


def subarray_sum(nums, k):
    seen = {0: 1}
    prefix = 0
    count = 0
    for x in nums:
        prefix += x
        count += seen.get(prefix - k, 0)
        seen[prefix] = seen.get(prefix, 0) + 1
    return count


def _run_tests():
    assert subarray_sum([1, 1, 1], 2) == 2
    assert subarray_sum([1, 2, 3], 3) == 2
    assert subarray_sum([], 0) == 0
    assert subarray_sum([0, 0, 0], 0) == 6
    assert subarray_sum([1, -1, 0], 0) == 3
    assert subarray_sum([3, 4, 7, 2, -3, 1, 4, 2], 7) == 4
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
