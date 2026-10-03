"""
Day 12, Task 3 -- Python: reverse Polish notation evaluator.

THE PROBLEM
------------
Implement eval_rpn(tokens) where tokens is a list of strings such as
["2", "3", "+", "4", "*"]  ->  (2 + 3) * 4 = 20.

Supported operators: + - * /. Operands are integers or decimals (may be
negative, e.g. "-3" or "2.5"). Division is true division (float).
Return a number (int when every step was integer-valued and no "/" was
used is fine; tests compare with ==).

Raise ValueError for: an unknown token, an operator with fewer than two
operands on the stack, leftover operands at the end (more than one value
remains), or an empty list. Division by zero raises ZeroDivisionError
(let it propagate).

HOW TO WORK THROUGH THIS
-------------------------
Use a list as a stack. For a binary operator pop b first, then a, and
push a OP b. Try float(tok) to recognise numbers.

Run: python3 rpn_eval.py
"""


def eval_rpn(tokens):
    raise NotImplementedError


def _run_tests() -> None:
    assert eval_rpn(["2", "3", "+", "4", "*"]) == 20
    assert eval_rpn(["5"]) == 5
    assert eval_rpn(["10", "4", "-"]) == 6          # order matters
    assert eval_rpn(["9", "3", "/"]) == 3
    assert eval_rpn(["7", "2", "/"]) == 3.5
    assert eval_rpn(["-3", "2", "*"]) == -6
    assert eval_rpn(["2.5", "2", "*"]) == 5.0
    assert eval_rpn(["5", "1", "2", "+", "4", "*", "+", "3", "-"]) == 14
    for bad in ([], ["+"], ["1", "+"], ["1", "2"], ["1", "x", "+"]):
        try:
            eval_rpn(bad)
            assert False, f"should reject {bad!r}"
        except ValueError:
            pass
    try:
        eval_rpn(["1", "0", "/"])
        assert False
    except ZeroDivisionError:
        pass
    print("All rpn_eval tests passed.")


if __name__ == "__main__":
    _run_tests()
