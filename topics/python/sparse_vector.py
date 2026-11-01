"""
Day 42, Task 3 -- Python: sparse vector class.

THE PROBLEM
------------
Implement class SparseVector that stores only non-zero entries.
  SparseVector(values: list)       build from a dense list
  .dot(other) -> number            dot product; iterate the smaller one
  .add(other) -> SparseVector      element-wise sum (same length required,
                                   raise ValueError otherwise)
  .to_list() -> list               dense list again
  .nnz -> int                      number of stored non-zero entries
Zeros produced by add (e.g. 3 + -3) must NOT be stored.
len(v) is the dense length.

Run: python3 sparse_vector.py
"""


class SparseVector:
    def __init__(self, values):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    @property
    def nnz(self):
        raise NotImplementedError

    def dot(self, other):
        raise NotImplementedError

    def add(self, other):
        raise NotImplementedError

    def to_list(self):
        raise NotImplementedError


def _run_tests():
    a = SparseVector([1, 0, 0, 2, 3])
    b = SparseVector([0, 3, 0, 4, 0])
    assert len(a) == 5 and a.nnz == 3 and b.nnz == 2
    assert a.dot(b) == 8
    assert b.dot(a) == 8
    assert a.add(b).to_list() == [1, 3, 0, 6, 3]
    c = SparseVector([0, 0, 0, 0, 0])
    assert c.nnz == 0 and a.dot(c) == 0
    d = SparseVector([-1, 0, 0, -2, -3])
    s = a.add(d)
    assert s.nnz == 0 and s.to_list() == [0, 0, 0, 0, 0]
    try:
        a.add(SparseVector([1, 2]))
        assert False, "expected ValueError"
    except ValueError:
        pass
    assert SparseVector([]).to_list() == []
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
