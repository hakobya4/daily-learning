"""
Day 56, Task 1 -- Python: count of smaller numbers after self (merge sort or Fenwick tree).

THE PROBLEM
------------
Given a list of integers nums, return a list counts where counts[i] is the number of
indices j > i with nums[j] < nums[i] (STRICTLY smaller, to the right).

Also implement count_inversions_total(nums): the total number of pairs (i, j) with
i < j and nums[i] > nums[j]. (It is sum(count_smaller(nums)), but write it so it does
not need the per-index list -- or reuse your helper, your choice.)

Rules:
  * nums may contain negatives, duplicates and be empty.
  * Equal values do NOT count (strictly smaller only).
  * Must run in O(n log n): the tests include n = 100_000.

Example:
  count_smaller([5, 2, 6, 1])   -> [2, 1, 1, 0]
  count_smaller([-1, -1])       -> [0, 0]
  count_inversions_total([3, 1, 2]) -> 2

Hint (two classic approaches -- pick one, then try the other):
  (a) Merge sort over (value, original_index) pairs. While merging, when you take an
      element from the LEFT half, every element already taken from the RIGHT half is
      smaller and was originally to its right -- add that running count to its index.
  (b) Coordinate-compress the values to ranks 1..m, walk nums from RIGHT to LEFT, and
      for each value ask a Fenwick tree "how many ranks < mine have I seen?" before
      adding your own rank.

Run: python3 count_smaller_after_self.py
"""


def count_smaller(nums):
    # Fenwick tree over coordinate-compressed ranks, walking right to left.
    n = len(nums)
    if n == 0:
        return []
    ranks = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}
    m = len(ranks)
    tree = [0] * (m + 1)
    counts = [0] * n
    for i in range(n - 1, -1, -1):
        r = ranks[nums[i]]
        # query prefix sum of ranks < r
        k, total = r - 1, 0
        while k > 0:
            total += tree[k]
            k -= k & -k
        counts[i] = total
        k = r
        while k <= m:
            tree[k] += 1
            k += k & -k
    return counts


def count_inversions_total(nums):
    # Iterative-recursive merge sort counting strictly-greater-left pairs.
    def sort(a):
        if len(a) <= 1:
            return a, 0
        mid = len(a) // 2
        left, x = sort(a[:mid])
        right, y = sort(a[mid:])
        merged, inv = [], x + y
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
                inv += len(left) - i
        merged.extend(left[i:]); merged.extend(right[j:])
        return merged, inv
    return sort(list(nums))[1]


def _naive(nums):
    return [sum(1 for j in range(i + 1, len(nums)) if nums[j] < nums[i])
            for i in range(len(nums))]


def _run_tests():
    assert count_smaller([]) == []
    assert count_smaller([7]) == [0]
    assert count_smaller([5, 2, 6, 1]) == [2, 1, 1, 0]
    assert count_smaller([-1]) == [0]
    assert count_smaller([-1, -1]) == [0, 0]
    assert count_smaller([1, 2, 3, 4]) == [0, 0, 0, 0]
    assert count_smaller([4, 3, 2, 1]) == [3, 2, 1, 0]
    assert count_smaller([2, 0, 1, 2, 0]) == [3, 0, 1, 1, 0]

    assert count_inversions_total([]) == 0
    assert count_inversions_total([3, 1, 2]) == 2
    assert count_inversions_total([4, 3, 2, 1]) == 6
    assert count_inversions_total([1, 1, 1]) == 0

    import random
    rng = random.Random(56)
    for _ in range(300):
        nums = [rng.randint(-5, 5) for _ in range(rng.randint(0, 25))]
        expected = _naive(nums)
        assert count_smaller(nums) == expected, nums
        assert count_inversions_total(nums) == sum(expected), nums

    # Must be O(n log n).
    n = 100_000
    desc = list(range(n, 0, -1))
    res = count_smaller(desc)
    assert res[0] == n - 1 and res[-1] == 0 and res[n // 2] == n - n // 2 - 1
    assert count_inversions_total(desc) == n * (n - 1) // 2
    assert count_inversions_total(list(range(n))) == 0

    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
