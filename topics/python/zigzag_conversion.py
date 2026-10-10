"""
Day 20, Task 2 -- Python: zigzag conversion.

THE PROBLEM
------------
Write s in a zigzag over num_rows rows, going down then diagonally up,
then read it row by row.

  s = "PAYPALISHIRING", num_rows = 3
      P   A   H   N
      A P L S I I G
      Y   I   R
  -> "PAHNAPLSIIGYIR"

  num_rows = 4 -> "PINALSIGYAHRPI"
  num_rows = 1 -> s unchanged (also when num_rows >= len(s))

Raise ValueError if num_rows < 1.

HOW TO WORK THROUGH THIS
-------------------------
Keep one list of characters per row and a direction that flips at the top
and bottom row. Careful with num_rows == 1 (direction never flips).

Run: python3 zigzag_conversion.py
"""


def convert(s: str, num_rows: int) -> str:
    raise NotImplementedError


def _run_tests():
    assert convert("PAYPALISHIRING", 3) == "PAHNAPLSIIGYIR"
    assert convert("PAYPALISHIRING", 4) == "PINALSIGYAHRPI"
    assert convert("ABC", 1) == "ABC"
    assert convert("AB", 5) == "AB"
    assert convert("", 3) == ""
    assert convert("ABCDE", 2) == "ACEBD"
    try:
        convert("ABC", 0)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
