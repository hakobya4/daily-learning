"""
Day 13, Task 7 -- CS fundamentals: longest increasing subsequence.

THE PROBLEM
------------
lis_length(nums): length of the longest STRICTLY increasing subsequence
(elements need not be adjacent).
    [10, 9, 2, 5, 3, 7, 101, 18]  ->  4   (e.g. 2, 3, 7, 18)

lis(nums): return one actual longest subsequence as a list. If several
exist, return the one that ends earliest in the input (the first one
found when scanning with the standard "predecessor index" DP, taking
the first best end index). The tests only check length, strict
increase and that it is a real subsequence, so any valid answer passes.

Do the O(n^2) DP first, then try the O(n log n) "tails" version with
bisect for lis_length.

Run: python3 lis.py
"""


def lis_length(nums: list[int]) -> int:
    raise NotImplementedError


def lis(nums: list[int]) -> list[int]:
    raise NotImplementedError


def _is_subsequence(sub, seq) -> bool:
    it = iter(seq)
    return all(x in it for x in sub)


def _run_tests() -> None:
    assert lis_length([]) == 0
    assert lis_length([7]) == 1
    assert lis_length([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert lis_length([0, 1, 0, 3, 2, 3]) == 4
    assert lis_length([7, 7, 7, 7]) == 1          # strictly increasing
    assert lis_length([5, 4, 3, 2, 1]) == 1
    assert lis_length(list(range(50))) == 50
    assert lis([]) == []
    import random
    random.seed(7)
    for _ in range(200):
        a = [random.randint(0, 15) for _ in range(random.randint(0, 14))]
        s = lis(a)
        assert len(s) == lis_length(a), a
        assert all(x < y for x, y in zip(s, s[1:])), (a, s)
        assert _is_subsequence(s, a), (a, s)
    print("All lis tests passed.")


if __name__ == "__main__":
    _run_tests()
