"""
Day 47, Task 3 -- Python: score of balanced parentheses.

THE PROBLEM
------------
Given a balanced parentheses string s:
  "()"  scores 1
  "AB"  scores score(A) + score(B)      (concatenation)
  "(A)" scores 2 * score(A)             (nesting)
score(s) returns the total. Examples: "()" -> 1, "(())" -> 2, "()()" -> 2,
"(()(()))" -> 6. The empty string scores 0.
Hint: a stack of partial scores, or track depth and add 2**depth at every "()".

Run: python3 score_of_parentheses.py
"""


def score(s):
    raise NotImplementedError


def _run_tests():
    assert score("") == 0
    assert score("()") == 1
    assert score("(())") == 2
    assert score("()()") == 2
    assert score("(()(()))") == 6
    assert score("((()))") == 4
    assert score("(()())") == 4
    assert score("()(())") == 3
    assert score("(" * 20 + ")" * 20) == 2 ** 19
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
