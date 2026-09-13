"""
Day 2, Task 2 -- Python: palindrome check.

THE PROBLEM
------------
Write is_palindrome(s) that returns True if `s` reads the same forwards
and backwards, IGNORING case, spaces, and punctuation.

Examples that should return True:
    "racecar"
    "A man, a plan, a canal: Panama"
    "Was it a car or a cat I saw?"

Examples that should return False:
    "hello"
    "Not a palindrome"

HOW TO WORK THROUGH THIS
-------------------------
Think about what "ignore punctuation/spaces/case" means as a
preprocessing step BEFORE you check the palindrome property itself --
that separation (clean the input, then check) is a pattern worth
noticing, since it shows up constantly in string-processing problems.

Run: python3 palindrome.py
"""

def is_palindrome(s: str) -> bool:
    # TODO: normalize `s` (lowercase, strip non-alphanumeric characters),
    # then check whether the cleaned string equals its own reverse.
    raise NotImplementedError


def _run_tests() -> None:
    cases = [
        ("racecar", True),
        ("A man, a plan, a canal: Panama", True),
        ("Was it a car or a cat I saw?", True),
        ("hello", False),
        ("Not a palindrome", False),
        ("", True),   # empty string is trivially a palindrome
        ("a", True),
    ]
    for s, expected in cases:
        got = is_palindrome(s)
        assert got == expected, f"is_palindrome({s!r}) -> {got!r}, expected {expected!r}"
    print("All palindrome tests passed.")


if __name__ == "__main__":
    _run_tests()
