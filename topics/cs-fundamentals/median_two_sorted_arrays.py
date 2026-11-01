"""
Day 42, Task 9 -- CS fundamentals: median of two sorted arrays.

THE PROBLEM
------------
find_median(a, b) -> median of the union of two sorted lists of numbers
(not both empty). For an even total count, return the mean of the two middle
values as a float. Required: O(log(min(len(a), len(b)))) time via binary search
on the partition of the shorter array (not merging, not sorting).

Run: python3 median_two_sorted_arrays.py
"""


def find_median(a, b):
    raise NotImplementedError


def _run_tests():
    import random
    assert find_median([1, 3], [2]) == 2
    assert find_median([1, 2], [3, 4]) == 2.5
    assert find_median([], [5]) == 5
    assert find_median([2], []) == 2
    assert find_median([0, 0], [0, 0]) == 0
    assert find_median([1, 2, 3], [10, 11, 12, 13]) == 10
    assert find_median([-5, -3], [-4]) == -4
    random.seed(7)
    for _ in range(300):
        a = sorted(random.randint(-20, 20) for _ in range(random.randint(0, 8)))
        b = sorted(random.randint(-20, 20) for _ in range(random.randint(0, 8)))
        if not a and not b:
            continue
        m = sorted(a + b)
        n = len(m)
        exp = m[n // 2] if n % 2 else (m[n // 2 - 1] + m[n // 2]) / 2
        assert find_median(a, b) == exp, (a, b)
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
