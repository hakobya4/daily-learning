"""
Day 63, Task 10 -- Python: consistent hashing -- a hash ring with virtual nodes and
replica lookup, plus Google's "jump consistent hash".

THE PROBLEM
------------
With `node = hash(key) % N`, adding one server remaps almost every key. Consistent
hashing remaps only ~1/(N+1) of them. Implement two classic schemes.

Use the provided ring_hash() for EVERY position on the ring (keys and virtual nodes),
so results are deterministic across runs (Python's built-in hash() is salted per process).

1) class HashRing(vnodes=100)
   - add_node(name): place `vnodes` points on the ring at ring_hash(f"{name}#{i}") for
     i in range(vnodes). Adding a node that is already present -> ValueError.
   - remove_node(name): remove all of its points; unknown node -> KeyError.
   - nodes() -> sorted list of node names.
   - get_node(key) -> name: h = ring_hash(key); the owner is the node of the FIRST point
     whose position is >= h, wrapping around to the smallest point if there is none.
     Empty ring -> LookupError. Must be O(log P) per lookup (P = number of points):
     keep a SORTED list of positions and use the bisect module -- do not scan.
     (If two points ever had the same position, the one from the node added first wins;
     with a 64-bit hash this will not happen in the tests.)
   - get_nodes(key, n) -> list of up to n DISTINCT node names for replication: walk
     clockwise from the owner's point, skipping nodes already chosen, until you have n
     (or every node). The first element is get_node(key).
   Keep add/remove at O(P) or better per call (re-sorting the list is fine;
   bisect.insort per point is fine).

2) jump_hash(key: int, num_buckets: int) -> int in [0, num_buckets)
   Lamping & Veach (2014), with 64-bit unsigned arithmetic emulated by masking:
       b, j = -1, 0
       while j < num_buckets:
           b = j
           key = (key * 2862933555777941757 + 1) mod 2**64
           j = int((b + 1) * (2**31 / ((key >> 33) + 1)))      # float division
       return b
   num_buckets < 1 -> ValueError; key must be a non-negative int (mask it to 64 bits
   first: key & (2**64 - 1)).
   Property to understand (and that the tests check): when num_buckets grows from n to
   n + 1, a key either keeps its bucket or moves to the NEW bucket n -- never elsewhere.

Run: python3 consistent_hash_ring.py
"""

import bisect
import hashlib


def ring_hash(s):
    """Position on the ring: first 8 bytes of MD5(s) as a big-endian unsigned int."""
    return int.from_bytes(hashlib.md5(s.encode("utf-8")).digest()[:8], "big")


class HashRing:
    def __init__(self, vnodes=100):
        if vnodes < 1:
            raise ValueError("vnodes must be >= 1")
        self.vnodes = vnodes
        self._order = {}        # name -> insertion sequence number (tie-breaker)
        self._seq = 0
        self._points = []       # sorted list of (position, seq, name)
        self._positions = []    # parallel sorted list of positions for bisect

    def _rebuild_positions(self):
        self._positions = [p for p, _, _ in self._points]

    def add_node(self, name):
        if name in self._order:
            raise ValueError(f"node {name!r} already present")
        seq = self._seq
        self._seq += 1
        self._order[name] = seq
        self._points.extend((ring_hash(f"{name}#{i}"), seq, name) for i in range(self.vnodes))
        self._points.sort()
        self._rebuild_positions()

    def remove_node(self, name):
        if name not in self._order:
            raise KeyError(name)
        del self._order[name]
        self._points = [pt for pt in self._points if pt[2] != name]
        self._rebuild_positions()

    def nodes(self):
        return sorted(self._order)

    def _start_index(self, key):
        if not self._points:
            raise LookupError("hash ring is empty")
        i = bisect.bisect_left(self._positions, ring_hash(key))
        return 0 if i == len(self._positions) else i

    def get_node(self, key):
        return self._points[self._start_index(key)][2]

    def get_nodes(self, key, n):
        if n <= 0:
            return []
        start = self._start_index(key)
        want = min(n, len(self._order))
        out, seen = [], set()
        total = len(self._points)
        for off in range(total):
            name = self._points[(start + off) % total][2]
            if name not in seen:
                seen.add(name)
                out.append(name)
                if len(out) == want:
                    break
        return out


def jump_hash(key, num_buckets):
    if num_buckets < 1:
        raise ValueError("num_buckets must be >= 1")
    if not isinstance(key, int) or key < 0:
        raise ValueError("key must be a non-negative int")
    mask = (1 << 64) - 1
    key &= mask
    b, j = -1, 0
    while j < num_buckets:
        b = j
        key = (key * 2862933555777941757 + 1) & mask
        j = int((b + 1) * (float(1 << 31) / ((key >> 33) + 1)))
    return b


def _brute_owner(node_names, vnodes, key):
    """Reference owner by brute force over all points (used only by the tests)."""
    pts = sorted((ring_hash(f"{nd}#{i}"), nd) for nd in node_names for i in range(vnodes))
    h = ring_hash(key)
    for pos, nd in pts:
        if pos >= h:
            return nd
    return pts[0][1]


def _run_tests():
    import time

    ring = HashRing(vnodes=50)
    try:
        ring.get_node("x")
    except LookupError:
        pass
    else:
        raise AssertionError("empty ring must raise LookupError")
    for nd in ("alpha", "beta", "gamma", "delta"):
        ring.add_node(nd)
    assert ring.nodes() == ["alpha", "beta", "delta", "gamma"]
    try:
        ring.add_node("beta")
    except ValueError:
        pass
    else:
        raise AssertionError("duplicate node must raise ValueError")
    try:
        ring.remove_node("omega")
    except KeyError:
        pass
    else:
        raise AssertionError("unknown node must raise KeyError")

    keys = [f"user:{i}" for i in range(3000)]
    names = ["alpha", "beta", "gamma", "delta"]
    for k in keys[:400]:
        assert ring.get_node(k) == _brute_owner(names, 50, k), k

    # replicas
    for k in keys[:300]:
        reps = ring.get_nodes(k, 3)
        assert len(reps) == 3 and len(set(reps)) == 3 and reps[0] == ring.get_node(k)
        assert ring.get_nodes(k, 1) == [reps[0]]
        assert sorted(ring.get_nodes(k, 10)) == sorted(names)
    assert ring.get_nodes("user:7", 0) == []

    # adding a node only moves keys TO the new node, and about 1/5 of them
    before = {k: ring.get_node(k) for k in keys}
    ring.add_node("epsilon")
    after = {k: ring.get_node(k) for k in keys}
    moved = [k for k in keys if before[k] != after[k]]
    assert all(after[k] == "epsilon" for k in moved)
    assert 0.10 < len(moved) / len(keys) < 0.32, len(moved) / len(keys)
    for k in keys[:200]:
        assert after[k] == _brute_owner(names + ["epsilon"], 50, k)

    # removing it again restores exactly the old mapping
    ring.remove_node("epsilon")
    assert all(ring.get_node(k) == before[k] for k in keys)
    assert ring.nodes() == sorted(names)

    # removing a node only moves ITS keys
    ring.remove_node("gamma")
    for k in keys:
        if before[k] != "gamma":
            assert ring.get_node(k) == before[k]
        else:
            assert ring.get_node(k) != "gamma"

    # with many virtual nodes the load is reasonably balanced
    big = HashRing(vnodes=200)
    for i in range(10):
        big.add_node(f"node-{i}")
    load = {}
    for i in range(50000):
        nd = big.get_node(f"obj-{i}")
        load[nd] = load.get(nd, 0) + 1
    assert len(load) == 10
    assert max(load.values()) / min(load.values()) < 1.5, load

    # lookups must be logarithmic
    huge = HashRing(vnodes=100)
    for i in range(100):
        huge.add_node(f"n{i}")
    t0 = time.perf_counter()
    for i in range(100000):
        huge.get_node(f"k{i}")
    assert time.perf_counter() - t0 < 3.0, "get_node is too slow -- use bisect"

    # --- jump consistent hash ---
    for bad in (0, -3):
        try:
            jump_hash(1, bad)
        except ValueError:
            pass
        else:
            raise AssertionError("num_buckets < 1 must raise ValueError")
    assert all(jump_hash(k, 1) == 0 for k in range(100))
    # key 0: after one LCG step key == 1, so (key >> 33) == 0 and j jumps past any n
    assert jump_hash(0, 10) == 0 and jump_hash(0, 10**6) == 0
    assert [jump_hash(k, 1000) for k in (1, 42, 123456789, 2**63)] == [549, 571, 294, 453]
    for k in range(2000):
        prev = jump_hash(k, 1)
        for n in range(2, 40):
            cur = jump_hash(k, n)
            assert 0 <= cur < n
            assert cur == prev or cur == n - 1, (k, n, prev, cur)
            prev = cur
    counts = [0] * 10
    for k in range(50000):
        counts[jump_hash(ring_hash(f"obj-{k}"), 10)] += 1
    assert max(counts) / min(counts) < 1.1, counts
    assert jump_hash(2**64 + 5, 100) == jump_hash(5, 100)    # masked to 64 bits

    print("all consistent hashing tests passed")


if __name__ == "__main__":
    _run_tests()
