"""
Day 8, Task 3 -- Python: three-sum (sorted two-pointer technique).

THE PROBLEM
------------
Write three_sum(nums: list[int]) -> list[list[int]] that returns every
UNIQUE triplet [a, b, c] from `nums` (a <= b <= c) whose values sum to
zero. No duplicate triplets in the output, even if `nums` has repeated
values. If no such triplet exists, return an empty list.

This builds on Day 2's two_sum (still open -- go clear that one first
if you haven't) but needs a different technique: hashing one target
value doesn't scale cleanly to three numbers, so this one leans on
SORTING plus a two-pointer sweep instead.

HOW TO WORK THROUGH THIS
-------------------------
1. Sort `nums` first. Sorting is what makes both the two-pointer sweep
   AND the duplicate-skipping possible.
2. Fix one number at a time as the smallest of the triplet: for i in
   range(len(nums) - 2), treat nums[i] as that anchor.
3. For the remaining two numbers, use two pointers -- l starting right
   after i, r starting at the end of the list. While l < r: if
   nums[i] + nums[l] + nums[r] == 0, you found a triplet; if it's less
   than 0, the sum is too small so move l rightward (bigger value); if
   it's more than 0, move r leftward (smaller value).
4. Duplicates: after fixing a triplet, skip past any repeated value at
   both l and r before continuing (nums[l] == nums[l-1], etc.) -- and
   skip a repeated anchor value at the top of the i loop too
   (nums[i] == nums[i-1]), so the same triplet isn't found twice.

Run: python3 three_sum.py
"""


def three_sum(nums: list[int]) -> list[list[int]]:
    # TODO: sort nums, then for each anchor index i, run the
    # two-pointer sweep described above, skipping duplicates at every
    # level (anchor, left pointer, right pointer).
    raise NotImplementedError


def _run_tests() -> None:
    # classic case: sorted nums are [-4, -1, -1, 0, 1, 2]
    result = three_sum([-1, 0, 1, 2, -1, -4])
    assert result == [[-1, -1, 2], [-1, 0, 1]], result

    # all zeros -- only one unique triplet, not four
    assert three_sum([0, 0, 0, 0]) == [[0, 0, 0]]

    # no valid triplet at all
    assert three_sum([1, 2, -2, -1]) == []
    assert three_sum([]) == []
    assert three_sum([0, 0]) == []  # fewer than 3 elements

    print("All three_sum tests passed.")


if __name__ == "__main__":
    _run_tests()
