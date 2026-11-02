"""
Day 43, Task 1 -- Python: move zeroes in place.

THE PROBLEM
------------
move_zeroes(nums) moves every 0 in the list to the END, keeping the relative
order of the non-zero elements (stable). It must work IN PLACE (mutate the
list, return None), use O(1) extra space, and make a single pass of writes.
Hint: keep a write index for the next non-zero slot, then fill the tail.

Run: python3 move_zeroes.py
"""


def move_zeroes(nums):
    raise NotImplementedError


def _run_tests():
    a = [0, 1, 0, 3, 12]
    assert move_zeroes(a) is None
    assert a == [1, 3, 12, 0, 0]
    b = [0, 0, 0]
    move_zeroes(b)
    assert b == [0, 0, 0]
    c = [1, 2, 3]
    move_zeroes(c)
    assert c == [1, 2, 3]
    d = []
    move_zeroes(d)
    assert d == []
    e = [4, 0, 0, 5, 0, 6, 0]
    move_zeroes(e)
    assert e == [4, 5, 6, 0, 0, 0, 0]
    f = [0]
    move_zeroes(f)
    assert f == [0]
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
