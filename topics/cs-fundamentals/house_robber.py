"""
Day 38, Task 9 -- CS fundamentals: house robber (1-D DP) incl. circular street.

THE PROBLEM
------------
nums[i] is the money in house i. You cannot rob two ADJACENT houses.
Implement:
  rob_line(nums)   -> max money on a straight street
  rob_circle(nums) -> max money when the street is a circle
                      (first and last houses are adjacent)

  rob_line([2, 7, 9, 3, 1]) -> 12
  rob_circle([2, 3, 2])     -> 3
  rob_circle([1, 2, 3, 1])  -> 4

HOW TO WORK THROUGH THIS
-------------------------
Line: keep (take, skip) or a rolling pair: best[i] = max(best[i-1], best[i-2] + nums[i]).
Circle: either house 0 or the last house is excluded, so answer =
max(rob_line(nums[1:]), rob_line(nums[:-1])); handle len 0 and 1 specially.

Run: python3 house_robber.py
"""


def rob_line(nums: list) -> int:
    prev, cur = 0, 0
    for x in nums:
        prev, cur = cur, max(cur, prev + x)
    return cur


def rob_circle(nums: list) -> int:
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    return max(rob_line(nums[1:]), rob_line(nums[:-1]))


def _run_tests():
    assert rob_line([2, 7, 9, 3, 1]) == 12
    assert rob_line([1, 2, 3, 1]) == 4
    assert rob_line([]) == 0
    assert rob_line([5]) == 5
    assert rob_line([2, 1, 1, 2]) == 4
    assert rob_circle([2, 3, 2]) == 3
    assert rob_circle([1, 2, 3, 1]) == 4
    assert rob_circle([]) == 0
    assert rob_circle([7]) == 7
    assert rob_circle([1, 2]) == 2
    assert rob_circle([200, 3, 140, 20, 10]) == 340
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
