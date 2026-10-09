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
    raise NotImplementedError


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
