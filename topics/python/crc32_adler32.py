"""
Day 62, Task 10 -- Python: CRC-32 (bitwise and table-driven) and Adler-32 from scratch.

THE PROBLEM
------------
zip, gzip and PNG protect data with CRC-32; zlib streams use Adler-32. Implement both
without zlib / binascii (the tests use zlib only to check you).

CRC-32 (the "IEEE" / zlib variant) is defined by:
    reflected polynomial  0xEDB88320
    initial value         0xFFFFFFFF
    final XOR             0xFFFFFFFF
    bits processed LSB-first (reflected input and output)

1) crc32_bitwise(data, crc=0) -> int
   For each byte: crc ^= byte; then 8 times: if crc & 1: crc = (crc >> 1) ^ POLY
   else crc >>= 1. Wrap the whole thing in the init / final XOR so that chaining
   works like zlib: crc32_bitwise(b, crc32_bitwise(a)) == crc32_bitwise(a + b).
   (Hint: start from `crc ^ 0xFFFFFFFF`, and XOR again at the end.)

2) make_crc_table() -> list of 256 ints
   table[n] = the result of running the 8-step inner loop on the value n alone.
   table[1] == 0x77073096 and table[255] == 0x2D02EF8D.

3) crc32_table(data, crc=0) -> int
   Same results as crc32_bitwise but one table lookup per byte:
       crc = table[(crc ^ byte) & 0xFF] ^ (crc >> 8)
   Build the table ONCE (module level or cached), not per call. It must hash 2 MB in
   well under 3 seconds on plain CPython.

4) adler32(data, value=1) -> int
   a = value & 0xFFFF, b = value >> 16; for each byte: a = (a + byte) % 65521,
   b = (b + a) % 65521; result (b << 16) | a. Chaining works like zlib.adler32.
   Optimisation (required for the speed test): you do NOT need the modulo on every
   byte -- process the data in blocks of at most 5552 bytes and reduce once per
   block (5552 is the largest n for which b cannot overflow 32 bits; Python ints
   don't overflow, but taking the modulo less often is what makes it fast).

5) find_crc_collision_bytes(target_crc, prefix) -> bytes of length 4
   Return 4 bytes X such that crc32_table(prefix + X) == target_crc.
   CRC is linear, so this is solvable without brute force: run the CRC "backwards"
   from target_crc through 4 bytes using the inverse table (for each table entry,
   its top byte is unique, so you can tell which entry was XORed in).
   Hint: work with the raw register (the CRC before the final XOR). The 256 top bytes
   table[i] >> 24 are all different, so build rev[top_byte] = i. Start from
   reg = target ^ 0xFFFFFFFF and undo 4 forward steps: each step look up
   i = rev[reg >> 24] and compute reg = ((reg ^ table[i]) << 8 | i) & 0xFFFFFFFF.
   Then XOR the result with the prefix's forward register
   (crc32_table(prefix) ^ 0xFFFFFFFF) and emit those 32 bits as 4 bytes -- think
   about which byte order the forward loop consumes them in. Check your answer
   with crc32_table.

Run: python3 crc32_adler32.py
"""

POLY = 0xEDB88320


def crc32_bitwise(data, crc=0):
    crc ^= 0xFFFFFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ POLY
            else:
                crc >>= 1
    return crc ^ 0xFFFFFFFF


def make_crc_table():
    table = []
    for n in range(256):
        c = n
        for _ in range(8):
            c = (c >> 1) ^ POLY if c & 1 else c >> 1
        table.append(c)
    return table


_CRC_TABLE = make_crc_table()
_CRC_REV = {v >> 24: i for i, v in enumerate(_CRC_TABLE)}


def crc32_table(data, crc=0):
    table = _CRC_TABLE
    crc ^= 0xFFFFFFFF
    for byte in data:
        crc = table[(crc ^ byte) & 0xFF] ^ (crc >> 8)
    return crc ^ 0xFFFFFFFF


def adler32(data, value=1):
    MOD = 65521
    a, b = value & 0xFFFF, value >> 16
    view = memoryview(bytes(data))
    for start in range(0, len(view), 5552):
        for byte in view[start:start + 5552]:
            a += byte
            b += a
        a %= MOD
        b %= MOD
    return (b << 16) | a


def find_crc_collision_bytes(target_crc, prefix):
    table, rev = _CRC_TABLE, _CRC_REV
    assert len(rev) == 256
    reg = target_crc ^ 0xFFFFFFFF
    for _ in range(4):
        i = rev[reg >> 24]
        reg = (((reg ^ table[i]) << 8) | i) & 0xFFFFFFFF
    x = reg ^ (crc32_table(prefix) ^ 0xFFFFFFFF)
    return x.to_bytes(4, "little")          # the forward loop consumes the LOW byte first


def _run_tests():
    import random
    import time
    import zlib

    assert crc32_bitwise(b"") == 0
    assert crc32_bitwise(b"123456789") == 0xCBF43926       # the standard check value
    assert crc32_bitwise(b"The quick brown fox jumps over the lazy dog") == 0x414FA339

    t = make_crc_table()
    assert len(t) == 256 and t[0] == 0
    assert t[1] == 0x77073096 and t[255] == 0x2D02EF8D

    rng = random.Random(62)
    for n in [0, 1, 2, 3, 7, 64, 1000]:
        blob = bytes(rng.randrange(256) for _ in range(n))
        assert crc32_bitwise(blob) == zlib.crc32(blob), n
        assert crc32_table(blob) == zlib.crc32(blob), n
        assert adler32(blob) == zlib.adler32(blob), n
        cut = n // 3
        assert crc32_table(blob[cut:], crc32_table(blob[:cut])) == zlib.crc32(blob)
        assert adler32(blob[cut:], adler32(blob[:cut])) == zlib.adler32(blob)

    assert adler32(b"") == 1
    assert adler32(b"Wikipedia") == 0x11E60398
    assert adler32(b"\xff" * 20000) == zlib.adler32(b"\xff" * 20000)

    big = bytes(rng.randrange(256) for _ in range(2_000_000))
    t0 = time.perf_counter()
    assert crc32_table(big) == zlib.crc32(big)
    assert adler32(big) == zlib.adler32(big)
    elapsed = time.perf_counter() - t0
    assert elapsed < 3.0, f"too slow: {elapsed:.2f}s"

    for target, prefix in [(0, b""), (0xDEADBEEF, b"hello"), (0x12345678, bytes(range(50)))]:
        x = find_crc_collision_bytes(target, prefix)
        assert isinstance(x, bytes) and len(x) == 4
        assert crc32_table(prefix + x) == target, (hex(target), prefix, x)
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
