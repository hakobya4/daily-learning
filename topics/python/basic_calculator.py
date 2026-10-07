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
    tokens = []
    i = 0
    while i < len(expr):
        c = expr[i]
        if c.isspace():
            i += 1
        elif c.isdigit():
            j = i
            while j < len(expr) and expr[j].isdigit():
                j += 1
            tokens.append(int(expr[i:j]))
            i = j
        elif c in "+-*/()":
            tokens.append(c)
            i += 1
        else:
            raise ValueError(f"bad character {c!r}")
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def parse_expr():
        nonlocal pos
        val = parse_term()
        while peek() in ("+", "-"):
            op = tokens[pos]
            pos += 1
            rhs = parse_term()
            val = val + rhs if op == "+" else val - rhs
        return val

    def parse_term():
        nonlocal pos
        val = parse_factor()
        while peek() in ("*", "/"):
            op = tokens[pos]
            pos += 1
            rhs = parse_factor()
            if op == "*":
                val *= rhs
            else:
                if rhs == 0:
                    raise ZeroDivisionError("division by zero")
                val = int(val / rhs) if abs(val) < 2**52 else (abs(val) // abs(rhs)) * (1 if (val < 0) == (rhs < 0) else -1)
        return val

    def parse_factor():
        nonlocal pos
        t = peek()
        if t == "-":
            pos += 1
            return -parse_factor()
        if t == "+":
            pos += 1
            return parse_factor()
        if t == "(":
            pos += 1
            val = parse_expr()
            if peek() != ")":
                raise ValueError("missing )")
            pos += 1
            return val
        if isinstance(t, int):
            pos += 1
            return t
        raise ValueError("unexpected token")

    result = parse_expr()
    if pos != len(tokens):
        raise ValueError("trailing tokens")
    return result


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
