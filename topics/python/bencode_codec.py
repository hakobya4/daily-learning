"""
Day 63, Task 1 -- Python: a strict Bencode encoder and decoder (the BitTorrent format).

THE PROBLEM
------------
.torrent files and the BitTorrent tracker protocol use "bencoding", a tiny format with
exactly four kinds of values. Implement it from scratch (no third-party libraries).

    integer      i<decimal>e        i42e   i-7e   i0e
    byte string  <length>:<bytes>   4:spam   0:
    list         l<items>e          l4:spami42ee        == [b"spam", 42]
    dictionary   d<key><value>...e  d3:cow3:moo4:spam4:eggse
                                    == {b"cow": b"moo", b"spam": b"eggs"}

1) bencode(value) -> bytes
   Accepts int (NOT bool -- True is an int subclass, reject it), bytes, str (encode it as
   UTF-8 first), list/tuple, and dict whose keys are bytes or str. Dictionary keys must be
   written in SORTED order of their raw bytes (compare the UTF-8 encoded keys, so b"Z"
   sorts before b"a"). Two keys that encode to the same bytes (e.g. "a" and b"a") are an
   error. Anything else (float, None, set, bool, ...) -> raise TypeError.

2) bdecode(data: bytes) -> value
   Returns ints, bytes (never str), lists and dicts with bytes keys. STRICT: raise
   BencodeError (a ValueError subclass, already defined) for any of these:
     - empty input, unknown leading byte, or trailing bytes after one complete value
     - integers: "i-0e", leading zeros ("i03e", "i-03e"), "ie", "i-e", missing 'e',
       non-digits ("i1.5e")
     - strings: leading zeros in the length ("03:abc" -- but "0:" is fine), a length that
       runs past the end of the input, a missing ':'
     - lists/dicts that are never closed with 'e'
     - dictionary keys that are not byte strings, keys not in strictly increasing raw-byte
       order (this also rejects duplicate keys)
   Must not use recursion depth proportional to input length for flat data, and should
   handle nesting of at least 500 levels ("l"*500 + "e"*500) without RecursionError.
   (Hint: an explicit stack of containers being built is the cleanest approach; a
   recursive descent parser also passes if you raise the limit carefully -- prefer
   the stack.)

3) info_hash_hex(torrent: bytes) -> str
   A torrent's identity is the SHA-1 of the EXACT bytes of the value stored under the
   top-level key b"info". Return it as lowercase hex. Do NOT decode and re-encode -- a
   non-canonical file would hash differently; find the byte span of that value instead.
   (Hint: have your decoder record (start, end) offsets for top-level dict values, or
   write a small helper `_skip(data, pos) -> end_pos` that walks one value.)
   Raise BencodeError if the input is not a dict or has no b"info" key.

Run: python3 bencode_codec.py
"""


class BencodeError(ValueError):
    pass


def bencode(value):
    raise NotImplementedError


def bdecode(data):
    raise NotImplementedError


def info_hash_hex(torrent):
    raise NotImplementedError


def _run_tests():
    import hashlib
    import random

    # --- encoding ---
    assert bencode(42) == b"i42e"
    assert bencode(-7) == b"i-7e"
    assert bencode(0) == b"i0e"
    assert bencode(b"spam") == b"4:spam"
    assert bencode("") == b"0:"
    assert bencode("hé") == b"3:h\xc3\xa9"          # length counts BYTES
    assert bencode([b"spam", 42]) == b"l4:spami42ee"
    assert bencode((1, (2,))) == b"li1eli2eee"
    assert bencode({"spam": b"eggs", b"cow": "moo"}) == b"d3:cow3:moo4:spam4:eggse"
    assert bencode({"a": 1, "Z": 2, "aa": 3, "": 0}) == b"d0:i0e1:Zi2e1:ai1e2:aai3ee"
    for bad in (1.5, None, True, {1, 2}, {1: b"x"}, object()):
        try:
            bencode(bad)
        except TypeError:
            pass
        else:
            raise AssertionError(f"bencode should reject {bad!r}")
    try:
        bencode({"a": 1, b"a": 2})
    except (TypeError, ValueError):
        pass
    else:
        raise AssertionError("duplicate encoded keys must be rejected")

    # --- decoding ---
    assert bdecode(b"i42e") == 42
    assert bdecode(b"i-7e") == -7
    assert bdecode(b"i0e") == 0
    assert bdecode(b"0:") == b""
    assert bdecode(b"4:spam") == b"spam"
    assert bdecode(b"l4:spami42ee") == [b"spam", 42]
    assert bdecode(b"le") == []
    assert bdecode(b"de") == {}
    assert bdecode(b"d3:cow3:moo4:spam4:eggse") == {b"cow": b"moo", b"spam": b"eggs"}
    assert bdecode(b"d4:listli1eli2eee3:numi9ee") == {b"list": [1, [2]], b"num": 9}
    assert bdecode(b"10:0123456789") == b"0123456789"
    assert bdecode(b"5:a:b:c") == b"a:b:c"

    bad_inputs = [
        b"", b"x", b"i42", b"ie", b"i-e", b"i-0e", b"i03e", b"i-03e", b"i1.5e", b"i4 2e",
        b"03:abc", b"5:abc", b"3abc", b"-1:a", b"l", b"li1e", b"d", b"d1:a", b"d1:ai1e",
        b"di1ei2ee", b"d1:bi1e1:ai2ee", b"d1:ai1e1:ai2ee", b"i1ei2e", b"4:spamx", b"le ",
        b"l4:spam", b"dle", b"d1:al", b"e",
    ]
    for bad in bad_inputs:
        try:
            bdecode(bad)
        except BencodeError:
            pass
        except Exception as exc:  # pragma: no cover
            raise AssertionError(f"{bad!r}: expected BencodeError, got {type(exc).__name__}")
        else:
            raise AssertionError(f"bdecode should reject {bad!r}")
    assert issubclass(BencodeError, ValueError)

    deep = b"l" * 500 + b"e" * 500
    v = bdecode(deep)
    for _ in range(499):
        assert len(v) == 1
        v = v[0]
    assert v == []

    flat = b"l" + b"i1e" * 100000 + b"e"
    assert bdecode(flat) == [1] * 100000

    # round trips on random structures
    rng = random.Random(63)

    def rand_value(depth=0):
        kind = rng.randrange(4 if depth < 4 else 2)
        if kind == 0:
            return rng.randint(-10**20, 10**20)
        if kind == 1:
            return bytes(rng.randrange(256) for _ in range(rng.randrange(12)))
        if kind == 2:
            return [rand_value(depth + 1) for _ in range(rng.randrange(5))]
        return {bytes(rng.randrange(97, 123) for _ in range(rng.randrange(1, 4))): rand_value(depth + 1)
                for _ in range(rng.randrange(5))}

    for _ in range(300):
        val = rand_value()
        enc = bencode(val)
        assert bdecode(enc) == val
        assert bencode(bdecode(enc)) == enc

    # --- info hash over the raw span ---
    info = b"d6:lengthi1024e4:name8:file.bin12:piece lengthi16384ee"
    torrent = b"d8:announce18:http://tracker/ann7:comment2:hi4:info" + info + b"e"
    assert bdecode(torrent)[b"info"][b"name"] == b"file.bin"
    assert info_hash_hex(torrent) == hashlib.sha1(info).hexdigest()
    # a non-canonical-looking but valid integer form inside info still hashes as-is
    info2 = b"d1:xli1ei-5ee1:y0:e"
    t2 = b"d4:info" + info2 + b"4:zzzzi1ee"
    assert info_hash_hex(t2) == hashlib.sha1(info2).hexdigest()
    for bad in (b"li1ee", b"d4:name1:xe", b"i1e"):
        try:
            info_hash_hex(bad)
        except BencodeError:
            pass
        else:
            raise AssertionError(f"info_hash_hex should reject {bad!r}")

    print("all bencode tests passed")


if __name__ == "__main__":
    _run_tests()
