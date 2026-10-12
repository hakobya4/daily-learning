"""
Day 22, Task 2 -- Python: remove K digits.

THE PROBLEM
------------
Given a string num of digits and an int k, remove exactly k digits so the
remaining number is as SMALL as possible. Return it as a string with no
leading zeros; if nothing is left (or only zeros), return "0".

  remove_k_digits("1432219", 3) == "1219"
  remove_k_digits("10200", 1)   == "200"
  remove_k_digits("10", 2)      == "0"

Raise ValueError if k < 0 or k > len(num).

HOW TO WORK THROUGH THIS
-------------------------
Greedy with a monotonic stack: while the top of the stack is bigger than
the incoming digit and you still have removals left, pop. Afterwards drop
leftover removals from the end, then strip leading zeros.

Run: python3 remove_k_digits.py
"""


def remove_k_digits(num: str, k: int) -> str:
    raise NotImplementedError


def _run_tests():
    assert remove_k_digits("1432219", 3) == "1219"
    assert remove_k_digits("10200", 1) == "200"
    assert remove_k_digits("10", 2) == "0"
    assert remove_k_digits("9", 1) == "0"
    assert remove_k_digits("12345", 0) == "12345"
    assert remove_k_digits("12345", 2) == "123"
    assert remove_k_digits("54321", 2) == "321"
    assert remove_k_digits("112", 1) == "11"
    assert remove_k_digits("100", 1) == "0"
    assert remove_k_digits("", 0) == "0"
    for bad in (-1, 4):
        try:
            remove_k_digits("123", bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
