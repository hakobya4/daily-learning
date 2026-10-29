"""
Day 38, Task 4 -- Python: merge sorted log streams lazily.

THE PROBLEM
------------
Each stream is an iterable of (timestamp:int, message:str) tuples already
sorted by timestamp. Write merge_streams(*streams) that returns a GENERATOR
yielding all tuples in global timestamp order. On equal timestamps, earlier
streams (by argument position) come first. Do NOT concatenate and sort, and
do NOT consume a stream further than needed (streams may be infinite).

  a = [(1,"a1"),(4,"a2")]; b = [(2,"b1"),(4,"b2")]
  list(merge_streams(a, b)) -> [(1,"a1"),(2,"b1"),(4,"a2"),(4,"b2")]

HOW TO WORK THROUGH THIS
-------------------------
Use a heap holding (timestamp, stream_index, message, iterator). Pop the
smallest, yield it, then push the next item of that same iterator.
(heapq.merge works too, but try the manual heap first.)

Run: python3 merge_log_streams.py
"""
import heapq
import itertools
import types


def merge_streams(*streams):
    heap = []
    for idx, stream in enumerate(streams):
        it = iter(stream)
        first = next(it, None)
        if first is not None:
            heap.append((first[0], idx, first[1], it))
    heapq.heapify(heap)
    while heap:
        ts, idx, msg, it = heapq.heappop(heap)
        yield (ts, msg)
        nxt = next(it, None)
        if nxt is not None:
            heapq.heappush(heap, (nxt[0], idx, nxt[1], it))


def _run_tests():
    a = [(1, "a1"), (4, "a2")]
    b = [(2, "b1"), (4, "b2")]
    out = merge_streams(a, b)
    assert isinstance(out, types.GeneratorType)
    assert list(out) == [(1, "a1"), (2, "b1"), (4, "a2"), (4, "b2")]
    assert list(merge_streams()) == []
    assert list(merge_streams([], [(1, "x")])) == [(1, "x")]
    assert list(merge_streams([(3, "p")], [(3, "q")], [(3, "r")])) == [(3, "p"), (3, "q"), (3, "r")]
    # infinite streams: only take what is needed
    evens = ((i, "e") for i in itertools.count(0, 2))
    odds = ((i, "o") for i in itertools.count(1, 2))
    first = list(itertools.islice(merge_streams(evens, odds), 6))
    assert [t for t, _ in first] == [0, 1, 2, 3, 4, 5]
    assert [m for _, m in first] == ["e", "o", "e", "o", "e", "o"]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
