"""
Day 53, Task 7 -- CS fundamentals: k-th smallest pair distance (binary search on the answer).

THE PROBLEM
------------
smallest_distance_pair(nums, k): the distance of a pair (i, j) with i < j is |nums[i] - nums[j]|.
Return the k-th smallest distance among all n*(n-1)/2 pairs (k is 1-based and valid).
Examples: ([1, 3, 1], 1) -> 0, ([1, 6, 1], 3) -> 5, ([1, 2, 3, 4], 3) -> 1.
Generating all pairs is O(n^2 log n) -- do better.
Hint: sort nums; binary search the answer d in [0, max - min]. count(d) = number of pairs with
distance <= d, computable in O(n) with a sliding two-pointer window. Find the smallest d
with count(d) >= k. Total O(n log n + n log W).

Run: python3 kth_smallest_pair_distance.py
"""


def smallest_distance_pair(nums, k):
    raise NotImplementedError


def _run_tests():
    assert smallest_distance_pair([1, 3, 1], 1) == 0
    assert smallest_distance_pair([1, 1, 1], 2) == 0
    assert smallest_distance_pair([1, 6, 1], 3) == 5
    assert smallest_distance_pair([62, 100, 4], 2) == 58
    assert smallest_distance_pair([1, 2, 3, 4], 3) == 1
    assert smallest_distance_pair([1, 2, 3, 4], 4) == 2
    assert smallest_distance_pair([1, 2, 3, 4], 6) == 3
    assert smallest_distance_pair([9, 2], 1) == 7
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
