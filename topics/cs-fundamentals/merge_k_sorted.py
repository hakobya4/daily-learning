"""
Day 19, Task 9 -- CS fundamentals: merge k sorted lists with a heap.

THE PROBLEM
------------
Given a list of k individually sorted (ascending) lists of numbers, return
one sorted list with all the elements. Use a min-heap (heapq) holding one
candidate per list, so the time is O(N log k) -- do not just concatenate
and sort. Do not modify the input lists.

  [[1,4,5],[1,3,4],[2,6]] -> [1,1,2,3,4,4,5,6]

Raise ValueError if lists is not a list.

HOW TO WORK THROUGH THIS
-------------------------
Push (value, list_index, element_index) tuples; pop the smallest, then push
the next element from the same list if there is one.

Run: python3 merge_k_sorted.py
"""
import heapq  # noqa: F401  (you will want it)


def merge_k_sorted(lists: list) -> list:
    if not isinstance(lists, list):
        raise ValueError("lists must be a list")
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapq.heapify(heap)
    out = []
    while heap:
        value, i, j = heapq.heappop(heap)
        out.append(value)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return out


def _run_tests():
    assert merge_k_sorted([[1, 4, 5], [1, 3, 4], [2, 6]]) == [1, 1, 2, 3, 4, 4, 5, 6]
    assert merge_k_sorted([]) == []
    assert merge_k_sorted([[], []]) == []
    assert merge_k_sorted([[1], [0]]) == [0, 1]
    assert merge_k_sorted([[5, 6, 7]]) == [5, 6, 7]
    src = [[2, 3], [1]]
    merge_k_sorted(src)
    assert src == [[2, 3], [1]]
    try:
        merge_k_sorted("abc")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
