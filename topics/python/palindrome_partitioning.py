"""
Day 34, Task 2 -- Python: palindrome partitioning.

THE PROBLEM
------------
Given a string s, return every way to split it into substrings that are
all palindromes. Each way is a list of the pieces in order. Return the
partitions in the order a backtracking search finds them when it tries
SHORTER prefixes first.

  "aab" -> [["a", "a", "b"], ["aa", "b"]]
  "aba" -> [["a", "b", "a"], ["aba"]]
  "a"   -> [["a"]]
  ""    -> [[]]       (one way: no pieces)

HOW TO WORK THROUGH THIS
-------------------------
Backtrack: at position i, try every end j > i; if s[i:j] is a palindrome,
add it to the current path and recurse from j. When i reaches len(s),
record a copy of the path.

Run: python3 palindrome_partitioning.py
"""


def partition(s: str) -> list:
    res = []
    path = []

    def bt(i):
        if i == len(s):
            res.append(path[:])
            return
        for j in range(i + 1, len(s) + 1):
            piece = s[i:j]
            if piece == piece[::-1]:
                path.append(piece)
                bt(j)
                path.pop()

    bt(0)
    return res


def _run_tests():
    assert partition("aab") == [["a", "a", "b"], ["aa", "b"]]
    assert partition("aba") == [["a", "b", "a"], ["aba"]]
    assert partition("a") == [["a"]]
    assert partition("") == [[]]
    assert partition("ab") == [["a", "b"]]
    assert partition("aaa") == [["a", "a", "a"], ["a", "aa"], ["aa", "a"], ["aaa"]]
    assert len(partition("abacaba")) == 7
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
