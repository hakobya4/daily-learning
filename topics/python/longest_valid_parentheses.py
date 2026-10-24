"""
Day 33, Task 2 -- Python: longest valid parentheses substring.

THE PROBLEM
------------
Given a string s made only of '(' and ')', return the length of the
longest contiguous substring that is a valid (well-formed) parentheses
string.

  "(()"     -> 2     ("()")
  ")()())"  -> 4     ("()()")
  ""        -> 0
  "()(())"  -> 6

HOW TO WORK THROUGH THIS
-------------------------
Two classic routes: a stack of indices (start it with -1 as a base marker;
on ')' pop, and if the stack is empty push the current index as the new
base, else the length is i - stack[-1]), or a 1-D DP over positions.
Aim for O(n) time.

Run: python3 longest_valid_parentheses.py
"""


def longest_valid_parentheses(s: str) -> int:
    best = 0
    stack = [-1]
    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                best = max(best, i - stack[-1])
    return best


def _run_tests():
    assert longest_valid_parentheses("(()") == 2
    assert longest_valid_parentheses(")()())") == 4
    assert longest_valid_parentheses("") == 0
    assert longest_valid_parentheses("()(())") == 6
    assert longest_valid_parentheses("()(()") == 2
    assert longest_valid_parentheses("))((") == 0
    assert longest_valid_parentheses("(()())") == 6
    assert longest_valid_parentheses("()()") == 4
    assert longest_valid_parentheses("(" * 50 + ")" * 50) == 100
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
