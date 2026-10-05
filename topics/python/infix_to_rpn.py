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
    tokens = []
    i = 0
    while i < len(expr):
        ch = expr[i]
        if ch.isspace():
            i += 1
        elif ch.isdigit():
            j = i
            while j < len(expr) and expr[j].isdigit():
                j += 1
            tokens.append(expr[i:j])
            i = j
        elif ch in "+-*/^()":
            tokens.append(ch)
            i += 1
        else:
            raise ValueError(f"unknown character {ch!r}")
    return tokens


def to_rpn(expr: str) -> list[str]:
    prec = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
    out: list[str] = []
    stack: list[str] = []
    expect_operand = True  # validates alternation of operands/operators
    tokens = tokenize(expr)
    if not tokens:
        raise ValueError("empty expression")
    for tok in tokens:
        if tok.isdigit():
            if not expect_operand:
                raise ValueError("unexpected number")
            out.append(tok)
            expect_operand = False
        elif tok == "(":
            if not expect_operand:
                raise ValueError("unexpected '('")
            stack.append(tok)
        elif tok == ")":
            if expect_operand:
                raise ValueError("unexpected ')'")
            while stack and stack[-1] != "(":
                out.append(stack.pop())
            if not stack:
                raise ValueError("mismatched parentheses")
            stack.pop()
        else:
            if expect_operand:
                raise ValueError("unexpected operator")
            while (stack and stack[-1] != "(" and
                   (prec[stack[-1]] > prec[tok] or
                    (prec[stack[-1]] == prec[tok] and tok != "^"))):
                out.append(stack.pop())
            stack.append(tok)
            expect_operand = True
    if expect_operand:
        raise ValueError("expression ends unexpectedly")
    while stack:
        top = stack.pop()
        if top == "(":
            raise ValueError("mismatched parentheses")
        out.append(top)
    return out


def evaluate(expr: str) -> float:
    stack: list[float] = []
    for tok in to_rpn(expr):
        if tok.isdigit():
            stack.append(int(tok))
            continue
        b = stack.pop()
        a = stack.pop()
        if tok == "+":
            stack.append(a + b)
        elif tok == "-":
            stack.append(a - b)
        elif tok == "*":
            stack.append(a * b)
        elif tok == "/":
            if b == 0:
                raise ValueError("division by zero")
            stack.append(a / b)
        else:
            stack.append(a ** b)
    return stack[0]


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
