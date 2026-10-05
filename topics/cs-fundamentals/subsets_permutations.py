"""
Day 14, Task 7 -- CS fundamentals: backtracking (subsets, permutations,
combination sum).

THE PROBLEM
------------
Do NOT import itertools. Use recursive backtracking.

1. subsets(items) -> list of lists. All subsets of a list of distinct
   items, ordered by size first, then by position of the picked items
   (the same order as itertools.combinations for r = 0, 1, 2, ...).
       subsets([1, 2, 3]) -> [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]

2. permutations(items) -> list of lists. All orderings of distinct
   items, in the order produced by "pick the earliest unused item
   first" (the same order as itertools.permutations).
       permutations([1, 2, 3]) -> [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

3. combination_sum(candidates, target) -> list of lists. All unique
   combinations of candidates (positive ints, distinct values) that sum
   to target; each candidate may be used any number of times. Each
   combination is non-decreasing; return the combinations sorted.
       combination_sum([2, 3, 6, 7], 7) -> [[2, 2, 3], [7]]

HOW TO WORK THROUGH THIS
-------------------------
choose -> explore -> un-choose. Pass the current path and a start index
(or a "used" array for permutations) down the recursion.

Run: python3 subsets_permutations.py
"""


def subsets(items: list) -> list[list]:
    result: list[list] = []
    n = len(items)

    def backtrack(start: int, path: list, size: int) -> None:
        if len(path) == size:
            result.append(path[:])
            return
        for i in range(start, n):
            path.append(items[i])
            backtrack(i + 1, path, size)
            path.pop()

    for size in range(n + 1):
        backtrack(0, [], size)
    return result


def permutations(items: list) -> list[list]:
    result: list[list] = []
    n = len(items)
    used = [False] * n

    def backtrack(path: list) -> None:
        if len(path) == n:
            result.append(path[:])
            return
        for i in range(n):
            if used[i]:
                continue
            used[i] = True
            path.append(items[i])
            backtrack(path)
            path.pop()
            used[i] = False

    backtrack([])
    return result


def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    cands = sorted(candidates)
    result: list[list[int]] = []

    def backtrack(start: int, remaining: int, path: list[int]) -> None:
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(cands)):
            c = cands[i]
            if c > remaining:
                break
            path.append(c)
            backtrack(i, remaining - c, path)
            path.pop()

    backtrack(0, target, [])
    return sorted(result)


def _run_tests() -> None:
    import itertools
    assert subsets([]) == [[]]
    assert subsets([1, 2, 3]) == [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]
    assert permutations([]) == [[]]
    assert permutations([1, 2, 3]) == [
        [1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    for n in range(0, 6):
        items = list(range(n))
        want_s = [list(c) for r in range(n + 1) for c in itertools.combinations(items, r)]
        assert subsets(items) == want_s, n
        want_p = [list(p) for p in itertools.permutations(items)]
        assert permutations(items) == want_p, n
    assert combination_sum([2, 3, 6, 7], 7) == [[2, 2, 3], [7]]
    assert combination_sum([2, 3, 5], 8) == [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
    assert combination_sum([2], 1) == []
    assert combination_sum([7, 3, 2], 7) == [[2, 2, 3], [7]]
    print("All subsets_permutations tests passed.")


if __name__ == "__main__":
    _run_tests()
