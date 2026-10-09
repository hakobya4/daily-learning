"""
Day 18, Task 2 -- Python: partition labels.

THE PROBLEM
------------
Split string s into as many parts as possible so that each letter appears
in at most one part. Return the list of part sizes, in order.

  "ababcbacadefegdehijhklij" -> [9, 7, 8]
  "eccbbbbdec"               -> [10]
  ""                         -> []

Raise ValueError if s is not a str.

HOW TO WORK THROUGH THIS
-------------------------
Record the last index of each char, then sweep: extend the current part's
end to max(last[c]); when i reaches the end, cut.

Run: python3 partition_labels.py
"""


def partition_labels(s: str) -> list:
    if not isinstance(s, str):
        raise ValueError("s must be a str")
    last = {c: i for i, c in enumerate(s)}
    sizes, start, end = [], 0, 0
    for i, c in enumerate(s):
        end = max(end, last[c])
        if i == end:
            sizes.append(i - start + 1)
            start = i + 1
    return sizes


def _run_tests():
    assert partition_labels("ababcbacadefegdehijhklij") == [9, 7, 8]
    assert partition_labels("eccbbbbdec") == [10]
    assert partition_labels("a") == [1]
    assert partition_labels("abc") == [1, 1, 1]
    assert partition_labels("aaabbb") == [3, 3]
    assert partition_labels("") == []
    for bad in (None, 5, ["a"]):
        try:
            partition_labels(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for %r" % (bad,))
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
