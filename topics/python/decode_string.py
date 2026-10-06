"""
Day 16, Task 2 -- Python: decode nested repeat strings.

THE PROBLEM
------------
Decode strings of the form k[encoded], meaning encoded repeated k times.
k is a positive integer (may be multi-digit); brackets nest; letters
outside brackets are copied as-is.

    decode("3[a]2[bc]")      -> "aaabcbc"
    decode("3[a2[c]]")       -> "accaccacc"
    decode("2[ab]x1[y]")     -> "ababxy"
    decode("10[z]")          -> "zzzzzzzzzz"
    decode("")               -> ""

Raise ValueError for unbalanced brackets ("3[a", "a]").

HOW TO WORK THROUGH THIS
-------------------------
A stack of (previous_string, repeat_count) pairs works well: push on '[',
pop and combine on ']'.

Run: python3 decode_string.py
"""


def decode(s: str) -> str:
    raise NotImplementedError


def _run_tests():
    assert decode("3[a]2[bc]") == "aaabcbc"
    assert decode("3[a2[c]]") == "accaccacc"
    assert decode("2[ab]x1[y]") == "ababxy"
    assert decode("10[z]") == "z" * 10
    assert decode("") == ""
    assert decode("abc") == "abc"
    assert decode("2[2[2[a]]]") == "a" * 8
    for bad in ("3[a", "a]", "2[[a]"):
        try:
            decode(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad!r}")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
