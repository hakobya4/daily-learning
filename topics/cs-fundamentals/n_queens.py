"""
Day 16, Task 9 -- CS fundamentals: N-Queens by backtracking.

THE PROBLEM
------------
Place n queens on an n x n board so none attack each other.

    count_n_queens(n)  -> number of distinct solutions
    solve_n_queens(n)  -> list of solutions; each solution is a list of
                          n strings of '.' and 'Q', row by row.
                          Solutions are ordered by the column of the
                          queen in row 0, then row 1, ... (lexicographic
                          by column tuple).

    count_n_queens(4) -> 2        count_n_queens(8) -> 92
    solve_n_queens(4) -> [[".Q..","...Q","Q...","..Q."],
                          ["..Q.","Q...","...Q",".Q.."]]
    solve_n_queens(1) -> [["Q"]]  solve_n_queens(2) -> []

HOW TO WORK THROUGH THIS
-------------------------
Place one queen per row; track used columns and both diagonals
(r - c and r + c) in sets so each check is O(1).

Run: python3 n_queens.py
"""


def _placements(n: int):
    cols, d1, d2 = set(), set(), set()
    placement = []

    def bt(r):
        if r == n:
            yield tuple(placement)
            return
        for c in range(n):
            if c in cols or (r - c) in d1 or (r + c) in d2:
                continue
            cols.add(c)
            d1.add(r - c)
            d2.add(r + c)
            placement.append(c)
            yield from bt(r + 1)
            placement.pop()
            cols.remove(c)
            d1.remove(r - c)
            d2.remove(r + c)

    yield from bt(0)


def count_n_queens(n: int) -> int:
    return sum(1 for _ in _placements(n))


def solve_n_queens(n: int) -> list[list[str]]:
    return [
        ["." * c + "Q" + "." * (n - c - 1) for c in p]
        for p in _placements(n)
    ]


def _run_tests():
    assert [count_n_queens(n) for n in range(1, 9)] == [1, 0, 0, 2, 10, 4, 40, 92]
    assert solve_n_queens(1) == [["Q"]]
    assert solve_n_queens(2) == []
    assert solve_n_queens(4) == [
        [".Q..", "...Q", "Q...", "..Q."],
        ["..Q.", "Q...", "...Q", ".Q.."],
    ]
    sols = solve_n_queens(6)
    assert len(sols) == 4 and all(len(b) == 6 for b in sols)
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
