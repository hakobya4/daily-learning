"""
Day 29, Task 10 -- CS fundamentals: Huffman coding (greedy + heap).

THE PROBLEM
------------
Implement:
  huffman_codes(text) -> dict {char: bitstring}
      Build the Huffman tree with a min-heap of (frequency, ...) nodes and
      return the prefix code for each distinct character. Special case: if
      text has only ONE distinct character, its code is "0". Empty text
      returns {}.
  encode(text, codes) -> str     concatenated bitstring
  decode(bits, codes) -> str     inverse of encode

The exact codes depend on tie-breaking, so the tests check PROPERTIES:
  * prefix-free (no code is a prefix of another)
  * decode(encode(text)) == text
  * total encoded length equals the known optimum for the sample

  "aaaabbc" -> frequencies a:4 b:2 c:1 -> optimal cost = 4*1 + 2*2 + 1*2 = 10 bits

HOW TO WORK THROUGH THIS
-------------------------
Heap entries (freq, tiebreak_counter, tree) where tree is either a char or a
(left, right) tuple -- the counter stops Python comparing trees on ties.
Repeatedly pop two, push their merge with summed frequency. Then walk the
final tree, appending "0" going left and "1" going right.

Run: python3 huffman_coding.py
"""


def huffman_codes(text: str) -> dict:
    raise NotImplementedError


def encode(text: str, codes: dict) -> str:
    raise NotImplementedError


def decode(bits: str, codes: dict) -> str:
    raise NotImplementedError


def _run_tests():
    assert huffman_codes("") == {}
    assert huffman_codes("zzzz") == {"z": "0"}

    text = "aaaabbc"
    codes = huffman_codes(text)
    assert set(codes) == {"a", "b", "c"}
    vals = list(codes.values())
    for i, x in enumerate(vals):
        for j, y in enumerate(vals):
            assert i == j or not y.startswith(x), "codes must be prefix-free"
    bits = encode(text, codes)
    assert len(bits) == 10
    assert decode(bits, codes) == text

    text = "this is an example of a huffman tree"
    codes = huffman_codes(text)
    bits = encode(text, codes)
    assert decode(bits, codes) == text
    assert len(bits) == 135  # known optimum for this classic sample
    assert len(codes[" "]) <= len(codes["x"])  # frequent chars never longer
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
