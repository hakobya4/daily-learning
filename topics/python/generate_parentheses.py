"""
Day 24, Task 2 -- Python: generate all balanced parentheses.

THE PROBLEM
------------
generate_parentheses(n) returns every well-formed string made of n pairs
of parentheses, as a list sorted in ascending string order ('(' < ')').

  generate_parentheses(0) == [""]
  generate_parentheses(1) == ["()"]
  generate_parentheses(3) == ["((()))", "(()())", "(())()", "()(())", "()()()"]

Raise ValueError if n is negative.

HOW TO WORK THROUGH THIS
-------------------------
Backtracking: track how many '(' and ')' are used; you may add '(' while
opens < n, and ')' while closes < opens. Trying '(' before ')' yields
sorted order for free.

Run: python3 generate_parentheses.py
"""


def generate_parentheses(n: int) -> list:
    raise NotImplementedError


def _run_tests():
    assert generate_parentheses(0) == [""]
    assert generate_parentheses(1) == ["()"]
    assert generate_parentheses(2) == ["(())", "()()"]
    assert generate_parentheses(3) == ["((()))", "(()())", "(())()", "()(())", "()()()"]
    assert len(generate_parentheses(6)) == 132  # Catalan(6)
    assert generate_parentheses(5) == sorted(generate_parentheses(5))
    try:
        generate_parentheses(-1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
