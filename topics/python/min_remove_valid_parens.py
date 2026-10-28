"""
Day 38, Task 2 -- Python: minimum removals to make parentheses valid.

THE PROBLEM
------------
Given a string s of lowercase letters and '(' / ')', remove the MINIMUM number
of parentheses so the result is valid (every '(' matched, no stray ')').
Return any valid result with the fewest removals -- the tests accept only the
canonical answer produced by: drop unmatched ')' while scanning left to right,
then drop the LAST unmatched '(' characters.

  "lee(t(c)o)de)" -> "lee(t(c)o)de"
  "a)b(c)d"       -> "ab(c)d"
  "))(("          -> ""
  "(a(b(c)d)"     -> "a(b(c)d)"   (the stack leaves index 0 unmatched, so it is dropped)

HOW TO WORK THROUGH THIS
-------------------------
Scan once with a stack of indices of '(' . On ')' pop if stack non-empty,
otherwise mark that index for removal. After the scan, whatever indices
remain in the stack are unmatched '(' -> mark them too. Rebuild the string.

Run: python3 min_remove_valid_parens.py
"""


def min_remove_to_make_valid(s: str) -> str:
    remove = set()
    stack = []
    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        elif ch == ")":
            if stack:
                stack.pop()
            else:
                remove.add(i)
    remove.update(stack)
    return "".join(ch for i, ch in enumerate(s) if i not in remove)


def _run_tests():
    assert min_remove_to_make_valid("lee(t(c)o)de)") == "lee(t(c)o)de"
    assert min_remove_to_make_valid("a)b(c)d") == "ab(c)d"
    assert min_remove_to_make_valid("))((") == ""
    assert min_remove_to_make_valid("(a(b(c)d)") == "a(b(c)d)"
    assert min_remove_to_make_valid("") == ""
    assert min_remove_to_make_valid("abc") == "abc"
    assert min_remove_to_make_valid("(((") == ""
    assert min_remove_to_make_valid("()()") == "()()"
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
