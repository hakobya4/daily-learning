"""
Day 37, Task 3 -- Python: add two binary strings.

THE PROBLEM
------------
Given two binary strings a and b (only '0'/'1', non-empty), return their
sum as a binary string, WITHOUT converting the whole strings with int(x, 2)
or bin(). Do the digit-by-digit carry addition yourself.

  ("11", "1")     -> "100"
  ("1010", "1011") -> "10101"
  ("0", "0")      -> "0"

HOW TO WORK THROUGH THIS
-------------------------
Walk both strings from the right with two indices and a carry. Each step:
total = carry + digit_a + digit_b; append total % 2; carry = total // 2.
Continue while either index is valid or carry is 1. Reverse at the end.

Run: python3 add_binary_strings.py
"""


def add_binary(a: str, b: str) -> str:
    i, j = len(a) - 1, len(b) - 1
    carry = 0
    out = []
    while i >= 0 or j >= 0 or carry:
        total = carry
        if i >= 0:
            total += ord(a[i]) - 48
            i -= 1
        if j >= 0:
            total += ord(b[j]) - 48
            j -= 1
        out.append(chr(48 + total % 2))
        carry = total // 2
    return "".join(reversed(out))


def _run_tests():
    assert add_binary("11", "1") == "100"
    assert add_binary("1010", "1011") == "10101"
    assert add_binary("0", "0") == "0"
    assert add_binary("1", "1") == "10"
    assert add_binary("1111", "1") == "10000"
    assert add_binary("100", "110010") == "110110"
    assert add_binary("0", "101") == "101"
    big = "1" * 70
    assert add_binary(big, "1") == "1" + "0" * 70
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
