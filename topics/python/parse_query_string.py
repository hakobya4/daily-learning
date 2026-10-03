"""
Day 13, Task 2 -- Python: parse a URL query string.

THE PROBLEM
------------
Implement parse_query(qs) that turns "a=1&b=two&a=3" into
{"a": ["1", "3"], "b": ["two"]}  (every value is a LIST, in order of
appearance).

Rules:
- A leading "?" is ignored. Empty string -> {}.
- "+" means a space, and "%XX" is a percent-escape for the byte 0xXX
  (decode as UTF-8). Do not use urllib.parse.
- A pair without "=" ("flag") gets the value "".
- Empty pairs (from "&&" or a trailing "&") are skipped.
- Split each pair on the FIRST "=" only ("x=a=b" -> {"x": ["a=b"]}).
- A malformed escape ("%zz" or a "%" at the very end) raises ValueError.

HOW TO WORK THROUGH THIS
-------------------------
Write a helper _unquote(s) that replaces "+" first, then walks the
string collecting bytes, and finally bytes.decode("utf-8").

Run: python3 parse_query_string.py
"""


def parse_query(qs: str) -> dict:
    raise NotImplementedError


def _run_tests() -> None:
    assert parse_query("") == {}
    assert parse_query("?") == {}
    assert parse_query("a=1&b=two&a=3") == {"a": ["1", "3"], "b": ["two"]}
    assert parse_query("?q=hello+world") == {"q": ["hello world"]}
    assert parse_query("name=J%C3%BCrgen") == {"name": ["Jürgen"]}
    assert parse_query("flag&x=") == {"flag": [""], "x": [""]}
    assert parse_query("a=1&&b=2&") == {"a": ["1"], "b": ["2"]}
    assert parse_query("x=a=b") == {"x": ["a=b"]}
    assert parse_query("p=100%25") == {"p": ["100%"]}
    for bad in ("a=%zz", "a=50%", "a=%4"):
        try:
            parse_query(bad)
            assert False, f"should reject {bad!r}"
        except ValueError:
            pass
    print("All parse_query_string tests passed.")


if __name__ == "__main__":
    _run_tests()
