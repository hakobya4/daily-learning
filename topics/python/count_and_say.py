"""
Day 21, Task 4 -- Python: count-and-say.

THE PROBLEM
------------
The count-and-say sequence: term 1 is "1"; each next term describes the
previous one by reading its runs of equal digits aloud.

  1 -> "1"
  2 -> "11"      (one 1)
  3 -> "21"      (two 1s)
  4 -> "1211"    (one 2, one 1)
  5 -> "111221"
  6 -> "312211"

Return the n-th term as a string. Raise ValueError if n < 1.

HOW TO WORK THROUGH THIS
-------------------------
Iterate n-1 times; each round, walk the string grouping equal neighbours
(itertools.groupby works) and emit f"{count}{digit}".

Run: python3 count_and_say.py
"""


def count_and_say(n: int) -> str:
    raise NotImplementedError


def _run_tests():
    expected = ["1", "11", "21", "1211", "111221", "312211", "13112221",
                "1113213211"]
    for i, e in enumerate(expected, start=1):
        assert count_and_say(i) == e, i
    assert len(count_and_say(20)) == 302
    try:
        count_and_say(0)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
