"""
Day 47, Task 10 -- CS fundamentals: alien dictionary (topological sort).

THE PROBLEM
------------
words is a list of words sorted lexicographically by the rules of an unknown
alphabet. alien_order(words) returns a string containing every letter that
appears, in an order consistent with the list, or "" if no valid order exists
(a cycle, or a longer word listed before its own prefix, e.g. ["abc", "ab"]).
If several orders are valid, any one is accepted.
Hint: compare adjacent words, the first differing letters give an edge a -> b;
then Kahn's algorithm (in-degree queue) or DFS with 3 colors.

Run: python3 alien_order.py
"""


def alien_order(words):
    raise NotImplementedError


def _is_valid(words, order):
    letters = set("".join(words))
    if sorted(order) != sorted(letters):
        return False
    rank = {ch: i for i, ch in enumerate(order)}
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:
                if rank[x] > rank[y]:
                    return False
                break
        else:
            if len(a) > len(b):
                return False
    return True


def _run_tests():
    assert alien_order(["wrt", "wrf", "er", "ett", "rftt"]) == "wertf"
    assert alien_order(["z", "x"]) == "zx"
    assert alien_order(["z", "x", "z"]) == ""
    assert alien_order(["abc", "ab"]) == ""
    assert alien_order(["z", "z"]) == "z"
    assert alien_order(["ba", "bc", "ac", "cab"]) == "bac"
    w = ["abc"]
    assert _is_valid(w, alien_order(w))
    w = ["ab", "ac", "bc"]
    assert _is_valid(w, alien_order(w))
    assert alien_order([]) == ""
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
