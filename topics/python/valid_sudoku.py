"""
Day 17, Task 2 -- Python: validate a Sudoku board.

THE PROBLEM
------------
A board is a list of 9 strings of length 9; each char is '1'-'9' or '.'
(empty). Return True if the filled cells break no rule: no repeated digit
in any row, any column, or any of the nine 3x3 boxes. The board need not
be solvable -- only check what is filled in.

Raise ValueError if the board is not 9x9 or contains a char outside
'1'-'9' and '.'.

HOW TO WORK THROUGH THIS
-------------------------
Keep sets for rows, columns and boxes; box index = (r // 3) * 3 + c // 3.

Run: python3 valid_sudoku.py
"""


def is_valid_sudoku(board: list) -> bool:
    raise NotImplementedError


def _run_tests():
    good = [
        "53..7....", "6..195...", ".98....6.",
        "8...6...3", "4..8.3..1", "7...2...6",
        ".6....28.", "...419..5", "....8..79",
    ]
    assert is_valid_sudoku(good) is True
    assert is_valid_sudoku(["........."] * 9) is True
    row_dup = list(good); row_dup[0] = "53..7...3"
    assert is_valid_sudoku(row_dup) is False
    col_dup = list(good); col_dup[4] = "4..8.3..1"; col_dup[7] = "5..419..5"
    assert is_valid_sudoku(col_dup) is False
    box_dup = list(good); box_dup[1] = "6..195..."; box_dup[2] = "598....6."
    assert is_valid_sudoku(box_dup) is False
    for bad in (good[:8], ["x" * 9] * 9, ["12345678"] * 9):
        try:
            is_valid_sudoku(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for %r" % (bad[:1],))
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
