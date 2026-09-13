"""
Day 2, Task 5 -- CS fundamentals: two-sum (hash map lookup pattern).

THE PROBLEM
------------
Given a list of integers `nums` and an integer `target`, return the
indices (i, j) of the two numbers that add up to `target`. Assume
exactly one valid pair exists. Order of the returned tuple doesn't
matter, but i != j.

Do it in O(n) time, not the obvious O(n^2) double loop -- the trick is
a hash map: as you scan once, for each number check whether
(target - number) was already seen, and only THEN record the current
number. Recording before checking would let a number pair with itself.

HOW TO WORK THROUGH THIS
-------------------------
First write the O(n^2) brute-force version in your head (or on paper)
to make sure you understand the problem. Then implement the O(n)
hash-map version below -- that's the one that should actually ship.

Run: python3 two_sum.py
"""

def two_sum(nums: list[int], target: int) -> tuple[int, int]:
    # TODO: single pass, dict mapping value -> index seen so far.
    raise NotImplementedError


def _run_tests() -> None:
    cases = [
        ([2, 7, 11, 15], 9, {2, 7}),      # check by VALUES, not exact indices
        ([3, 2, 4], 6, {2, 4}),
        ([3, 3], 6, {3, 3}),
        ([-1, 0, 5, 8], 4, {-1, 5}),
    ]
    for nums, target, expected_values in cases:
        i, j = two_sum(nums, target)
        assert i != j, f"two_sum returned the same index twice: {i}"
        got_values = {nums[i], nums[j]}
        assert got_values == expected_values, (
            f"two_sum({nums!r}, {target!r}) -> indices {(i, j)!r} "
            f"(values {got_values!r}), expected values {expected_values!r}"
        )
    print("All two_sum tests passed.")


if __name__ == "__main__":
    _run_tests()
