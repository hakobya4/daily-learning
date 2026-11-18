"""
Day 59, Task 7 -- CS fundamentals: LZW compression with a bounded dictionary + bit packing.

THE PROBLEM
------------
Implement four functions.

compress(data: bytes, max_bits=12) -> list[int]
    Classic LZW. The dictionary starts with the 256 single bytes (code i = bytes([i])).
    Grow the current string w while w + next byte is in the dictionary; otherwise emit
    code(w), add w + next byte as the next free code (256, 257, ...) -- but ONLY while
    the dictionary holds fewer than 2**max_bits entries (after that it is frozen) --
    and restart w with that byte. Emit code(w) at the end. b"" -> [].
    max_bits outside 9..16 -> ValueError.

decompress(codes, max_bits=12) -> bytes
    The inverse, rebuilding the same dictionary on the fly (same freezing rule). Handle
    the special "KwKwK" case: a code equal to the NEXT code to be assigned (not yet in
    the dictionary) means w + w[0]. Any other unknown code (or a first code >= 256)
    -> ValueError. [] -> b"".

pack(codes, width) -> bytes
    Write each code as exactly `width` bits, MSB first, back to back; pad the last byte
    with zero bits. A code that doesn't fit in width bits -> ValueError.

unpack(data, width, count) -> list[int]
    Read `count` codes of `width` bits back (ignore padding). If data has fewer than
    count*width bits -> ValueError.

Examples:
  compress(b"TOBEORNOTTOBEORTOBEORNOT")
    -> [84, 79, 66, 69, 79, 82, 78, 79, 84, 256, 258, 260, 265, 259, 261, 263]
  compress(b"abababab") -> [97, 98, 256, 258, 98]   (258 is used before decompress
                                                     has seen it: the KwKwK case)
  pack([1, 2, 3], 12).hex() -> "0010020030"

Hint: compress keeps dict bytes -> code; decompress keeps code -> bytes and adds
prev + current[:1] after decoding each code. For packing keep an integer
accumulator and a bit count; flush whole bytes while count >= 8.

Run: python3 lzw_codec.py
"""


def compress(data, max_bits=12):
    raise NotImplementedError


def decompress(codes, max_bits=12):
    raise NotImplementedError


def pack(codes, width):
    raise NotImplementedError


def unpack(data, width, count):
    raise NotImplementedError


def _run_tests():
    import random

    assert compress(b"TOBEORNOTTOBEORTOBEORNOT") == \
        [84, 79, 66, 69, 79, 82, 78, 79, 84, 256, 258, 260, 265, 259, 261, 263]
    assert compress(b"abababab") == [97, 98, 256, 258, 98]
    assert compress(b"aaaaaaa") == [97, 256, 257, 97]
    assert compress(b"") == [] and decompress([]) == b""
    assert decompress([97, 98, 256, 258, 98]) == b"abababab"
    assert decompress([97, 256, 257, 97]) == b"aaaaaaa"
    assert decompress(compress(b"TOBEORNOTTOBEORTOBEORNOT")) == b"TOBEORNOTTOBEORTOBEORNOT"
    for bad in ([97, 300], [256], [97, 98, 259]):
        try:
            decompress(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for %r" % (bad,))
    for mb in (8, 17):
        try:
            compress(b"x", max_bits=mb)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for max_bits=%d" % mb)

    assert pack([1, 2, 3], 12).hex() == "0010020030"
    assert pack([256, 257], 9).hex() == "804040"
    assert pack([], 9) == b""
    assert unpack(bytes.fromhex("0010020030"), 12, 3) == [1, 2, 3]
    assert unpack(bytes.fromhex("804040"), 9, 2) == [256, 257]
    try:
        pack([512], 9)
    except ValueError:
        pass
    else:
        raise AssertionError("512 does not fit in 9 bits")
    try:
        unpack(b"\x00", 9, 1)
    except ValueError:
        pass
    else:
        raise AssertionError("not enough bits")

    # frozen dictionary: with 9 bits no code may reach 512, round trip still works
    data = bytes((i * i + 3 * i) % 11 + 97 for i in range(20000))
    c9 = compress(data, max_bits=9)
    assert max(c9) < 512 and len(c9) == 955 and decompress(c9, max_bits=9) == data
    assert len(compress(data, max_bits=12)) == 658   # a bigger dictionary compresses better

    rng = random.Random(59)
    for _ in range(200):
        s = bytes(rng.choice(b"abc") for _ in range(rng.randint(0, 3000)))
        for mb in (9, 12):
            c = compress(s, mb)
            assert decompress(c, mb) == s
            assert all(0 <= x < (1 << mb) for x in c)
            assert unpack(pack(c, mb), mb, len(c)) == c
    text = bytes(range(256)) * 4
    assert decompress(compress(text)) == text
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
