"""
Day 41, Task 1 -- Python: run-length encoding.

THE PROBLEM
------------
rle_encode(s) -> compress runs of the same character as <count><char>.
A run of length 1 is still written with its count: "aabccc" -> "2a1b3c".
rle_decode(t) -> the inverse; counts can be multi-digit ("12x" -> 12 x's).
Empty string maps to empty string. Input to encode never contains digits.

Run: python3 rle_codec.py
"""


def rle_encode(s: str) -> str:
    raise NotImplementedError


def rle_decode(t: str) -> str:
    raise NotImplementedError


def _run_tests():
    assert rle_encode("") == ""
    assert rle_encode("aabccc") == "2a1b3c"
    assert rle_encode("z") == "1z"
    assert rle_encode("x" * 12) == "12x"
    assert rle_decode("2a1b3c") == "aabccc"
    assert rle_decode("12x") == "x" * 12
    assert rle_decode("") == ""
    for s in ["", "abc", "aaabbbcccd", "  ,,!!", "q" * 100 + "w"]:
        assert rle_decode(rle_encode(s)) == s
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
