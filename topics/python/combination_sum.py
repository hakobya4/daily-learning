"""
Day 31, Task 3 -- Python: combination sum (backtracking).

THE PROBLEM
------------
combination_sum(candidates, target) returns every UNIQUE combination of
numbers from candidates (distinct positive ints) that adds up to target.
Each number may be used any number of times. Each combination is a list in
ascending order; the outer list may be in any order (tests sort it).

  ([2,3,6,7], 7)  -> [[2,2,3], [7]]
  ([2,3,5], 8)    -> [[2,2,2,2], [2,3,3], [3,5]]
  ([2], 1)        -> []

HOW TO WORK THROUGH THIS
-------------------------
Sort the candidates, then recurse with (start_index, remaining, path).
Reusing the same number means recursing with the same start index; moving
on means start+1. Stop a loop early once candidate > remaining.

Run: python3 combination_sum.py
"""


def combination_sum(candidates: list, target: int) -> list:
    cands = sorted(set(candidates))
    result = []

    def backtrack(start, remaining, path):
        if remaining == 0:
            result.append(path[:])
            return
        for idx in range(start, len(cands)):
            c = cands[idx]
            if c > remaining:
                break
            path.append(c)
            backtrack(idx, remaining - c, path)
            path.pop()

    backtrack(0, target, [])
    return result


def _run_tests():
    assert sorted(combination_sum([2, 3, 6, 7], 7)) == [[2, 2, 3], [7]]
    assert sorted(combination_sum([2, 3, 5], 8)) == [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
    assert combination_sum([2], 1) == []
    assert combination_sum([1], 2) == [[1, 1]]
    assert combination_sum([], 5) == []
    assert sorted(combination_sum([7, 3, 2], 7)) == [[2, 2, 3], [7]]
    assert combination_sum([5], 5) == [[5]]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
