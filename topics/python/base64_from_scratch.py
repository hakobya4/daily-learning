"""
Day 61, Task 10 -- Python: Base64 / Base64url encoder and strict decoder from scratch (RFC 4648).

THE PROBLEM
------------
Implement Base64 with bit operations only -- do NOT import base64, binascii, codecs or
use bytes.hex()/int.from_bytes tricks. The tests compare against the base64 module.

ALPHABET     = "A-Z a-z 0-9 + /"      (standard, RFC 4648 section 4)
URL_ALPHABET = "A-Z a-z 0-9 - _"      (URL- and filename-safe, section 5)

1) b64encode(data: bytes, urlsafe=False, pad=True) -> str
   Take the input 3 bytes (24 bits) at a time and emit 4 six-bit characters. A final
   group of 1 byte gives 2 characters, 2 bytes give 3 characters; with pad=True append
   "=" so the output length is a multiple of 4 ("==" or "="). pad=False omits them
   (common in JWTs).

2) b64decode(text: str, urlsafe=False) -> bytes        -- STRICT:
   - padding is OPTIONAL: "TWE" and "TWE=" both decode to b"Ma";
   - but if present, "=" may only appear at the very end, at most 2 of them, and the
     total length WITH padding must then be a multiple of 4;
   - a data length (without padding) of 4k+1 is impossible -> invalid;
   - any character outside the selected alphabet -> invalid (no whitespace skipping;
     "+" is invalid in urlsafe mode and "-" is invalid in standard mode);
   - NON-CANONICAL encodings are invalid: the unused low bits of the last character
     must be zero. "TWE=" is the canonical encoding of b"Ma"; a lax decoder would also
     turn "TWF=" into b"Ma", but F (000101) leaves the bits 01 over -> invalid here.
   Raise ValueError for every invalid input.

3) b64_roundtrip_len(n) -> int   the padded encoded length for n input bytes
   (4 * ceil(n / 3)), using integer arithmetic only.

Hint: n = (b0 << 16) | (b1 << 8) | b2, then the four indices are (n >> 18) & 63,
(n >> 12) & 63, (n >> 6) & 63, n & 63. For decoding, build a dict char -> value once.

Run: python3 base64_from_scratch.py
"""

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
URL_ALPHABET = ALPHABET[:62] + "-_"


def b64encode(data, urlsafe=False, pad=True):
    raise NotImplementedError


def b64decode(text, urlsafe=False):
    raise NotImplementedError


def b64_roundtrip_len(n):
    raise NotImplementedError


def _run_tests():
    import base64
    import random

    # RFC 4648 section 10 test vectors
    vectors = [(b"", ""), (b"f", "Zg=="), (b"fo", "Zm8="), (b"foo", "Zm9v"),
               (b"foob", "Zm9vYg=="), (b"fooba", "Zm9vYmE="), (b"foobar", "Zm9vYmFy")]
    for raw, enc in vectors:
        assert b64encode(raw) == enc, (raw, b64encode(raw))
        assert b64decode(enc) == raw
        assert b64decode(enc.rstrip("=")) == raw          # padding optional
        assert b64encode(raw, pad=False) == enc.rstrip("=")

    assert b64encode(b"Ma") == "TWE="
    assert b64decode("TWE") == b"Ma"
    assert b64encode(b"\xfb\xff\xbf") == "+/+/"
    assert b64encode(b"\xfb\xff\xbf", urlsafe=True) == "-_-_"
    assert b64decode("-_-_", urlsafe=True) == b"\xfb\xff\xbf"

    invalid_std = ["Zg=", "Z", "Zm9vY", "Zg===", "Z=g=", "=Zg=", "Zm 9v", "Zm9v\n",
                   "-_-_", "Zg==Zg==", "Zh==", "Zm9=", "TWF", "TWF="]
    for bad in invalid_std:
        try:
            b64decode(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for %r" % bad)
    try:
        b64decode("+/+/", urlsafe=True)
    except ValueError:
        pass
    else:
        raise AssertionError("'+' must be invalid in urlsafe mode")

    rng = random.Random(61)
    for _ in range(500):
        raw = bytes(rng.randrange(256) for _ in range(rng.randint(0, 64)))
        assert b64encode(raw) == base64.b64encode(raw).decode()
        assert b64encode(raw, urlsafe=True) == base64.urlsafe_b64encode(raw).decode()
        assert b64decode(b64encode(raw)) == raw
        assert b64decode(b64encode(raw, urlsafe=True, pad=False), urlsafe=True) == raw
        assert len(b64encode(raw)) == b64_roundtrip_len(len(raw))
    for n, want in [(0, 0), (1, 4), (2, 4), (3, 4), (4, 8), (10 ** 12, 4 * (10 ** 12 // 3 + 1))]:
        assert b64_roundtrip_len(n) == want, n
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
