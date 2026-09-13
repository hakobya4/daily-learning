"""
Day 1, Task 3 -- Python: palindrome check.

"""

def is_palindrome(s: str) -> bool:
    lowercase_s = s.lower()
    nospaces_s = lowercase_s.replace(" ", "")
    removed_punctuation_s = ""
    for char in nospaces_s:
        if char.isalnum():
            removed_punctuation_s += char
    
    return removed_punctuation_s == removed_punctuation_s[::-1]
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
