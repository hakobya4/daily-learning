"""
Day 33, Task 3 -- Python: increasing triplet subsequence.

THE PROBLEM
------------
Given a list of integers nums, return True if there exist indices
i < j < k with nums[i] < nums[j] < nums[k], otherwise False. The elements
need not be adjacent. Do it in O(n) time and O(1) extra space.

  [1, 2, 3, 4, 5]        -> True
  [5, 4, 3, 2, 1]        -> False
  [2, 1, 5, 0, 4, 6]     -> True    (2, 4, 6)
  [1, 1, 1]              -> False   (strictly increasing)

HOW TO WORK THROUGH THIS
-------------------------
Keep two values: the smallest number seen so far (first) and the smallest
possible "middle" of a pair that ends an increasing pair (second). If you
ever see a number bigger than both, you have a triplet.

Run: python3 increasing_triplet.py
"""


def increasing_triplet(nums: list) -> bool:
    first = second = float("inf")
    for n in nums:
        if n <= first:
            first = n
        elif n <= second:
            second = n
        else:
            return True
    return False


def _run_tests():
    assert increasing_triplet([1, 2, 3, 4, 5]) is True
    assert increasing_triplet([5, 4, 3, 2, 1]) is False
    assert increasing_triplet([2, 1, 5, 0, 4, 6]) is True
    assert increasing_triplet([1, 1, 1]) is False
    assert increasing_triplet([20, 100, 10, 12, 5, 13]) is True
    assert increasing_triplet([]) is False
    assert increasing_triplet([1, 2]) is False
    assert increasing_triplet([6, 7, 1, 2]) is False
    assert increasing_triplet([1, 5, 0, 4, 1, 3]) is True
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
