"""
Day 8, Task 7 -- CS fundamentals: hash table from scratch (separate chaining).

THE PROBLEM
------------
Implement a HashTable class with:
  - put(key, value) -> None       -- insert, or overwrite if key exists
  - get(key) -> value             -- return the value, raise KeyError
                                      if key isn't present
  - delete(key) -> None           -- remove key, raise KeyError if it
                                      isn't present
  - __contains__(key) -> bool     -- so `key in table` works
  - __len__() -> int              -- number of keys currently stored

Use SEPARATE CHAINING for collisions: `self.buckets` is a fixed-size
list, and each bucket is itself a small list of [key, value] pairs.
Take `num_buckets` in __init__ (default something small, e.g. 8) --
this is a from-scratch exercise, so no dict-based shortcuts for the
actual storage: the point is understanding what a dict gives you "for
free" underneath.

HOW TO WORK THROUGH THIS
-------------------------
A private helper `_bucket_index(key)` -- something like
`hash(key) % self.num_buckets` -- picks which bucket a key belongs in
(Python's built-in hash() is fine to build on here; you're not
implementing the hash function itself, just the table structure around
it). Every other method starts by finding that bucket, then does a
short LINEAR SCAN through the (small) list of pairs in it:
  - put: scan for a pair with a matching key to overwrite; if none
    found, append a new [key, value] pair.
  - get / delete / __contains__: scan for a matching key; get raises
    KeyError if the scan finishes without finding one, and so does
    delete.
Keep a running count for __len__ rather than recomputing it by summing
bucket lengths every time (though either approach works).

Run: python3 hash_table.py
"""


class HashTable:
    def __init__(self, num_buckets: int = 8):
        self.num_buckets = num_buckets
        self.buckets = [[] for _ in range(num_buckets)]

    def _bucket_index(self, key) -> int:
        # TODO: hash(key) % self.num_buckets
        raise NotImplementedError

    def put(self, key, value) -> None:
        # TODO: find the bucket, overwrite a matching key's value if
        # present, otherwise append a new [key, value] pair.
        raise NotImplementedError

    def get(self, key):
        # TODO: scan the bucket for a matching key; raise KeyError if
        # not found.
        raise NotImplementedError

    def delete(self, key) -> None:
        # TODO: scan the bucket for a matching key and remove it;
        # raise KeyError if not found.
        raise NotImplementedError

    def __contains__(self, key) -> bool:
        # TODO: True if a matching key is present, else False.
        raise NotImplementedError

    def __len__(self) -> int:
        # TODO: number of keys currently stored.
        raise NotImplementedError


def _run_tests() -> None:
    # deliberately few buckets with several keys -- FORCES collisions,
    # so this only actually proves chaining works if buckets really
    # do end up holding more than one pair.
    ht = HashTable(num_buckets=4)
    keys = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta"]
    for i, k in enumerate(keys):
        ht.put(k, i)

    assert len(ht) == 6, len(ht)
    bucket_sizes = [len(b) for b in ht.buckets]
    assert max(bucket_sizes) > 1, (
        f"expected at least one collision with 6 keys in 4 buckets, "
        f"got bucket sizes {bucket_sizes}"
    )

    for i, k in enumerate(keys):
        assert ht.get(k) == i, (k, ht.get(k))
        assert k in ht

    # overwrite an existing key -- value changes, length doesn't
    ht.put("alpha", 100)
    assert ht.get("alpha") == 100
    assert len(ht) == 6

    # delete, then confirm it's really gone
    ht.delete("beta")
    assert "beta" not in ht
    assert len(ht) == 5
    try:
        ht.get("beta")
        assert False, "expected KeyError after delete"
    except KeyError:
        pass

    try:
        ht.get("never-inserted")
        assert False, "expected KeyError for a key never inserted"
    except KeyError:
        pass

    try:
        ht.delete("never-inserted")
        assert False, "expected KeyError deleting a key never inserted"
    except KeyError:
        pass

    print("All hash_table tests passed.")


if __name__ == "__main__":
    _run_tests()
