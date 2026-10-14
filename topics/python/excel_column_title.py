"""
Day 24, Task 3 -- Python: Excel column titles (bijective base 26).

THE PROBLEM
------------
Spreadsheet columns go A..Z, AA..AZ, BA.., ..ZZ, AAA..
Implement both directions:

  column_to_number("A") == 1     column_to_number("AB") == 28
  number_to_column(1) == "A"     number_to_column(703) == "AAA"

There is no zero digit, so this is NOT plain base 26 (26 -> "Z", 27 -> "AA").
column_to_number is case-insensitive. Raise ValueError for an empty string
or any non-letter in column_to_number, and for numbers < 1 in
number_to_column.

HOW TO WORK THROUGH THIS
-------------------------
to number: n = n * 26 + (ord(ch) - 64). To title: repeatedly do
n -= 1; letter = chr(65 + n % 26); n //= 26, then reverse.

Run: python3 excel_column_title.py
"""


def column_to_number(title: str) -> int:
    raise NotImplementedError


def number_to_column(n: int) -> str:
    raise NotImplementedError


def _run_tests():
    assert column_to_number("A") == 1
    assert column_to_number("Z") == 26
    assert column_to_number("AA") == 27
    assert column_to_number("AB") == 28
    assert column_to_number("zy") == 701
    assert column_to_number("AAA") == 703
    assert number_to_column(1) == "A"
    assert number_to_column(26) == "Z"
    assert number_to_column(27) == "AA"
    assert number_to_column(52) == "AZ"
    assert number_to_column(701) == "ZY"
    assert number_to_column(703) == "AAA"
    for n in range(1, 2000):
        assert column_to_number(number_to_column(n)) == n
    for bad in ("", "A1", "-"):
        try:
            column_to_number(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for %r" % bad)
    for bad in (0, -5):
        try:
            number_to_column(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
