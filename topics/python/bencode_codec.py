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
    out = []

    def key_bytes(k):
        if isinstance(k, bytes):
            return k
        if isinstance(k, str):
            return k.encode("utf-8")
        raise TypeError(f"dict key must be bytes or str, not {type(k).__name__}")

    # explicit work stack: items are either values to encode or raw bytes to emit
    stack = [value]
    while stack:
        v = stack.pop()
        if isinstance(v, _Raw):
            out.append(v.b)
        elif isinstance(v, bool):
            raise TypeError("bool is not bencodable")
        elif isinstance(v, int):
            out.append(b"i%de" % v)
        elif isinstance(v, (bytes, bytearray)):
            out.append(b"%d:" % len(v) + bytes(v))
        elif isinstance(v, str):
            b = v.encode("utf-8")
            out.append(b"%d:" % len(b) + b)
        elif isinstance(v, (list, tuple)):
            out.append(b"l")
            stack.append(_Raw(b"e"))
            stack.extend(reversed(v))
        elif isinstance(v, dict):
            items = []
            seen = set()
            for k, val in v.items():
                kb = key_bytes(k)
                if kb in seen:
                    raise ValueError(f"duplicate dictionary key {kb!r}")
                seen.add(kb)
                items.append((kb, val))
            items.sort(key=lambda kv: kv[0])
            out.append(b"d")
            stack.append(_Raw(b"e"))
            for kb, val in reversed(items):
                stack.append(val)
                stack.append(_Raw(b"%d:" % len(kb) + kb))
        else:
            raise TypeError(f"cannot bencode {type(v).__name__}")
    return b"".join(out)


class _Raw:
    __slots__ = ("b",)

    def __init__(self, b):
        self.b = b


def _parse_int(data, pos):
    """data[pos] == 'i'. Returns (value, new_pos)."""
    end = data.find(b"e", pos + 1)
    if end == -1:
        raise BencodeError("unterminated integer")
    body = data[pos + 1:end]
    neg = body.startswith(b"-")
    digits = body[1:] if neg else body
    if not digits or not digits.isdigit() or not all(48 <= c <= 57 for c in digits):
        raise BencodeError(f"bad integer {body!r}")
    if len(digits) > 1 and digits[0:1] == b"0":
        raise BencodeError("leading zero in integer")
    if neg and digits == b"0":
        raise BencodeError("negative zero")
    return int(body), end + 1


def _parse_str(data, pos):
    colon = data.find(b":", pos)
    if colon == -1:
        raise BencodeError("missing ':' in string")
    ln = data[pos:colon]
    if not ln or not all(48 <= c <= 57 for c in ln):
        raise BencodeError(f"bad string length {ln!r}")
    if len(ln) > 1 and ln[0:1] == b"0":
        raise BencodeError("leading zero in string length")
    n = int(ln)
    start = colon + 1
    if start + n > len(data):
        raise BencodeError("string runs past end of input")
    return data[start:start + n], start + n


def _decode(data, pos=0, spans=None):
    """Decode one value starting at pos. Returns (value, end).
    If spans is a dict, records top-level dict key -> (start, end) of its value."""
    n = len(data)
    if pos >= n:
        raise BencodeError("unexpected end of input")
    # stack entries: [container, pending_key_or_None, last_key, value_start]
    stack = []
    result = None
    done = False
    while True:
        if pos >= n:
            raise BencodeError("unexpected end of input")
        c = data[pos]
        if c == 0x65:  # 'e'
            if not stack:
                raise BencodeError("unexpected 'e'")
            frame = stack.pop()
            if isinstance(frame[0], dict) and frame[1] is not None:
                raise BencodeError("dictionary key without value")
            pos += 1
            value = frame[0]
        elif c == 0x6C:  # 'l'
            stack.append([[], None, None, pos])
            pos += 1
            continue
        elif c == 0x64:  # 'd'
            stack.append([{}, None, None, pos])
            pos += 1
            continue
        elif c == 0x69:  # 'i'
            vstart = pos
            value, pos = _parse_int(data, pos)
        elif 48 <= c <= 57:
            vstart = pos
            value, pos = _parse_str(data, pos)
        else:
            raise BencodeError(f"unexpected byte {bytes([c])!r} at {pos}")

        # attach value to parent
        if not stack:
            return value, pos
        parent = stack[-1]
        cont = parent[0]
        if isinstance(cont, list):
            cont.append(value)
        else:
            if parent[1] is None:
                if not isinstance(value, bytes):
                    raise BencodeError("dictionary key must be a byte string")
                if parent[2] is not None and not (value > parent[2]):
                    raise BencodeError("dictionary keys not in strictly increasing order")
                parent[1] = value
                parent[3] = pos  # value starts right after the key
            else:
                key = parent[1]
                cont[key] = value
                if spans is not None and len(stack) == 1:
                    spans[key] = (parent[3], pos)
                parent[2] = key
                parent[1] = None


def bdecode(data):
    data = bytes(data)
    if not data:
        raise BencodeError("empty input")
    value, end = _decode(data, 0)
    if end != len(data):
        raise BencodeError("trailing bytes after value")
    return value


def info_hash_hex(torrent):
    import hashlib
    data = bytes(torrent)
    if not data:
        raise BencodeError("empty input")
    spans = {}
    value, end = _decode(data, 0, spans)
    if end != len(data):
        raise BencodeError("trailing bytes after value")
    if not isinstance(value, dict):
        raise BencodeError("torrent is not a dictionary")
    if b"info" not in spans:
        raise BencodeError("no info key")
    s, e = spans[b"info"]
    return hashlib.sha1(data[s:e]).hexdigest()


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
