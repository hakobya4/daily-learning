"""
Day 4, Task 4 -- Python: valid parentheses (stack matching).

THE PROBLEM
------------
Write is_valid(s) that takes a string containing only the characters
'(', ')', '[', ']', '{', '}' and returns True if the brackets are
validly matched and nested, False otherwise.

Valid means: every closing bracket matches the most recently opened,
still-unclosed bracket of the same type, and every opened bracket
gets closed by the end of the string. The empty string is valid.

Examples:
  "()[]{}"  -> True
  "([{}])"  -> True
  "(]"      -> False   (wrong bracket type closes it)
  "([)]"    -> False   (closes out of order -- not properly nested)
  "((("     -> False   (never closed)
  ")"       -> False   (closes something that was never opened)

HOW TO WORK THROUGH THIS
-------------------------
Classic stack problem: use a plain list as a stack. For each char --
if it's an opening bracket, push it. If it's a closing bracket, the
string can only be valid if the stack is non-empty AND the top of the
stack is the matching opening bracket for it; pop it if so, otherwise
return False immediately. After processing every char, the string is
only valid if the stack ended up EMPTY (every opener got closed).

A dict mapping each closing bracket to its matching opening bracket
(e.g. {")": "(", "]": "[", "}": "{"}) makes the "does this match"
check a single lookup.

Run: python3 valid_parentheses.py
"""


def is_valid(s: str) -> bool:
    # TODO: use a list as a stack. Push openers. On a closer, pop and
    # check it matches (return False on empty stack or mismatch).
    # Return True only if the stack is empty at the end.
    raise NotImplementedError


def _run_tests() -> None:
    cases = [
        ("", True),
        ("()", True),
        ("()[]{}", True),
        ("([{}])", True),
        ("(]", False),
        ("([)]", False),
        ("{[]}", True),
        ("(", False),
        (")", False),
        ("]", False),
        ("(())", True),
        ("(()", False),
        ("())", False),
    ]
    for s, expected in cases:
        got = is_valid(s)
        assert got == expected, f"is_valid({s!r}) -> {got!r}, expected {expected!r}"
    print("All valid_parentheses tests passed.")


if __name__ == "__main__":
    _run_tests()
