"""
Day 26, Task 2 -- Python: bulls and cows.

THE PROBLEM
------------
get_hint(secret, guess) compares two digit strings of equal length and
returns "<A>A<B>B" where A (bulls) is the number of positions with the
same digit, and B (cows) is the number of digits in guess that exist in
secret but at a different position (each secret digit can be matched once).

  get_hint("1807", "7810") -> "1A3B"
  get_hint("1123", "0111") -> "1A1B"

HOW TO WORK THROUGH THIS
-------------------------
One pass counts bulls and tallies the NON-bull digits of both strings;
cows = sum over digits of min(secret_count, guess_count).

Run: python3 bulls_and_cows.py
"""


def get_hint(secret: str, guess: str) -> str:
    raise NotImplementedError


def _run_tests():
    assert get_hint("1807", "7810") == "1A3B"
    assert get_hint("1123", "0111") == "1A1B"
    assert get_hint("1", "0") == "0A0B"
    assert get_hint("1122", "1222") == "3A0B"
    assert get_hint("1234", "1234") == "4A0B"
    assert get_hint("1234", "4321") == "0A4B"
    assert get_hint("", "") == "0A0B"
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
