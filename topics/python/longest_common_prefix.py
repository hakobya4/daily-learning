"""
Day 9, Task 3 -- Python: longest common prefix of a list of strings.

THE PROBLEM
------------
Write longest_common_prefix(strs: list[str]) -> str returning the
longest string that is a prefix of EVERY string in the list. Empty
list -> "". If nothing is shared -> "".

HOW TO WORK THROUGH THIS
-------------------------
Idea A: take the first string as a candidate and shorten it until every
other string startswith() it. Idea B: compare column by column with
zip(*strs). Either way, think about the empty-string and single-string
cases before coding.

Run: python3 longest_common_prefix.py
"""


def longest_common_prefix(strs: list[str]) -> str:
    raise NotImplementedError


def _run_tests() -> None:
    assert longest_common_prefix(["flower", "flow", "flight"]) == "fl"
    assert longest_common_prefix(["dog", "racecar", "car"]) == ""
    assert longest_common_prefix(["interview"]) == "interview"
    assert longest_common_prefix([]) == ""
    assert longest_common_prefix(["", "abc"]) == ""
    assert longest_common_prefix(["same", "same", "same"]) == "same"
    assert longest_common_prefix(["ab", "abc", "a"]) == "a"
    print("All longest_common_prefix tests passed.")


if __name__ == "__main__":
    _run_tests()
