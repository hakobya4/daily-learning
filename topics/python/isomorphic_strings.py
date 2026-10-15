"""
Day 25, Task 2 -- Python: isomorphic strings.

THE PROBLEM
------------
is_isomorphic(s, t) returns True if the characters of s can be replaced
(consistently, one-to-one) to get t. Every occurrence of a character must
map to the same character, and no two different characters may map to the
same one. Strings of different lengths are never isomorphic.

  is_isomorphic("egg", "add")   -> True
  is_isomorphic("foo", "bar")   -> False   (o would need to be a AND r)
  is_isomorphic("badc", "baba") -> False   (b and d would both have to map to b)

HOW TO WORK THROUGH THIS
-------------------------
Keep two dicts (s->t and t->s) and check both directions as you scan, or
compare the "first-seen index" pattern of both strings.

Run: python3 isomorphic_strings.py
"""


def is_isomorphic(s: str, t: str) -> bool:
    raise NotImplementedError


def _run_tests():
    assert is_isomorphic("egg", "add") is True
    assert is_isomorphic("foo", "bar") is False
    assert is_isomorphic("paper", "title") is True
    assert is_isomorphic("badc", "baba") is False
    assert is_isomorphic("ab", "aa") is False
    assert is_isomorphic("aa", "ab") is False
    assert is_isomorphic("", "") is True
    assert is_isomorphic("abc", "ab") is False
    assert is_isomorphic("a", "a") is True
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
