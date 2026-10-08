"""
Day 18, Task 9 -- CS fundamentals: word ladder (BFS on an implicit graph).

THE PROBLEM
------------
Given begin, end and a list of allowed words (all same length), return the
number of words in the shortest transformation sequence from begin to end,
changing one letter at a time, where every intermediate word (and end)
must be in the list. begin need not be in the list. Return 0 if no
sequence exists.

  ("hit", "cog", ["hot","dot","dog","lot","log","cog"]) -> 5
  ("hit", "cog", ["hot","dot","dog","lot","log"])       -> 0

If begin == end return 1.

HOW TO WORK THROUGH THIS
-------------------------
BFS with a queue of (word, length). To find neighbours, replace each
position with a wildcard ("h*t") and bucket words by pattern, or try all
26 letters per position against a set.

Run: python3 word_ladder.py
"""


def ladder_length(begin: str, end: str, words: list) -> int:
    raise NotImplementedError


def _run_tests():
    w = ["hot", "dot", "dog", "lot", "log", "cog"]
    assert ladder_length("hit", "cog", w) == 5
    assert ladder_length("hit", "cog", w[:-1]) == 0
    assert ladder_length("a", "c", ["a", "b", "c"]) == 2
    assert ladder_length("hot", "hot", w) == 1
    assert ladder_length("hit", "hot", ["hot"]) == 2
    assert ladder_length("abc", "xyz", []) == 0
    big = ["a%03d" % i for i in range(1000)]
    assert ladder_length("a000", "a999", big) == 4
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
