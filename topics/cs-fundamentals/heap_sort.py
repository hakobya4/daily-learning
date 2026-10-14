"""
Day 23, Task 10 -- CS fundamentals: heap sort.

THE PROBLEM
------------
Implement heap_sort(items) returning a NEW ascending list (input is not
mutated). Build a max-heap in place on a copy, then repeatedly swap the
root to the end and sift down. You must write the sift-down yourself:
no sorted(), list.sort(), or heapq.

  heap_sort([5, 2, 9, 1, 5, 6]) == [1, 2, 5, 5, 6, 9]

O(n log n) worst case, O(1) extra space beyond the copy.

HOW TO WORK THROUGH THIS
-------------------------
Children of i are 2i+1 and 2i+2. Heapify by sifting down from index
n//2 - 1 back to 0. Then for end from n-1 down to 1: swap a[0], a[end],
sift down a[0] within a[:end].

Run: python3 heap_sort.py
"""


def heap_sort(items: list) -> list:
    a = list(items)
    n = len(a)

    def sift_down(i, size):
        while True:
            left = 2 * i + 1
            right = left + 1
            largest = i
            if left < size and a[left] > a[largest]:
                largest = left
            if right < size and a[right] > a[largest]:
                largest = right
            if largest == i:
                return
            a[i], a[largest] = a[largest], a[i]
            i = largest

    for i in range(n // 2 - 1, -1, -1):
        sift_down(i, n)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift_down(0, end)
    return a


def _run_tests():
    import random
    assert heap_sort([5, 2, 9, 1, 5, 6]) == [1, 2, 5, 5, 6, 9]
    assert heap_sort([]) == []
    assert heap_sort([1]) == [1]
    orig = [3, 1, 2]
    assert heap_sort(orig) == [1, 2, 3]
    assert orig == [3, 1, 2]
    assert heap_sort([2, 2, 2]) == [2, 2, 2]
    assert heap_sort(["b", "a", "c"]) == ["a", "b", "c"]
    rng = random.Random(7)
    for _ in range(200):
        data = [rng.randint(-50, 50) for _ in range(rng.randint(0, 60))]
        assert heap_sort(data) == sorted(data)
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
