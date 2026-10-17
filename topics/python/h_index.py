"""
Day 27, Task 3 -- Python: h-index.

THE PROBLEM
------------
h_index(citations) takes the citation count of each of a researcher's
papers and returns their h-index: the largest h such that at least h
papers have at least h citations each.

  h_index([3, 0, 6, 1, 5]) -> 3
  h_index([1, 3, 1])       -> 1
  h_index([])              -> 0

HOW TO WORK THROUGH THIS
-------------------------
Sort descending; the answer is the number of positions i (0-based) where
citations[i] >= i + 1. (An O(n) counting-bucket version also exists.)

Run: python3 h_index.py
"""


def h_index(citations: list) -> int:
    raise NotImplementedError


def _run_tests():
    assert h_index([3, 0, 6, 1, 5]) == 3
    assert h_index([1, 3, 1]) == 1
    assert h_index([]) == 0
    assert h_index([0, 0, 0]) == 0
    assert h_index([100]) == 1
    assert h_index([4, 4, 4, 4]) == 4
    assert h_index([10, 8, 5, 4, 3]) == 4
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
