"""
Day 41, Task 10 -- CS fundamentals: next greater element (monotonic stack).

THE PROBLEM
------------
next_greater(nums) returns out where out[i] is the first element to the RIGHT
of i that is strictly greater than nums[i], or -1 if none. O(n) using a stack
of indices that are still waiting for their answer.

  [2,1,2,4,3] -> [4,2,4,-1,-1]

Also implement days_until_warmer(temps): out[i] = how many days until a
strictly warmer temperature, or 0 if never.

  [73,74,75,71,69,72,76,73] -> [1,1,4,2,1,1,0,0]

Run: python3 next_greater_element.py
"""


def next_greater(nums: list) -> list:
    raise NotImplementedError


def days_until_warmer(temps: list) -> list:
    raise NotImplementedError


def _run_tests():
    assert next_greater([]) == []
    assert next_greater([2, 1, 2, 4, 3]) == [4, 2, 4, -1, -1]
    assert next_greater([5, 4, 3]) == [-1, -1, -1]
    assert next_greater([1, 2, 3]) == [2, 3, -1]
    assert next_greater([3, 3, 3]) == [-1, -1, -1]
    assert days_until_warmer([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
    assert days_until_warmer([30, 40, 50, 60]) == [1, 1, 1, 0]
    assert days_until_warmer([]) == []
    assert days_until_warmer(list(range(1000, 0, -1))) == [0] * 1000
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
