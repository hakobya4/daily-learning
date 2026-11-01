"""
Day 41, Task 9 -- CS fundamentals: evaluate Reverse Polish Notation (stack).

THE PROBLEM
------------
eval_rpn(tokens) evaluates a list of string tokens: integers (possibly
negative) and the operators + - * /. Division truncates TOWARD ZERO
(7/-2 -> -3, not -4). Assume the expression is valid; return an int.

  ["2","1","+","3","*"]            -> 9
  ["4","13","5","/","+"]           -> 6

Run: python3 eval_rpn.py
"""


def eval_rpn(tokens: list) -> int:
    stack = []
    for t in tokens:
        if t in ("+", "-", "*", "/"):
            b = stack.pop()
            a = stack.pop()
            if t == "+":
                stack.append(a + b)
            elif t == "-":
                stack.append(a - b)
            elif t == "*":
                stack.append(a * b)
            else:
                stack.append(int(a / b))
        else:
            stack.append(int(t))
    return stack[0]


def _run_tests():
    assert eval_rpn(["2", "1", "+", "3", "*"]) == 9
    assert eval_rpn(["4", "13", "5", "/", "+"]) == 6
    assert eval_rpn(["7", "-2", "/"]) == -3
    assert eval_rpn(["-7", "2", "/"]) == -3
    assert eval_rpn(["5"]) == 5
    assert eval_rpn(["3", "4", "-"]) == -1
    assert eval_rpn(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]) == 22
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
