"""
Day 38, Task 3 -- Python: count subarrays with product less than k.

THE PROBLEM
------------
Given a list nums of positive integers and an integer k, return the number
of contiguous, non-empty subarrays whose product is strictly less than k.

  ([10, 5, 2, 6], 100) -> 8
  ([1, 2, 3], 0)       -> 0
  ([1, 1, 1], 2)       -> 6

HOW TO WORK THROUGH THIS
-------------------------
Sliding window: keep a running product for window [left..right]; while it is
>= k shrink from the left (divide). Each right end adds (right - left + 1)
new subarrays. Watch the k <= 1 edge case (nothing can qualify). O(n).

Run: python3 subarray_product_less_k.py
"""


def num_subarray_product_less_than_k(nums: list, k: int) -> int:
    raise NotImplementedError


def _run_tests():
    assert num_subarray_product_less_than_k([10, 5, 2, 6], 100) == 8
    assert num_subarray_product_less_than_k([1, 2, 3], 0) == 0
    assert num_subarray_product_less_than_k([1, 1, 1], 2) == 6
    assert num_subarray_product_less_than_k([1, 1, 1], 1) == 0
    assert num_subarray_product_less_than_k([], 10) == 0
    assert num_subarray_product_less_than_k([5], 6) == 1
    assert num_subarray_product_less_than_k([5], 5) == 0
    assert num_subarray_product_less_than_k([2] * 20, 1000) == 144
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
