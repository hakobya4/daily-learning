"""
Day 6, Task 3 -- Python: Roman numeral conversion.

THE PROBLEM
------------
Write two functions:

  to_roman(n: int) -> str     -- convert an integer (1-3999) to its
                                  Roman numeral string.
  from_roman(s: str) -> int   -- convert a Roman numeral string back
                                  to an integer.

Roman numerals use these symbol values: I=1, V=5, X=10, L=50, C=100,
D=500, M=1000. Most numbers are formed by writing symbols largest to
smallest (e.g. 8 -> "VIII"), but there are 6 SUBTRACTIVE exceptions:
4="IV", 9="IX", 40="XL", 90="XC", 400="CD", 900="CM".

Example: to_roman(1994) -> "MCMXCIV"  (M=1000, CM=900, XC=90, IV=4)

HOW TO WORK THROUGH THIS
-------------------------
to_roman: build an ordered list of (value, symbol) pairs from LARGEST
to smallest, INCLUDING the 6 subtractive pairs (e.g. (900, "CM")
right after (1000, "M")). Walk the list; for each pair, while n >= 
value, append the symbol to the result and subtract value from n.

from_roman: walk the string left to right. For each symbol, if its
value is LESS than the value of the symbol immediately after it,
SUBTRACT it (that's the subtractive case, e.g. the 'I' in "IV");
otherwise ADD it. A running total handles both cases.

Run: python3 roman_numeral.py
"""


def to_roman(n: int) -> str:
    # TODO: walk an ordered (value, symbol) table largest-to-smallest,
    # including the 6 subtractive pairs, greedily subtracting.
    raise NotImplementedError


def from_roman(s: str) -> int:
    # TODO: walk left to right, subtracting a symbol whose value is
    # less than the NEXT symbol's value, adding otherwise.
    raise NotImplementedError


def _run_tests() -> None:
    cases = [
        (1, "I"),
        (4, "IV"),
        (9, "IX"),
        (14, "XIV"),
        (40, "XL"),
        (58, "LVIII"),
        (90, "XC"),
        (400, "CD"),
        (900, "CM"),
        (1994, "MCMXCIV"),
        (3999, "MMMCMXCIX"),
    ]
    for n, roman in cases:
        got = to_roman(n)
        assert got == roman, f"to_roman({n}) -> {got!r}, expected {roman!r}"
        got_back = from_roman(roman)
        assert got_back == n, f"from_roman({roman!r}) -> {got_back!r}, expected {n!r}"

    print("All roman_numeral tests passed.")


if __name__ == "__main__":
    _run_tests()
