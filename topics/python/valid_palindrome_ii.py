"""
Day 36, Task 4 -- Python: valid palindrome with one deletion.

THE PROBLEM
------------
Return True if s is a palindrome after deleting AT MOST one character.
Compare exactly as given (case-sensitive, no filtering).

  "aba"   -> True
  "abca"  -> True   (delete 'c' or 'b')
  "abc"   -> False
  ""      -> True

HOW TO WORK THROUGH THIS
-------------------------
Two pointers from the ends. On the first mismatch, you may skip either the
left or the right char: check whether s[l+1..r] or s[l..r-1] is a plain
palindrome. O(n).

Run: python3 valid_palindrome_ii.py
"""


def valid_palindrome(s: str) -> bool:
    def is_pal(l: int, r: int) -> bool:
        while l < r:
            if s[l] != s[r]:
                return False
            l += 1
            r -= 1
        return True

    l, r = 0, len(s) - 1
    while l < r:
        if s[l] != s[r]:
            return is_pal(l + 1, r) or is_pal(l, r - 1)
        l += 1
        r -= 1
    return True


def _run_tests():
    assert valid_palindrome("aba") is True
    assert valid_palindrome("abca") is True
    assert valid_palindrome("abc") is False
    assert valid_palindrome("") is True
    assert valid_palindrome("a") is True
    assert valid_palindrome("ab") is True
    assert valid_palindrome("abcba") is True
    assert valid_palindrome("deeee") is True
    assert valid_palindrome("abcdeba") is False
    assert valid_palindrome("eedede") is True
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
