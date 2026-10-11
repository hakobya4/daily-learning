"""
Day 20, Task 3 -- Python: group shifted strings.

THE PROBLEM
------------
Two lowercase strings belong to the same group if one can be turned into
the other by shifting every letter by the same amount (wrapping z -> a).
"abc", "bcd" and "xyz" are one group; "az" and "ba" are another (gap -25
== +1 mod 26).

group_shifted(strings) returns a list of groups. Inside each group the
strings are sorted; the groups themselves are sorted by their first
string.

  ["abc","bcd","acef","xyz","az","ba","a","z"]
  -> [["a","z"], ["abc","bcd","xyz"], ["acef"], ["az","ba"]]

Raise ValueError if strings is not a list.

HOW TO WORK THROUGH THIS
-------------------------
Build a canonical key from the differences between consecutive letters
(mod 26), then group with a dict.

Run: python3 group_shifted_strings.py
"""


def group_shifted(strings: list) -> list:
    if not isinstance(strings, list):
        raise ValueError("strings must be a list")
    groups = {}
    for w in strings:
        key = tuple((ord(w[i + 1]) - ord(w[i])) % 26 for i in range(len(w) - 1))
        groups.setdefault((len(w), key), []).append(w)
    result = [sorted(g) for g in groups.values()]
    result.sort(key=lambda g: g[0])
    return result


def _run_tests():
    assert group_shifted(["abc", "bcd", "acef", "xyz", "az", "ba", "a", "z"]) == [
        ["a", "z"], ["abc", "bcd", "xyz"], ["acef"], ["az", "ba"]]
    assert group_shifted([]) == []
    assert group_shifted(["a"]) == [["a"]]
    assert group_shifted(["ab", "ab"]) == [["ab", "ab"]]
    assert group_shifted(["abc", "abd"]) == [["abc"], ["abd"]]
    try:
        group_shifted("abc")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
