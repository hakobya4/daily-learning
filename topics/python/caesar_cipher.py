"""
Day 5, Task 4 -- Python: Caesar cipher encode/decode.

THE PROBLEM
------------
Write encode(text, shift) and decode(text, shift) that shift each
letter in `text` by `shift` positions through the alphabet, wrapping
around (shifting 'z' by 1 gives 'a'), preserving the original case,
and leaving non-letter characters (spaces, punctuation, digits)
completely unchanged. decode(encode(text, shift), shift) should
always return the original text.

Example: encode("Hello, World!", 3) -> "Khoor, Zruog!"

HOW TO WORK THROUGH THIS
-------------------------
For a single letter c: find its 0-25 position in the alphabet with
ord(c) - ord('a') (or ord('A') for uppercase), add the shift, take
the result mod 26 to wrap around, then convert back to a character
with chr(). Handle upper and lowercase separately (each against its
own 'a'/'A' base), and skip straight past anything where
c.isalpha() is False. decode() should just call encode() with the
shift negated -- don't write a separate implementation.

Run: python3 caesar_cipher.py
"""


def encode(text: str, shift: int) -> str:
    result_chars = []
    for c in text:
        if not c.isalpha():
            result_chars.append(c)
            continue
        base = ord('A') if c.isupper() else ord('a')
        offset = (ord(c) - base + shift) % 26
        result_chars.append(chr(base + offset))
    return "".join(result_chars)


def decode(text: str, shift: int) -> str:
    return encode(text, -shift)


def _run_tests() -> None:
    assert encode("abc", 1) == "bcd"
    assert encode("xyz", 3) == "abc"
    assert encode("Hello, World!", 3) == "Khoor, Zruog!"
    assert encode("ABC", 26) == "ABC"  # full wraparound is a no-op
    assert encode("", 5) == ""

    for text, shift in [
        ("Hello, World!", 3),
        ("abcXYZ", 13),
        ("Python 3.11 rocks!", 5),
        ("no letters here 123", 7),
    ]:
        roundtrip = decode(encode(text, shift), shift)
        assert roundtrip == text, f"round-trip failed for {text!r} shift {shift}: got {roundtrip!r}"

    print("All caesar_cipher tests passed.")


if __name__ == "__main__":
    _run_tests()
