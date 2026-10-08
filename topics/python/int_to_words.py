"""
Day 18, Task 4 -- Python: integer to English words.

THE PROBLEM
------------
Convert a non-negative integer to English words, title case, no "and",
single spaces.

  0          -> "Zero"
  123        -> "One Hundred Twenty Three"
  12345      -> "Twelve Thousand Three Hundred Forty Five"
  1000010    -> "One Million Ten"

Support up to 2**31 - 1 (billions). Raise ValueError for negative numbers,
bools, or non-ints.

HOW TO WORK THROUGH THIS
-------------------------
Handle chunks of three digits with a helper (below 20 table, tens table,
hundreds), then append "Thousand"/"Million"/"Billion" for non-zero chunks.

Run: python3 int_to_words.py
"""


def int_to_words(n: int) -> str:
    raise NotImplementedError


def _run_tests():
    assert int_to_words(0) == "Zero"
    assert int_to_words(7) == "Seven"
    assert int_to_words(19) == "Nineteen"
    assert int_to_words(40) == "Forty"
    assert int_to_words(100) == "One Hundred"
    assert int_to_words(123) == "One Hundred Twenty Three"
    assert int_to_words(12345) == "Twelve Thousand Three Hundred Forty Five"
    assert int_to_words(1000000) == "One Million"
    assert int_to_words(1000010) == "One Million Ten"
    assert int_to_words(2147483647) == (
        "Two Billion One Hundred Forty Seven Million Four Hundred Eighty "
        "Three Thousand Six Hundred Forty Seven")
    for bad in (-1, True, 3.5, "5", None):
        try:
            int_to_words(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for %r" % (bad,))
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
