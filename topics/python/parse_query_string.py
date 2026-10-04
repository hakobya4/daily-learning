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


def _unquote(s: str) -> str:
    s = s.replace("+", " ")
    out = bytearray()
    i = 0
    while i < len(s):
        c = s[i]
        if c == "%":
            h = s[i + 1:i + 3]
            if len(h) != 2 or any(ch not in "0123456789abcdefABCDEF" for ch in h):
                raise ValueError(f"malformed escape in {s!r}")
            out.append(int(h, 16))
            i += 3
        else:
            out.extend(c.encode("utf-8"))
            i += 1
    return out.decode("utf-8")


def parse_query(qs: str) -> dict:
    if qs.startswith("?"):
        qs = qs[1:]
    result: dict = {}
    for pair in qs.split("&"):
        if not pair:
            continue
        key, _, value = pair.partition("=")
        result.setdefault(_unquote(key), []).append(_unquote(value))
    return result


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
