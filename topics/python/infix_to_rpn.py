"""
Day 14, Task 3 -- Python: shunting-yard (infix -> RPN) and evaluation.

THE PROBLEM
------------
Support non-negative integers, the binary operators + - * / ^, and
parentheses. Whitespace is optional ("3+4*2" and "3 + 4 * 2" are equal).
No unary minus.

Precedence: ^ (highest, RIGHT associative), then * and /, then + and -
(all left associative).

    to_rpn("3 + 4 * 2")      -> ["3", "4", "2", "*", "+"]
    to_rpn("2^3^2")          -> ["2", "3", "2", "^", "^"]
    evaluate("(1+2)*3")      -> 9
    evaluate("10/4")         -> 2.5      (true division)

Raise ValueError for mismatched parentheses, unknown characters, or a
malformed expression (e.g. "3 +", "3 4", "()").

HOW TO WORK THROUGH THIS
-------------------------
tokenize -> shunting-yard with an operator stack -> evaluate the RPN
list with a value stack. (rpn_eval.py from an earlier day is the same
evaluator, if you want to reuse the idea.)

Run: python3 infix_to_rpn.py
"""


def tokenize(expr: str) -> list[str]:
    # TODO: split into number / operator / paren tokens.
    raise NotImplementedError


def to_rpn(expr: str) -> list[str]:
    # TODO: shunting-yard.
    raise NotImplementedError


def evaluate(expr: str) -> float:
    # TODO: to_rpn + stack evaluation.
    raise NotImplementedError


def _run_tests() -> None:
    assert tokenize("12+(3*4)") == ["12", "+", "(", "3", "*", "4", ")"]
    assert to_rpn("3 + 4 * 2") == ["3", "4", "2", "*", "+"]
    assert to_rpn("3+4*2") == ["3", "4", "2", "*", "+"]
    assert to_rpn("2^3^2") == ["2", "3", "2", "^", "^"]
    assert to_rpn("8-3-2") == ["8", "3", "-", "2", "-"]
    assert to_rpn("(1+2)*3") == ["1", "2", "+", "3", "*"]
    assert evaluate("(1+2)*3") == 9
    assert evaluate("10/4") == 2.5
    assert evaluate("2^3^2") == 512
    assert evaluate("8-3-2") == 3
    assert evaluate("2*(3+4)*5") == 70
    assert evaluate("7") == 7
    for bad in ["(1+2", "1+2)", "3 +", "3 4", "()", "", "2 $ 3"]:
        try:
            evaluate(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad!r}")
    print("All infix_to_rpn tests passed.")


if __name__ == "__main__":
    _run_tests()
