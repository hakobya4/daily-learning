"""
Day 4, Task 3 -- Python: run-length encoding.

THE PROBLEM
------------
Write encode(s) that takes a string and returns a list of (char, count)
tuples, collapsing consecutive repeated characters into a single
(char, count) pair, in original order.

Example: encode("aaabbbccd") -> [("a", 3), ("b", 3), ("c", 2), ("d", 1)]

Also write decode(pairs) that takes a list of (char, count) tuples (as
produced by encode) and reconstructs the original string.

Example: decode([("a", 3), ("b", 3), ("c", 2), ("d", 1)]) -> "aaabbbccd"

HOW TO WORK THROUGH THIS
-------------------------
For encode: walk the string tracking a "current char" and a running
count; when the next char differs from the current one, append the
(char, count) pair to the result and reset the tracker to the new
char with count 1. Don't forget to append the final pair after the
loop ends.

For decode: for each (char, count) pair, repeat char count times and
concatenate.

Run: python3 run_length_encode.py
"""


def encode(s: str) -> list[tuple[str, int]]:
    result: list[tuple[str, int]] = []
    if not s:
        return result
    current_char = s[0]
    count = 1
    for ch in s[1:]:
        if ch == current_char:
            count += 1
        else:
            result.append((current_char, count))
            current_char = ch
            count = 1
    result.append((current_char, count))
    return result


def decode(pairs: list[tuple[str, int]]) -> str:
    return "".join(char * count for char, count in pairs)


def _run_tests() -> None:
    encode_cases = [
        ("", []),
        ("a", [("a", 1)]),
        ("aaabbbccd", [("a", 3), ("b", 3), ("c", 2), ("d", 1)]),
        ("aabcccccaaa", [("a", 2), ("b", 1), ("c", 5), ("a", 3)]),
    ]
    for s, expected in encode_cases:
        got = encode(s)
        assert got == expected, f"encode({s!r}) -> {got!r}, expected {expected!r}"

    decode_cases = [
        ([], ""),
        ([("a", 1)], "a"),
        ([("a", 3), ("b", 3), ("c", 2), ("d", 1)], "aaabbbccd"),
    ]
    for pairs, expected in decode_cases:
        got = decode(pairs)
        assert got == expected, f"decode({pairs!r}) -> {got!r}, expected {expected!r}"

    # round trip
    for s in ["", "a", "aaabbbccd", "aabcccccaaa", "abcdef"]:
        assert decode(encode(s)) == s, f"round trip failed for {s!r}"

    print("All run_length_encode tests passed.")


if __name__ == "__main__":
    _run_tests()
