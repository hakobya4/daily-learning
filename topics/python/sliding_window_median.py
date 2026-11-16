"""
Day 57, Task 2 -- Python: sliding window median with two heaps and lazy deletion.

THE PROBLEM
------------
Given a list of integers `nums` and a window size k (1 <= k <= len(nums)), return the
list of medians of every contiguous window nums[i:i+k], for i = 0 .. len(nums) - k.
  * For odd k the median is the middle element (return it as a float).
  * For even k it is the mean of the two middle elements (a float, e.g. 2.5).
Return [] if nums is empty.

Example:
  sliding_median([1, 3, -1, -3, 5, 3, 6, 7], 3) -> [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]
  sliding_median([1, 2, 3, 4, 2, 3, 1, 4, 2], 4) -> [2.5, 2.5, 3.0, 2.5, 2.5, 2.5]
  sliding_median([5], 1)                        -> [5.0]

Hint: keep a max-heap `lo` (negated values) for the smaller half and a min-heap `hi`
for the larger half, with len(lo) == len(hi) or len(lo) == len(hi) + 1 counting only
VALID elements. Heaps cannot remove arbitrary items, so on leaving the window record
the outgoing value in a dict `delayed[value] += 1` and adjust a "balance" counter for
whichever side it logically belonged to; only physically pop a delayed value when it
reaches the TOP of a heap ("prune"). Rebalance after every insert/remove, then prune
both tops before reading the median. O(n log n) overall.
(Alternative: maintain a sorted list with bisect.insort / del -- O(n*k), accepted by the
small tests but too slow for the big one.)

Run: python3 sliding_window_median.py
"""


def sliding_median(nums, k):
    raise NotImplementedError


def _brute(nums, k):
    out = []
    for i in range(len(nums) - k + 1):
        w = sorted(nums[i:i + k])
        if k % 2:
            out.append(float(w[k // 2]))
        else:
            out.append((w[k // 2 - 1] + w[k // 2]) / 2)
    return out


def _run_tests():
    assert sliding_median([1, 3, -1, -3, 5, 3, 6, 7], 3) == [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]
    assert sliding_median([1, 2, 3, 4, 2, 3, 1, 4, 2], 4) == [2.5, 2.5, 3.0, 2.5, 2.5, 2.5]
    assert sliding_median([5], 1) == [5.0]
    assert sliding_median([], 1) == []
    assert sliding_median([2, 2, 2, 2], 2) == [2.0, 2.0, 2.0]
    assert sliding_median([2147483647, 2147483647], 2) == [2147483647.0]
    assert sliding_median([1, 4, 2, 3], 4) == [2.5]

    import random
    rng = random.Random(57)
    for _ in range(500):
        n = rng.randint(1, 30)
        nums = [rng.randint(-5, 5) for _ in range(n)]
        k = rng.randint(1, n)
        assert sliding_median(nums, k) == _brute(nums, k), (nums, k)

    # O(n log n): 200k elements, window 50k.
    import time
    big = [rng.randint(-10**9, 10**9) for _ in range(200_000)]
    t0 = time.time()
    res = sliding_median(big, 50_000)
    assert len(res) == 150_001
    assert res[0] == _brute(big[:50_000], 50_000)[0]
    assert res[-1] == _brute(big[-50_000:], 50_000)[0]
    assert time.time() - t0 < 10, "too slow -- use heaps, not a sorted list"
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
