"""
Day 19, Task 4 -- Python: decode ways.

THE PROBLEM
------------
A message of digits is decoded with 'A'=1, 'B'=2, ..., 'Z'=26. Return the
number of different ways to decode the string s.

  "12"  -> 2   (AB, L)
  "226" -> 3   (BZ, VF, BBF)
  "06"  -> 0   (a leading zero is not decodable)

Raise ValueError if s is empty or not a string of digits.

HOW TO WORK THROUGH THIS
-------------------------
dp[i] = ways to decode the first i characters. A single digit 1-9 adds
dp[i-1]; a two-digit number 10-26 adds dp[i-2]. Keep only two variables.

Run: python3 decode_ways.py
"""


def num_decodings(s: str) -> int:
    if not isinstance(s, str) or not s or not s.isascii() or not s.isdigit():
        raise ValueError("s must be a non-empty string of digits")
    prev2, prev1 = 1, 1  # dp[i-2], dp[i-1]; dp[0] = 1
    if s[0] == "0":
        return 0
    for i in range(1, len(s)):
        cur = 0
        if s[i] != "0":
            cur += prev1
        if 10 <= int(s[i - 1:i + 1]) <= 26:
            cur += prev2
        prev2, prev1 = prev1, cur
    return prev1


def _run_tests():
    assert num_decodings("12") == 2
    assert num_decodings("226") == 3
    assert num_decodings("06") == 0
    assert num_decodings("0") == 0
    assert num_decodings("10") == 1
    assert num_decodings("27") == 1
    assert num_decodings("100") == 0
    assert num_decodings("11106") == 2
    for bad in ("", "1a", None, 12):
        try:
            num_decodings(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for %r" % (bad,))
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
