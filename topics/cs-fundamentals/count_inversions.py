"""
Day 17, Task 9 -- CS fundamentals: count inversions with merge sort.

THE PROBLEM
------------
An inversion is a pair of indices i < j with a[i] > a[j]. Implement
count_inversions(a) in O(n log n) by counting during a merge sort, and
return (sorted_copy, inversions). The input list must not be mutated.
Equal elements are NOT inversions.

    count_inversions([2, 4, 1, 3, 5]) -> ([1, 2, 3, 4, 5], 3)
    count_inversions([5, 4, 3, 2, 1]) -> ([1, 2, 3, 4, 5], 10)
    count_inversions([])              -> ([], 0)

HOW TO WORK THROUGH THIS
-------------------------
While merging, whenever you take an element from the right half before
the remaining left elements, add len(left_remaining) to the count.

Run: python3 count_inversions.py
"""


def count_inversions(a: list):
    raise NotImplementedError


def _run_tests():
    import random
    assert count_inversions([2, 4, 1, 3, 5]) == ([1, 2, 3, 4, 5], 3)
    assert count_inversions([5, 4, 3, 2, 1]) == ([1, 2, 3, 4, 5], 10)
    assert count_inversions([]) == ([], 0)
    assert count_inversions([7]) == ([7], 0)
    assert count_inversions([2, 2, 2]) == ([2, 2, 2], 0)
    assert count_inversions([3, 1, 2, 1]) == ([1, 1, 2, 3], 4)
    orig = [3, 1, 2]
    count_inversions(orig)
    assert orig == [3, 1, 2], "input mutated"
    rng = random.Random(7)
    for _ in range(50):
        arr = [rng.randint(0, 20) for _ in range(rng.randint(0, 40))]
        brute = sum(1 for i in range(len(arr)) for j in range(i + 1, len(arr)) if arr[i] > arr[j])
        assert count_inversions(arr) == (sorted(arr), brute)
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
