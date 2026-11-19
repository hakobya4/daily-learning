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


def _check_max_bits(max_bits):
    if not (9 <= max_bits <= 16):
        raise ValueError("max_bits must be in 9..16, got %r" % (max_bits,))


def compress(data, max_bits=12):
    _check_max_bits(max_bits)
    limit = 1 << max_bits
    table = {bytes([i]): i for i in range(256)}
    out = []
    w = b""
    for byte in data:
        wc = w + bytes([byte])
        if wc in table:
            w = wc
            continue
        out.append(table[w])
        if len(table) < limit:
            table[wc] = len(table)
        w = bytes([byte])
    if w:
        out.append(table[w])
    return out


def decompress(codes, max_bits=12):
    _check_max_bits(max_bits)
    codes = list(codes)
    if not codes:
        return b""
    limit = 1 << max_bits
    table = [bytes([i]) for i in range(256)]
    first = codes[0]
    if not (0 <= first < 256):
        raise ValueError("invalid first code %r" % (first,))
    prev = table[first]
    out = [prev]
    for code in codes[1:]:
        if 0 <= code < len(table):
            cur = table[code]
        elif code == len(table) and len(table) < limit:
            cur = prev + prev[:1]  # KwKwK case
        else:
            raise ValueError("invalid code %r" % (code,))
        out.append(cur)
        if len(table) < limit:
            table.append(prev + cur[:1])
        prev = cur
    return b"".join(out)


def pack(codes, width):
    if width <= 0:
        raise ValueError("width must be positive")
    out = bytearray()
    acc = 0
    nbits = 0
    for code in codes:
        if not (0 <= code < (1 << width)):
            raise ValueError("code %r does not fit in %d bits" % (code, width))
        acc = (acc << width) | code
        nbits += width
        while nbits >= 8:
            nbits -= 8
            out.append((acc >> nbits) & 0xFF)
        acc &= (1 << nbits) - 1
    if nbits:
        out.append((acc << (8 - nbits)) & 0xFF)
    return bytes(out)


def unpack(data, width, count):
    if width <= 0:
        raise ValueError("width must be positive")
    if len(data) * 8 < count * width:
        raise ValueError("not enough bits for %d codes of width %d" % (count, width))
    out = []
    acc = 0
    nbits = 0
    mask = (1 << width) - 1
    it = iter(data)
    while len(out) < count:
        while nbits < width:
            acc = (acc << 8) | next(it)
            nbits += 8
        nbits -= width
        out.append((acc >> nbits) & mask)
        acc &= (1 << nbits) - 1
    return out


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
