"""
Day 61, Task 4 -- CS fundamentals: Burrows-Wheeler transform + move-to-front (the core of bzip2).

THE PROBLEM
------------
BWT doesn't compress anything by itself -- it REORDERS a string so equal characters
cluster together, which move-to-front + run-length/entropy coding then exploit.

1) bwt(s) -> (last_column: str, index: int)
   Build all len(s) cyclic rotations of s, sort them lexicographically (plain Python
   string order), and return the string made of the LAST character of every sorted
   rotation, plus the position (0-based) of the ORIGINAL s in the sorted list.
   bwt("banana") -> ("nnbaaa", 3)
   (sorted rotations: abanan, anaban, ananab, banana, nabana, nanaba)
   Identical rotations (s = "abab") are fine: use a STABLE sort of the rotation start
   positions and report the first position whose rotation equals s.
   bwt("") -> ("", 0).

2) inverse_bwt(last, index) -> str
   Recover s from (last, index) WITHOUT rebuilding the rotation table (that's O(n^2 log n)
   and won't pass the big test). Use the LF-mapping:
     - first = sorted(last);
     - the k-th occurrence of character c in `last` is the same text character as the
       k-th occurrence of c in `first`;
     - build next/prev pointer arrays from that, then walk n steps starting from `index`.
   Must handle n = 200_000 in a couple of seconds (O(n log n) or O(n) with counting).

3) mtf_encode(s, alphabet) -> list[int]  /  mtf_decode(codes, alphabet) -> str
   Move-to-front: keep a list initialised to `alphabet` (a string of distinct chars);
   for each character output its current index in the list, then move it to the front.
   mtf_encode("nnbaaa", "abn") -> [2, 0, 2, 2, 0, 0]
   Raise ValueError if a character is not in the alphabet (encode) or a code is out of
   range (decode).

Note for the big test: bwt() itself may use the simple "sort rotation indices with
key=lambda i: s[i:] + s[:i]" approach -- only inverse_bwt must be fast.

Run: python3 bwt_mtf_codec.py
"""


def bwt(s):
    raise NotImplementedError


def inverse_bwt(last, index):
    raise NotImplementedError


def mtf_encode(s, alphabet):
    raise NotImplementedError


def mtf_decode(codes, alphabet):
    raise NotImplementedError


def _run_tests():
    import random
    import time

    assert bwt("banana") == ("nnbaaa", 3)
    assert bwt("") == ("", 0)
    assert bwt("a") == ("a", 0)
    assert bwt("abab") == ("bbaa", 0)
    assert bwt("mississippi") == ("pssmipissii", 4)
    assert bwt("aaaa") == ("aaaa", 0)

    for s in ["banana", "", "a", "abab", "mississippi", "aaaa", "abracadabra",
              "the quick brown fox jumps over the lazy dog", "zyxwvu"]:
        last, idx = bwt(s)
        assert sorted(last) == sorted(s)
        assert inverse_bwt(last, idx) == s, s

    rng = random.Random(61)
    for _ in range(300):
        s = "".join(rng.choice("abc") for _ in range(rng.randint(0, 30)))
        assert inverse_bwt(*bwt(s)) == s, s

    # inverse_bwt must be fast: build a valid (last, index) pair for a long string
    # directly from a suffix-sorted, sentinel-terminated text (no O(n^2) rotations).
    n = 200_000
    body = "".join(rng.choice("ACGT") for _ in range(n - 1))
    s = body + "\x00"                      # unique smallest sentinel at the end
    # Random 200k DNA has no repeated 64-char substring (with overwhelming probability),
    # so sorting by the first 64 chars already gives the true suffix (= rotation) order.
    sa = sorted(range(len(s)), key=lambda i: s[i:i + 64])
    assert all(s[a:a + 64] != s[b:b + 64] for a, b in zip(sa, sa[1:]))
    last = "".join(s[i - 1] for i in sa)
    idx = sa.index(0)
    t0 = time.time()
    assert inverse_bwt(last, idx) == s
    assert time.time() - t0 < 5, "inverse_bwt too slow"

    assert mtf_encode("nnbaaa", "abn") == [2, 0, 2, 2, 0, 0]
    assert mtf_decode([2, 0, 2, 2, 0, 0], "abn") == "nnbaaa"
    assert mtf_encode("", "ab") == []
    assert mtf_encode("bbbb", "ab") == [1, 0, 0, 0]
    assert mtf_encode("abcabc", "abc") == [0, 1, 2, 2, 2, 2]
    for _ in range(200):
        alpha = "abcdefgh"
        s = "".join(rng.choice(alpha[:rng.randint(1, 8)]) for _ in range(rng.randint(0, 40)))
        codes = mtf_encode(s, alpha)
        assert all(0 <= c < len(alpha) for c in codes)
        assert mtf_decode(codes, alpha) == s
    # BWT output clusters characters -> MTF produces lots of zeros
    text = "abracadabra " * 50
    zeros_plain = mtf_encode(text, "abcdr ").count(0)
    zeros_bwt = mtf_encode(bwt(text)[0], "abcdr ").count(0)
    assert zeros_bwt > 2 * zeros_plain, (zeros_plain, zeros_bwt)
    for bad in (lambda: mtf_encode("abz", "ab"), lambda: mtf_decode([0, 5], "ab"),
                lambda: mtf_decode([-1], "ab")):
        try:
            bad()
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
