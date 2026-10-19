"""
Day 29, Task 3 -- Python: intersection of two interval lists (two pointers).

THE PROBLEM
------------
a and b are each a list of closed intervals [start, end], sorted by start,
and pairwise disjoint WITHIN each list. interval_intersections(a, b)
returns every non-empty intersection, in sorted order. Touching at a single
point counts ([1,3] and [3,5] intersect in [3,3]).

  interval_intersections([[0,2],[5,10],[13,23],[24,25]],
                         [[1,5],[8,12],[15,24],[25,26]])
      -> [[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]
  interval_intersections([], [[1,2]]) -> []

HOW TO WORK THROUGH THIS
-------------------------
Two indices i, j. The overlap is [max(starts), min(ends)]; keep it if
lo <= hi. Then advance whichever interval ends FIRST. O(len(a) + len(b)).

Run: python3 interval_intersections.py
"""


def interval_intersections(a: list, b: list) -> list:
    raise NotImplementedError


def _run_tests():
    assert interval_intersections(
        [[0, 2], [5, 10], [13, 23], [24, 25]],
        [[1, 5], [8, 12], [15, 24], [25, 26]],
    ) == [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]
    assert interval_intersections([], [[1, 2]]) == []
    assert interval_intersections([[1, 2]], []) == []
    assert interval_intersections([[1, 3]], [[3, 5]]) == [[3, 3]]
    assert interval_intersections([[1, 3]], [[4, 5]]) == []
    assert interval_intersections([[1, 10]], [[2, 3], [5, 6]]) == [[2, 3], [5, 6]]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
