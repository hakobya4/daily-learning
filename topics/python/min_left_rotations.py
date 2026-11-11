"""
Day 51, Task 2 -- Python: minimum left rotations to turn one string into another.

THE PROBLEM
------------
min_left_rotations(a, b): one left rotation moves the first character of a to its end
("abcde" -> "bcdea"). Return the smallest k >= 0 such that rotating a left k times gives b,
or -1 if that is impossible (different lengths, or b is not a rotation of a).
Examples: ("abcde", "cdeab") -> 2, ("abab", "baba") -> 1, ("abc", "abd") -> -1.
Hint: b is a rotation of a iff b occurs in a + a (and len(a) == len(b)); the index is k.

Run: python3 min_left_rotations.py
"""


def min_left_rotations(a, b):
    # b is a rotation of a iff len matches and b occurs in a + a; the first index is k.
    if len(a) != len(b):
        return -1
    if not a:
        return 0
    return (a + a).find(b)


def _run_tests():
    assert min_left_rotations("abcde", "cdeab") == 2
    assert min_left_rotations("abcde", "abced") == -1
    assert min_left_rotations("aa", "aa") == 0
    assert min_left_rotations("", "") == 0
    assert min_left_rotations("abc", "ab") == -1
    assert min_left_rotations("abab", "abab") == 0
    assert min_left_rotations("abab", "baba") == 1
    assert min_left_rotations("abcde", "eabcd") == 4
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
