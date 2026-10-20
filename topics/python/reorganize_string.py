"""
Day 30, Task 3 -- Python: reorganize a string so no two neighbours match.

THE PROBLEM
------------
reorganize(s) returns ANY rearrangement of the characters of s in which no
two adjacent characters are equal, or "" if that is impossible.

  "aab"  -> "aba"
  "aaab" -> ""
  "abc"  -> any permutation with no equal neighbours

HOW TO WORK THROUGH THIS
-------------------------
Impossible exactly when the most frequent char occurs more than
(len(s)+1)//2 times. Greedy: a max-heap of (count, char) -- repeatedly take
the most frequent char that is not the one just placed (heapq with negated
counts; hold the previous char back one round).

Run: python3 reorganize_string.py
"""
import heapq  # noqa: F401  (hint: you will want it)
from collections import Counter  # noqa: F401


def reorganize(s: str) -> str:
    raise NotImplementedError


def _valid(original, result):
    return (
        sorted(result) == sorted(original)
        and all(a != b for a, b in zip(result, result[1:]))
    )


def _run_tests():
    assert _valid("aab", reorganize("aab"))
    assert reorganize("aaab") == ""
    assert _valid("abc", reorganize("abc"))
    assert reorganize("") == ""
    assert reorganize("a") == "a"
    assert reorganize("aa") == ""
    assert _valid("aabbcc", reorganize("aabbcc"))
    assert _valid("aaabbbc", reorganize("aaabbbc"))
    assert reorganize("aaaabbc") == ""
    assert _valid("vvvlo", reorganize("vvvlo"))  # v?v?v is possible
    assert reorganize("vvvvlo") == ""
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
