"""
Day 16, Task 3 -- Python: basic calculator.

THE PROBLEM
------------
Evaluate an arithmetic expression string containing non-negative
integers, + - * /, parentheses and spaces. Division truncates toward
zero. Unary minus may appear at the start or right after '('.
Do NOT use eval().

    calc("1 + 2 * 3")        -> 7
    calc("(1 + 2) * 3")      -> 9
    calc("10 / 3")           -> 3
    calc("-7 / 2")           -> -3
    calc("2 * (3 + (4 - 1))")-> 12
    calc("-(2 + 3)")         -> -5

Raise ZeroDivisionError on division by zero.

HOW TO WORK THROUGH THIS
-------------------------
Either a recursive-descent parser (expr -> term -> factor) or two stacks
(shunting-yard). Careful: int(a / b) truncates toward zero, // does not.

Run: python3 basic_calculator.py
"""


def calc(expr: str) -> int:
    raise NotImplementedError


def _run_tests():
    assert calc("1 + 2 * 3") == 7
    assert calc("(1 + 2) * 3") == 9
    assert calc("10 / 3") == 3
    assert calc("-7 / 2") == -3
    assert calc("2 * (3 + (4 - 1))") == 12
    assert calc("-(2 + 3)") == -5
    assert calc("  42 ") == 42
    assert calc("8 - 3 - 2") == 3
    assert calc("100 / 10 / 5") == 2
    assert calc("2 * 3 * 4 - 5") == 19
    assert calc("(-3) * (-3)") == 9
    try:
        calc("1 / (2 - 2)")
    except ZeroDivisionError:
        pass
    else:
        raise AssertionError("expected ZeroDivisionError")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
