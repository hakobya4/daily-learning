"""
Day 20, Task 9 -- CS fundamentals: Bloom filter.

THE PROBLEM
------------
Implement a Bloom filter: a bit array of `size` bits and `num_hashes`
hash functions.

  BloomFilter(size, num_hashes)
  add(item: str)             set the item's bits
  might_contain(item: str)   False => definitely absent,
                             True  => probably present
  bits_set() -> int          number of bits currently set to 1

Rules: no false negatives, ever. Raise ValueError if size < 1 or
num_hashes < 1. Hashing must be deterministic across runs (do not use
Python's built-in hash(), it is salted per process).

HOW TO WORK THROUGH THIS
-------------------------
Derive num_hashes indexes per item, e.g. hashlib.sha256(f"{i}:{item}")
for i in range(num_hashes), converted to an int modulo size. Store the
bits in a bytearray or a Python int.

Run: python3 bloom_filter.py
"""

import hashlib


class BloomFilter:
    def __init__(self, size: int, num_hashes: int):
        if size < 1 or num_hashes < 1:
            raise ValueError("size and num_hashes must be >= 1")
        self.size = size
        self.num_hashes = num_hashes
        self._bits = bytearray(size)

    def _indexes(self, item: str):
        for i in range(self.num_hashes):
            digest = hashlib.sha256(f"{i}:{item}".encode()).digest()
            yield int.from_bytes(digest, "big") % self.size

    def add(self, item: str) -> None:
        for idx in self._indexes(item):
            self._bits[idx] = 1

    def might_contain(self, item: str) -> bool:
        return all(self._bits[idx] for idx in self._indexes(item))

    def bits_set(self) -> int:
        return sum(self._bits)


def _run_tests():
    for bad in ((0, 3), (10, 0)):
        try:
            BloomFilter(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
    bf = BloomFilter(10000, 3)
    assert bf.bits_set() == 0
    assert not bf.might_contain("anything")
    items = [f"item-{i}" for i in range(100)]
    for it in items:
        bf.add(it)
    assert all(bf.might_contain(it) for it in items)  # no false negatives
    assert 0 < bf.bits_set() <= 300
    false_pos = sum(bf.might_contain(f"other-{i}") for i in range(1000))
    assert false_pos < 50, false_pos
    tiny = BloomFilter(1, 1)
    tiny.add("x")
    assert tiny.might_contain("anything-at-all")  # saturated filter
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
