"""
Day 39, Task 1 -- Python: encode/decode a list of strings.

THE PROBLEM
------------
Design encode(strs) -> str and decode(s) -> list[str] so that
decode(encode(strs)) == strs for ANY list of strings, including empty
strings, an empty list, and strings containing digits, '#', ':' or newlines.
You may not rely on a delimiter character being absent from the data.

  encode(["ab", "", "c#d"])  -> some string s
  decode(s)                  -> ["ab", "", "c#d"]
  encode([]) and encode([""]) must decode to DIFFERENT results ([] vs [""]).

HOW TO WORK THROUGH THIS
-------------------------
Length-prefix each string (e.g. "<len>:<text>") and when decoding read the
digits up to ':' to learn how many characters to take next. O(total length).

Run: python3 encode_decode_strings.py
"""


def encode(strs: list) -> str:
    raise NotImplementedError


def decode(s: str) -> list:
    raise NotImplementedError


def _run_tests():
    cases = [
        [],
        [""],
        ["", ""],
        ["ab", "", "c#d"],
        ["3:abc", "1:", "::"],
        ["line1\nline2", "tab\t", "  "],
        ["héllo", "日本語", "😀"],
        ["x" * 1000, "9", "10:"],
    ]
    for c in cases:
        enc = encode(c)
        assert isinstance(enc, str)
        assert decode(enc) == c, c
    assert encode([]) != encode([""])
    assert decode(encode([])) == []
    assert decode(encode([""])) == [""]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
