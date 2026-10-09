"""
Day 19, Task 2 -- Python: trapping rain water.

THE PROBLEM
------------
heights[i] is the height of a bar of width 1. After raining, how many
units of water are trapped between the bars?

  [0,1,0,2,1,0,1,3,2,1,2,1] -> 6
  [4,2,0,3,2,5]             -> 9

Raise ValueError if heights is not a list.

HOW TO WORK THROUGH THIS
-------------------------
Water above bar i = min(max height to its left, max height to its right)
- heights[i]. Try prefix/suffix max arrays first (O(n) space), then the
two-pointer version (O(1) space).

Run: python3 trapping_rain_water.py
"""


def trap(heights: list) -> int:
    raise NotImplementedError


def _run_tests():
    assert trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert trap([4, 2, 0, 3, 2, 5]) == 9
    assert trap([3, 0, 3]) == 3
    assert trap([]) == 0
    assert trap([3]) == 0
    assert trap([1, 2, 3]) == 0
    assert trap([3, 2, 1]) == 0
    try:
        trap("abc")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
