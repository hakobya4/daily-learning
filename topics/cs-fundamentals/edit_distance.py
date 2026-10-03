"""
Day 12, Task 7 -- CS fundamentals: edit (Levenshtein) distance.

THE PROBLEM
------------
edit_distance(a, b) returns the minimum number of single-character
insertions, deletions and substitutions needed to turn string a into b.

Also implement edit_script(a, b) -> list of operations that transforms
a into b using exactly edit_distance(a, b) steps. Each op is a tuple:
  ("keep", ch) | ("sub", old, new) | ("del", ch) | ("ins", ch)
Applying the ops left to right must rebuild b from a (keep/sub/ins emit
characters of b; keep/sub/del consume characters of a). The number of
non-"keep" ops must equal the distance.

HOW TO WORK THROUGH THIS
-------------------------
Fill a (len(a)+1) x (len(b)+1) table: dp[i][j] = distance between
a[:i] and b[:j]. Base rows are i and j. Backtrack from dp[n][m] to
recover the script, then reverse it.

Run: python3 edit_distance.py
"""


def _table(a, b):
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
    return dp


def edit_distance(a, b):
    return _table(a, b)[len(a)][len(b)]


def edit_script(a, b):
    dp = _table(a, b)
    i, j = len(a), len(b)
    ops = []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i - 1] == b[j - 1] and dp[i][j] == dp[i - 1][j - 1]:
            ops.append(("keep", a[i - 1]))
            i, j = i - 1, j - 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            ops.append(("sub", a[i - 1], b[j - 1]))
            i, j = i - 1, j - 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            ops.append(("del", a[i - 1]))
            i -= 1
        else:
            ops.append(("ins", b[j - 1]))
            j -= 1
    ops.reverse()
    return ops


def _apply(a, ops):
    out, i = [], 0
    for op in ops:
        if op[0] == "keep":
            assert a[i] == op[1]
            out.append(op[1]); i += 1
        elif op[0] == "sub":
            assert a[i] == op[1]
            out.append(op[2]); i += 1
        elif op[0] == "del":
            assert a[i] == op[1]
            i += 1
        else:
            out.append(op[1])
    assert i == len(a)
    return "".join(out)


def _run_tests() -> None:
    assert edit_distance("", "") == 0
    assert edit_distance("abc", "abc") == 0
    assert edit_distance("", "abc") == 3
    assert edit_distance("abc", "") == 3
    assert edit_distance("kitten", "sitting") == 3
    assert edit_distance("flaw", "lawn") == 2
    assert edit_distance("intention", "execution") == 5
    assert edit_distance("a", "b") == 1
    for a, b in [("kitten", "sitting"), ("flaw", "lawn"), ("", "xyz"),
                 ("abc", ""), ("same", "same"), ("intention", "execution")]:
        ops = edit_script(a, b)
        assert _apply(a, ops) == b
        assert sum(1 for o in ops if o[0] != "keep") == edit_distance(a, b)
    print("All edit_distance tests passed.")


if __name__ == "__main__":
    _run_tests()
