"""
Day 62, Task 1 -- Python: a UTF-8 encoder and a STRICT decoder from scratch.

THE PROBLEM
------------
Implement UTF-8 yourself, without str.encode / bytes.decode / codecs (they may only
be used inside the tests to cross-check you).

UTF-8 encodes a code point U+0000..U+10FFFF in 1..4 bytes:
    U+0000   .. U+007F    0xxxxxxx
    U+0080   .. U+07FF    110xxxxx 10xxxxxx
    U+0800   .. U+FFFF    1110xxxx 10xxxxxx 10xxxxxx
    U+10000  .. U+10FFFF  11110xxx 10xxxxxx 10xxxxxx 10xxxxxx

1) encode_code_point(cp) -> bytes
   Raise ValueError for cp < 0, cp > 0x10FFFF, or a surrogate (0xD800..0xDFFF).

2) utf8_encode(s) -> bytes        (encode every character of the str s; ord() is fine)

3) utf8_decode(data, errors="strict") -> str
   Walk the bytes and rebuild the code points. A sequence is INVALID when:
     - its lead byte is a continuation byte (0x80..0xBF) or 0xC0, 0xC1, 0xF5..0xFF;
     - it is truncated (end of data, or a non-continuation byte where a 10xxxxxx
       byte was expected);
     - it is OVERLONG (e.g. C0 AF or E0 80 AF for "/" -- every code point must use
       its shortest form);
     - it encodes a surrogate (ED A0 80 .. ED BF BF) or a value above U+10FFFF
       (F4 90 80 80 and up).
   errors="strict":  raise UTF8Error(position, reason) where position is the index of
                     the FIRST byte of the bad sequence.
   errors="replace": emit U+FFFD for each "maximal subpart" of an ill-formed sequence,
                     matching what Python's own b.decode("utf-8", "replace") does, then
                     resume. Practical rule: a lead byte that starts a valid prefix
                     consumes the continuation bytes that are still allowed by the
                     table below; the first byte that is NOT allowed ends that
                     subpart (one U+FFFD) and is re-examined as a new lead byte.
                       lead E0 -> 2nd byte A0..BF      lead ED -> 2nd byte 80..9F
                       lead F0 -> 2nd byte 90..BF      lead F4 -> 2nd byte 80..8F
                       otherwise continuation = 80..BF
                     A byte that can never start a sequence is one U+FFFD on its own.

4) count_code_points(data) -> int
   Count characters in VALID UTF-8 data without decoding: count the bytes that are
   NOT continuation bytes. (One line. Assume the input is valid.)

Run: python3 utf8_codec.py
"""


class UTF8Error(ValueError):
    def __init__(self, position, reason):
        super().__init__(f"invalid UTF-8 at byte {position}: {reason}")
        self.position = position
        self.reason = reason


def encode_code_point(cp):
    raise NotImplementedError


def utf8_encode(s):
    raise NotImplementedError


def utf8_decode(data, errors="strict"):
    raise NotImplementedError


def count_code_points(data):
    raise NotImplementedError


def _run_tests():
    samples = ["", "A", "/", "é", "€", "𝄞", "Hello, Բարեւ, 世界 🌍!", "\x00\x7f\x80߿ࠀ￿\U00010000\U0010ffff"]
    for s in samples:
        assert utf8_encode(s) == s.encode("utf-8"), s
        assert utf8_decode(s.encode("utf-8")) == s, s
        assert count_code_points(s.encode("utf-8")) == len(s), s

    assert encode_code_point(0x41) == b"A"
    assert encode_code_point(0x20AC) == b"\xe2\x82\xac"
    assert encode_code_point(0x1F30D) == b"\xf0\x9f\x8c\x8d"
    for bad in (-1, 0x110000, 0xD800, 0xDFFF):
        try:
            encode_code_point(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad:#x}")

    # strict errors: (data, position of first bad byte)
    strict_cases = [
        (b"\x80", 0),                    # lone continuation byte
        (b"ab\xc0\xaf", 2),              # overlong "/" (C0 is never valid)
        (b"\xe0\x80\xaf", 0),            # overlong 3-byte "/"
        (b"\xf0\x80\x80\xaf", 0),        # overlong 4-byte "/"
        (b"\xed\xa0\x80", 0),            # surrogate U+D800
        (b"\xf4\x90\x80\x80", 0),        # U+110000
        (b"x\xe2\x82", 1),               # truncated at end
        (b"\xe2\x28\xa1", 0),            # 2nd byte not a continuation
        (b"ok\xff", 2),                  # FF never valid
        (b"\xc3\xa9\xf5\x80", 2),        # F5 never valid
    ]
    for data, pos in strict_cases:
        try:
            utf8_decode(data)
        except UTF8Error as e:
            assert e.position == pos, (data, e.position, pos)
        else:
            raise AssertionError(f"expected UTF8Error for {data!r}")

    replace_cases = [
        b"\x80", b"ab\xc0\xaf", b"\xe0\x80\xaf", b"\xed\xa0\x80z", b"\xf4\x90\x80\x80",
        b"x\xe2\x82", b"\xe2\x28\xa1", b"\xf0\x9f\x8c", b"\xf0\x9f\x8cA\xf0\x9f\x8c\x8d",
        b"\xe1\x80\xe2\xf0\x91\x92\xf1\xbf\x41", b"\xc2\x41\x42", b"\xff\xfe\xfd",
    ]
    for data in replace_cases:
        assert utf8_decode(data, errors="replace") == data.decode("utf-8", "replace"), data

    import random
    rng = random.Random(62)
    for _ in range(300):
        blob = bytes(rng.choice([rng.randrange(256), rng.randrange(0x80, 0xC0), 0xE0, 0xED, 0xF0, 0xF4])
                     for _ in range(rng.randrange(12)))
        assert utf8_decode(blob, errors="replace") == blob.decode("utf-8", "replace"), blob
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
