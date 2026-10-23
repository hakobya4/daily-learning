"""
Day 32, Task 9 -- CS fundamentals: maximal square (2-D dynamic programming).

THE PROBLEM
------------
matrix is a list of strings of "0"/"1" characters (all rows the same
length). maximal_square(matrix) returns the AREA of the largest square made
only of "1"s. An empty matrix gives 0.

  ["10100",
   "10111",
   "11111",
   "10010"]  -> 4    (a 2x2 square)
  ["01","10"] -> 1
  ["0"]       -> 0

HOW TO WORK THROUGH THIS
-------------------------
dp[i][j] = side of the largest all-ones square whose BOTTOM-RIGHT corner is
(i, j). If cell is "1": dp = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]),
else 0. Answer is (max dp)^2. Try reducing memory to one row afterwards.

Run: python3 maximal_square.py
"""


def maximal_square(matrix: list) -> int:
    if not matrix:
        return 0
    cols = len(matrix[0])
    prev = [0] * (cols + 1)
    side = 0
    for row in matrix:
        cur = [0] * (cols + 1)
        for j in range(1, cols + 1):
            if row[j - 1] == "1":
                cur[j] = 1 + min(prev[j], cur[j - 1], prev[j - 1])
                side = max(side, cur[j])
        prev = cur
    return side * side


def _run_tests():
    assert maximal_square(["10100", "10111", "11111", "10010"]) == 4
    assert maximal_square(["01", "10"]) == 1
    assert maximal_square(["0"]) == 0
    assert maximal_square(["1"]) == 1
    assert maximal_square([]) == 0
    assert maximal_square(["111", "111", "111"]) == 9
    assert maximal_square(["1111", "1111", "0111", "0111"]) == 9
    assert maximal_square(["1110", "1110"]) == 4
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
