"""
Day 3, Task 3 -- Python: group anagrams.

THE PROBLEM
------------
Write group_anagrams(words) that takes a list of lowercase strings and
returns a list of lists, where each inner list holds words that are
anagrams of each other (same letters, different order). Words within
a group and the groups themselves can be in any order -- the tests
below compare as sets of frozensets so ordering won't trip you up.

Example: group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
groups into something like [["eat","tea","ate"], ["tan","nat"], ["bat"]]

HOW TO WORK THROUGH THIS
-------------------------
The trick: two words are anagrams iff their SORTED letters are equal
("eat" and "tea" both sort to "aet"). Use that sorted string as a
dict key, mapping it to the list of original words that match it.

Run: python3 anagram_groups.py
"""


def group_anagrams(words: list[str]) -> list[list[str]]:
    groups: dict[str, list[str]] = {}
    for word in words:
        key = "".join(sorted(word))
        groups.setdefault(key, []).append(word)
    return list(groups.values())


def _run_tests() -> None:
    def as_set_of_frozensets(groups):
        return {frozenset(g) for g in groups}

    cases = [
        ([], []),
        (["eat", "tea", "tan", "ate", "nat", "bat"],
         [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]),
        (["abc", "cba", "bac", "xyz"], [["abc", "cba", "bac"], ["xyz"]]),
    ]
    for words, expected in cases:
        got = group_anagrams(words)
        assert as_set_of_frozensets(got) == as_set_of_frozensets(expected), (
            f"group_anagrams({words!r}) -> {got!r}, expected groups like {expected!r}"
        )
    print("All anagram_groups tests passed.")


if __name__ == "__main__":
    _run_tests()
