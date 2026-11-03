"""
Day 44, Task 2 -- Python: k closest elements in a sorted array.

THE PROBLEM
------------
find_k_closest(arr, k, x): arr is sorted ascending. Return the k elements
closest to x as a sorted list. If two elements are equally close, the SMALLER
one wins. Target O(log(n-k) + k): binary search the left edge of the window
of size k (compare x - arr[mid] with arr[mid + k] - x).

Run: python3 find_k_closest.py
"""


def find_k_closest(arr, k, x):
    raise NotImplementedError


def _run_tests():
    assert find_k_closest([1, 2, 3, 4, 5], 4, 3) == [1, 2, 3, 4]
    assert find_k_closest([1, 2, 3, 4, 5], 4, -1) == [1, 2, 3, 4]
    assert find_k_closest([1, 1, 2, 3, 4, 5], 3, 3) == [2, 3, 4]
    assert find_k_closest([1, 3], 1, 2) == [1]
    assert find_k_closest([5], 1, 100) == [5]
    assert find_k_closest([1, 2, 3, 4, 5], 5, 3) == [1, 2, 3, 4, 5]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
