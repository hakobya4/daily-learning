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
    MAX_LEVEL = 16

    class _Node:
        __slots__ = ("val", "next")

        def __init__(self, val, height):
            self.val = val
            self.next = [None] * height

    def __init__(self):
        import random
        self._rand = random.random
        self.head = Skiplist._Node(None, self.MAX_LEVEL)

    def _random_height(self):
        h = 1
        while h < self.MAX_LEVEL and self._rand() < 0.5:
            h += 1
        return h

    def _find_preds(self, num):
        preds = [None] * self.MAX_LEVEL
        cur = self.head
        for lvl in range(self.MAX_LEVEL - 1, -1, -1):
            while cur.next[lvl] is not None and cur.next[lvl].val < num:
                cur = cur.next[lvl]
            preds[lvl] = cur
        return preds

    def add(self, num):
        preds = self._find_preds(num)
        node = Skiplist._Node(num, self._random_height())
        for lvl in range(len(node.next)):
            node.next[lvl] = preds[lvl].next[lvl]
            preds[lvl].next[lvl] = node

    def search(self, num):
        cand = self._find_preds(num)[0].next[0]
        return cand is not None and cand.val == num

    def erase(self, num):
        preds = self._find_preds(num)
        target = preds[0].next[0]
        if target is None or target.val != num:
            return False
        for lvl in range(len(target.next)):
            if preds[lvl].next[lvl] is target:
                preds[lvl].next[lvl] = target.next[lvl]
        return True


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
