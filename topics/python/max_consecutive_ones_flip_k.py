"""
Day 49, Task 2 -- Python: longest run of 1s after flipping at most k zeros.

THE PROBLEM
------------
Given a list of 0/1 ints and k >= 0, longest_ones(nums, k) returns the length of
the longest contiguous window that contains at most k zeros (i.e. all 1s after
flipping those zeros).
Examples: ([1,1,1,0,0,0,1,1,1,1,0], 2) -> 6, ([0,0,0], 0) -> 0, ([1,1], 0) -> 2.
Hint: variable-size sliding window; shrink from the left while zeros > k.

Run: python3 max_consecutive_ones_flip_k.py
"""


def longest_ones(nums, k):
    raise NotImplementedError


def _run_tests():
    assert longest_ones([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2) == 6
    assert longest_ones([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3) == 10
    assert longest_ones([0, 0, 0], 0) == 0
    assert longest_ones([1, 1], 0) == 2
    assert longest_ones([], 3) == 0
    assert longest_ones([0, 0, 0], 5) == 3
    assert longest_ones([1, 0, 1, 0, 1], 1) == 3
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
