"""
Day 22, Task 3 -- Python: row n of Pascal's triangle in O(n) memory.

THE PROBLEM
------------
Return row n (0-indexed) of Pascal's triangle as a list of ints.

  pascal_row(0) == [1]
  pascal_row(1) == [1, 1]
  pascal_row(4) == [1, 4, 6, 4, 1]

Use only O(n) extra memory (do not build the whole triangle), and it must
stay exact for big n (Python ints are arbitrary precision).
Raise ValueError if n < 0.

HOW TO WORK THROUGH THIS
-------------------------
Either update one list in place from right to left, or use
C(n, k+1) = C(n, k) * (n - k) // (k + 1) to walk along the row.

Run: python3 pascal_row.py
"""


def pascal_row(n: int) -> list:
    raise NotImplementedError


def _run_tests():
    assert pascal_row(0) == [1]
    assert pascal_row(1) == [1, 1]
    assert pascal_row(2) == [1, 2, 1]
    assert pascal_row(4) == [1, 4, 6, 4, 1]
    assert pascal_row(6) == [1, 6, 15, 20, 15, 6, 1]
    row = pascal_row(60)
    assert len(row) == 61
    assert row[30] == 118264581564861424
    assert sum(row) == 2 ** 60
    assert row == row[::-1]
    try:
        pascal_row(-1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
