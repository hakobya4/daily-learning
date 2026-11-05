"""
Day 45, Task 9 -- CS fundamentals: trapping rain water (two pointers).

THE PROBLEM
------------
height[i] is the height of a bar of width 1. After raining, how many units
of water are trapped between the bars? Solve in O(n) time, O(1) extra space.
Hint: two pointers l, r with running left_max/right_max; always advance the
side with the smaller max.

Run: python3 trapping_rain_water.py
"""


def trap(height):
    l, r = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    while l < r:
        if height[l] < height[r]:
            left_max = max(left_max, height[l])
            water += left_max - height[l]
            l += 1
        else:
            right_max = max(right_max, height[r])
            water += right_max - height[r]
            r -= 1
    return water


def _run_tests():
    assert trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert trap([4, 2, 0, 3, 2, 5]) == 9
    assert trap([]) == 0
    assert trap([3]) == 0
    assert trap([1, 2, 3, 4]) == 0
    assert trap([3, 0, 3]) == 3
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
