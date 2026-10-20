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
    import heapq
    from collections import Counter
    if not text:
        return {}
    freq = Counter(text)
    if len(freq) == 1:
        return {next(iter(freq)): "0"}
    heap = [(f, i, ch) for i, (ch, f) in enumerate(sorted(freq.items()))]
    heapq.heapify(heap)
    counter = len(heap)
    while len(heap) > 1:
        f1, _, t1 = heapq.heappop(heap)
        f2, _, t2 = heapq.heappop(heap)
        heapq.heappush(heap, (f1 + f2, counter, (t1, t2)))
        counter += 1
    codes = {}
    stack = [(heap[0][2], "")]
    while stack:
        tree, prefix = stack.pop()
        if isinstance(tree, tuple):
            stack.append((tree[0], prefix + "0"))
            stack.append((tree[1], prefix + "1"))
        else:
            codes[tree] = prefix
    return codes


def encode(text: str, codes: dict) -> str:
    return "".join(codes[ch] for ch in text)


def decode(bits: str, codes: dict) -> str:
    inverse = {code: ch for ch, code in codes.items()}
    out = []
    cur = ""
    for b in bits:
        cur += b
        if cur in inverse:
            out.append(inverse[cur])
            cur = ""
    return "".join(out)


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
