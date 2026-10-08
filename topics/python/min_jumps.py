"""
Day 18, Task 3 -- Python: minimum jumps to reach the end.

THE PROBLEM
------------
nums[i] is the maximum jump length from index i. Starting at index 0,
return the minimum number of jumps needed to reach the last index, or -1
if it cannot be reached. A single-element list needs 0 jumps.

  [2, 3, 1, 1, 4] -> 2
  [1, 0, 1]       -> -1

Raise ValueError if nums is empty or not a list.

HOW TO WORK THROUGH THIS
-------------------------
Greedy "BFS by levels": track the current level's end and the farthest
reachable index; when you pass the level end, count a jump. If farthest
never grows past i, the end is unreachable.

Run: python3 min_jumps.py
"""


def min_jumps(nums: list) -> int:
    raise NotImplementedError


def _run_tests():
    assert min_jumps([2, 3, 1, 1, 4]) == 2
    assert min_jumps([2, 3, 0, 1, 4]) == 2
    assert min_jumps([0]) == 0
    assert min_jumps([1, 1, 1, 1]) == 3
    assert min_jumps([5, 1, 1, 1, 1]) == 1
    assert min_jumps([1, 0, 1]) == -1
    assert min_jumps([0, 1]) == -1
    for bad in ([], None, "12"):
        try:
            min_jumps(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for %r" % (bad,))
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
