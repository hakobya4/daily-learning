"""
Day 50, Task 3 -- Python: ransom note.

THE PROBLEM
------------
can_construct(note, magazine) returns True if the string note can be built from letters
of magazine, using each magazine letter at most once (case-sensitive; spaces count as
ordinary characters). Empty note -> True.
Examples: ("a", "b") -> False, ("aa", "aab") -> True, ("aab", "ab") -> False.
Hint: collections.Counter and a subtraction / comparison.

Run: python3 ransom_note.py
"""


def can_construct(note, magazine):
    raise NotImplementedError


def _run_tests():
    assert can_construct("a", "b") is False
    assert can_construct("aa", "ab") is False
    assert can_construct("aa", "aab") is True
    assert can_construct("", "") is True
    assert can_construct("", "xyz") is True
    assert can_construct("Ab", "bA") is True
    assert can_construct("ab", "AB") is False
    assert can_construct("a b", "ab") is False
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
