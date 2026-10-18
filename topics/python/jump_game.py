"""
Day 27, Task 4 -- Python: jump game.

THE PROBLEM
------------
can_reach_end(nums) -- you start at index 0 and nums[i] is the MAXIMUM
jump length from index i. Return True if you can reach the last index.

  can_reach_end([2, 3, 1, 1, 4]) -> True
  can_reach_end([3, 2, 1, 0, 4]) -> False   (always stuck at index 3)

HOW TO WORK THROUGH THIS
-------------------------
Greedy: track the farthest index reachable so far. If the current index
is beyond it, you are stuck. O(n), O(1) space.

Run: python3 jump_game.py
"""


def can_reach_end(nums: list) -> bool:
    farthest = 0
    for i, jump in enumerate(nums):
        if i > farthest:
            return False
        farthest = max(farthest, i + jump)
        if farthest >= len(nums) - 1:
            return True
    return True


def _run_tests():
    assert can_reach_end([2, 3, 1, 1, 4]) is True
    assert can_reach_end([3, 2, 1, 0, 4]) is False
    assert can_reach_end([0]) is True
    assert can_reach_end([0, 1]) is False
    assert can_reach_end([1, 0, 0]) is False
    assert can_reach_end([5, 0, 0, 0, 0]) is True
    assert can_reach_end([2, 0, 0]) is True
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
