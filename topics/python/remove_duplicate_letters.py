"""
Day 32, Task 2 -- Python: remove duplicate letters (smallest subsequence).

THE PROBLEM
------------
Given a string s of lowercase letters, remove duplicate letters so that
every letter appears exactly once, and the result is the lexicographically
smallest string possible. You may only DELETE characters (the relative
order of the kept characters must match their order in s).

  "bcabc"     -> "abc"
  "cbacdcbc"  -> "acdb"
  "a"         -> "a"
  ""          -> ""

HOW TO WORK THROUGH THIS
-------------------------
Monotonic stack plus "last occurrence" index. Walk the string; skip letters
already on the stack; while the top of the stack is larger than the current
letter AND that top letter appears again later, pop it. Then push.

Run: python3 remove_duplicate_letters.py
"""


def remove_duplicate_letters(s: str) -> str:
    last = {c: i for i, c in enumerate(s)}
    stack, seen = [], set()
    for i, c in enumerate(s):
        if c in seen:
            continue
        while stack and stack[-1] > c and last[stack[-1]] > i:
            seen.discard(stack.pop())
        stack.append(c)
        seen.add(c)
    return "".join(stack)


def _run_tests():
    assert remove_duplicate_letters("bcabc") == "abc"
    assert remove_duplicate_letters("cbacdcbc") == "acdb"
    assert remove_duplicate_letters("a") == "a"
    assert remove_duplicate_letters("") == ""
    assert remove_duplicate_letters("aaaa") == "a"
    assert remove_duplicate_letters("abacb") == "abc"
    assert remove_duplicate_letters("edcba") == "edcba"
    assert remove_duplicate_letters("ecbacba") == "eacb"
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
