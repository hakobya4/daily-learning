"""
Day 48, Task 10 -- CS fundamentals: skip list.

THE PROBLEM
------------
Implement class Skiplist (no built-in balanced tree / sorted container) with:
  add(num)      insert num; duplicates are allowed
  search(num)   -> True if num is present
  erase(num)    -> remove ONE occurrence, True if one was removed, else False
Use multiple levels of sorted linked lists; give each new node a random height
(p = 1/2, capped at ~16 levels). Expected O(log n) per operation.

Run: python3 skip_list.py
"""


class Skiplist:
    def __init__(self):
        raise NotImplementedError

    def add(self, num):
        raise NotImplementedError

    def search(self, num):
        raise NotImplementedError

    def erase(self, num):
        raise NotImplementedError


def _run_tests():
    import random
    s = Skiplist()
    s.add(1)
    s.add(2)
    s.add(3)
    assert s.search(0) is False
    s.add(4)
    assert s.search(1) is True
    assert s.erase(0) is False
    assert s.erase(1) is True
    assert s.search(1) is False
    s.add(5)
    s.add(5)
    assert s.erase(5) is True
    assert s.search(5) is True      # one copy left
    assert s.erase(5) is True
    assert s.search(5) is False
    assert s.erase(5) is False
    # randomized check against a plain multiset
    random.seed(48)
    ref = {}
    sk = Skiplist()
    for _ in range(3000):
        x = random.randint(0, 60)
        op = random.choice("ase")
        if op == "a":
            sk.add(x)
            ref[x] = ref.get(x, 0) + 1
        elif op == "s":
            assert sk.search(x) is (ref.get(x, 0) > 0)
        else:
            had = ref.get(x, 0) > 0
            assert sk.erase(x) is had
            if had:
                ref[x] -= 1
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
