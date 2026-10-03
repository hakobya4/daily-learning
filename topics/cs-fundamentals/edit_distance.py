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


def edit_distance(a, b):
    raise NotImplementedError


def edit_script(a, b):
    raise NotImplementedError


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
