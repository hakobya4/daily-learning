"""
Day 36, Task 2 -- Python: container with most water (two pointers).

THE PROBLEM
------------
heights[i] is the height of a vertical line at x = i. Choose two lines;
together with the x-axis they form a container whose area is
min(heights[i], heights[j]) * (j - i). Return the maximum area.
Fewer than 2 lines -> 0.

  [1,8,6,2,5,4,8,3,7] -> 49
  [1,1]               -> 1

HOW TO WORK THROUGH THIS
-------------------------
Start with pointers at both ends. Compute the area, then move the pointer
at the SHORTER line inward (moving the taller one can never help). O(n).

Run: python3 container_with_most_water.py
"""


def max_area(heights: list[int]) -> int:
    l, r = 0, len(heights) - 1
    best = 0
    while l < r:
        best = max(best, min(heights[l], heights[r]) * (r - l))
        if heights[l] < heights[r]:
            l += 1
        else:
            r -= 1
    return best


def _run_tests():
    assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert max_area([1, 1]) == 1
    assert max_area([]) == 0
    assert max_area([5]) == 0
    assert max_area([4, 3, 2, 1, 4]) == 16
    assert max_area([1, 2, 1]) == 2
    assert max_area([0, 0, 0]) == 0
    assert max_area(list(range(1, 11))) == 25
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
