"""
Day 39, Task 8 -- CS fundamentals: merge accounts (union-find).

THE PROBLEM
------------
accounts is a list of [name, email1, email2, ...]. Two accounts belong to the
same person if they share at least one email (names alone prove nothing, and
two different people may share a name). Merge them. Return a list of
[name, sorted unique emails...], one per person, in any order.

  [["John","a@m","b@m"], ["John","a@m","c@m"], ["Mary","m@m"], ["John","j@m"]]
  -> [["John","a@m","b@m","c@m"], ["John","j@m"], ["Mary","m@m"]]

HOW TO WORK THROUGH THIS
-------------------------
Union-find over account indexes: map each email to the first account index
that owned it; when seen again, union the two indexes. Afterwards group
emails by root, sort them, and prepend the name. Near O(N log N).

Run: python3 accounts_merge.py
"""


def accounts_merge(accounts: list) -> list:
    parent = list(range(len(accounts)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    owner = {}
    for i, acc in enumerate(accounts):
        for email in acc[1:]:
            if email in owner:
                ra, rb = find(owner[email]), find(i)
                if ra != rb:
                    parent[rb] = ra
            else:
                owner[email] = i
    groups = {}
    for email, i in owner.items():
        groups.setdefault(find(i), set()).add(email)
    return [[accounts[r][0]] + sorted(emails) for r, emails in groups.items()]


def _norm(result):
    return sorted(result)


def _run_tests():
    got = accounts_merge(
        [["John", "a@m", "b@m"], ["John", "a@m", "c@m"], ["Mary", "m@m"], ["John", "j@m"]]
    )
    assert _norm(got) == [
        ["John", "a@m", "b@m", "c@m"],
        ["John", "j@m"],
        ["Mary", "m@m"],
    ]
    # transitive chain: 0-1 share x, 1-2 share y
    got = accounts_merge([["A", "x"], ["A", "x", "y"], ["A", "y", "z"], ["B", "q"]])
    assert _norm(got) == [["A", "x", "y", "z"], ["B", "q"]]
    # same name, no shared email -> stay separate
    got = accounts_merge([["Sam", "s1"], ["Sam", "s2"]])
    assert _norm(got) == [["Sam", "s1"], ["Sam", "s2"]]
    # duplicate emails inside one account
    got = accounts_merge([["Z", "e", "e", "d"]])
    assert _norm(got) == [["Z", "d", "e"]]
    assert accounts_merge([]) == []
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
