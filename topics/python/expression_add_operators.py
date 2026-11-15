"""
Day 55, Task 10 -- Python: expression add operators (backtracking with a '*' carry).

THE PROBLEM
------------
Given a string num of digits and an integer target, return EVERY expression obtained by
inserting the binary operators '+', '-' or '*' between the digits (or inserting nothing,
which concatenates digits into a multi-digit operand) such that the expression evaluates
to target with normal precedence ('*' before '+' / '-').

Rules:
  * Operands may not have leading zeros: "05" is not a valid operand, but "0" is.
  * No unary minus: the first operand has no sign.
  * Return the expressions as a SORTED list of strings with no spaces, e.g. "1+2*3".
  * An empty num returns [].
  * Raise ValueError if num contains anything other than the characters 0-9.

Example:
  add_operators("123", 6)   -> ["1*2*3", "1+2+3"]
  add_operators("232", 8)   -> ["2*3+2", "2+3*2"]
  add_operators("105", 5)   -> ["1*0+5", "10-5"]
  add_operators("00", 0)    -> ["0*0", "0+0", "0-0"]
  add_operators("3456237490", 9191) -> []

Hint: DFS over (position, expression_so_far, value_so_far, last_operand). When appending
'*' with operand x, undo the last operand and apply the multiplication:
    value - last + last * x,   new last = last * x
For '+': value + x, last = x.  For '-': value - x, last = -x.
Never call eval() -- the whole point is to track the value incrementally.

Run: python3 expression_add_operators.py
"""


def add_operators(num, target):
    if not isinstance(num, str) or any(c not in "0123456789" for c in num):
        raise ValueError(f"num must contain only digits 0-9, got {num!r}")
    n = len(num)
    out = []

    def dfs(pos, expr, value, last):
        if pos == n:
            if value == target:
                out.append(expr)
            return
        for end in range(pos + 1, n + 1):
            s = num[pos:end]
            if len(s) > 1 and s[0] == "0":    # no leading-zero operands
                break
            x = int(s)
            dfs(end, expr + "+" + s, value + x, x)
            dfs(end, expr + "-" + s, value - x, -x)
            # undo the last operand, then apply the multiplication to it
            dfs(end, expr + "*" + s, value - last + last * x, last * x)

    for end in range(1, n + 1):
        first = num[:end]
        if len(first) > 1 and first[0] == "0":
            break
        x = int(first)
        dfs(end, first, x, x)
    return sorted(out)


def _evaluate(expr):
    # Tiny precedence-aware evaluator used only by the tests (no eval()).
    cur = ""
    tokens = []
    for ch in expr:
        if ch.isdigit():
            cur += ch
        else:
            tokens.append(int(cur))
            tokens.append(ch)
            cur = ""
    tokens.append(int(cur))
    # collapse '*'
    stack = [tokens[0]]
    i = 1
    while i < len(tokens):
        op, val = tokens[i], tokens[i + 1]
        if op == "*":
            stack[-1] = stack[-1] * val
        else:
            stack.append(op)
            stack.append(val)
        i += 2
    total = stack[0]
    for j in range(1, len(stack), 2):
        total = total + stack[j + 1] if stack[j] == "+" else total - stack[j + 1]
    return total


def _run_tests():
    assert add_operators("123", 6) == ["1*2*3", "1+2+3"]
    assert add_operators("232", 8) == ["2*3+2", "2+3*2"]
    assert add_operators("105", 5) == ["1*0+5", "10-5"]
    assert add_operators("00", 0) == ["0*0", "0+0", "0-0"]
    assert add_operators("3456237490", 9191) == []
    assert add_operators("", 0) == []
    assert add_operators("7", 7) == ["7"]
    assert add_operators("7", 8) == []
    assert add_operators("123", 123) == ["123"]
    assert add_operators("1000", 1000) == ["1000"]         # trailing zeros are fine
    assert "1*05" not in add_operators("105", 5)            # no leading-zero operands
    assert add_operators("2147483648", -2147483648) == []   # no unary minus

    # Every returned expression must really evaluate to the target, have no
    # leading-zero operands, and the result must be sorted and duplicate-free.
    for num, target in [("1234", 10), ("9999", 81), ("1203", 6), ("123456", 21)]:
        res = add_operators(num, target)
        assert res == sorted(set(res)), (num, target)
        assert res, (num, target)
        for e in res:
            assert e.replace("+", "").replace("-", "").replace("*", "") == num
            assert _evaluate(e) == target, e
            for operand in e.replace("+", " ").replace("-", " ").replace("*", " ").split():
                assert operand == "0" or not operand.startswith("0"), e

    assert add_operators("1234", 10) == ["1*2*3+4", "1+2+3+4"]

    for bad in ("12a", "1 2", "-12", "1.5"):
        try:
            add_operators(bad, 3)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{bad!r} must raise ValueError")

    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
