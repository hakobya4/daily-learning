"""
Day 34, Task 9 -- CS fundamentals: word search in a grid (DFS backtracking).

THE PROBLEM
------------
board is a grid of single-character strings. Return True if word can be
built by walking to horizontally or vertically adjacent cells, using each
cell at most once per path. The empty word is always found (True).

  board = [["A","B","C","E"],
           ["S","F","C","S"],
           ["A","D","E","E"]]
  "ABCCED" -> True      "SEE" -> True      "ABCB" -> False

HOW TO WORK THROUGH THIS
-------------------------
For each cell matching word[0], run dfs(r, c, k): if k == len(word) return
True; reject out-of-bounds, visited or mismatching cells; mark the cell
(e.g. temporarily set it to "#"), try the four neighbours, then restore it.

Run: python3 word_search.py
"""


def exist(board: list, word: str) -> bool:
    if not word:
        return True
    rows = len(board)
    cols = len(board[0]) if rows else 0

    def dfs(r, c, k):
        if k == len(word):
            return True
        if r < 0 or c < 0 or r >= rows or c >= cols or board[r][c] != word[k]:
            return False
        saved = board[r][c]
        board[r][c] = "#"
        found = (dfs(r + 1, c, k + 1) or dfs(r - 1, c, k + 1)
                 or dfs(r, c + 1, k + 1) or dfs(r, c - 1, k + 1))
        board[r][c] = saved
        return found

    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))


def _run_tests():
    b = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    assert exist(b, "ABCCED") is True
    assert exist(b, "SEE") is True
    assert exist(b, "ABCB") is False
    assert exist(b, "") is True
    assert exist([["A"]], "A") is True
    assert exist([["A"]], "AA") is False
    assert exist([["A", "A"]], "AAA") is False
    assert exist([["C", "A", "A"], ["A", "A", "A"], ["B", "C", "D"]], "AAB") is True
    assert b == [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
