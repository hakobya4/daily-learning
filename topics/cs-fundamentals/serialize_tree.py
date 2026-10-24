"""
Day 33, Task 10 -- CS fundamentals: serialize / deserialize a binary tree.

THE PROBLEM
------------
A binary tree is a nested tuple (value, left, right) where left/right are
again trees or None, and value is an int. An empty tree is None.

Implement:
  serialize(tree)  -> str   preorder, values joined by ',', None as '#'
  deserialize(s)   -> tree  the exact inverse

  serialize((1, (2, None, None), (3, (4, None, None), None)))
      == "1,2,#,#,3,4,#,#,#"
  serialize(None) == "#"
  deserialize(serialize(t)) == t   for every tree t (including negatives)

HOW TO WORK THROUGH THIS
-------------------------
Preorder with explicit null markers is enough to rebuild a unique tree.
In deserialize, split on ',' and consume tokens with an iterator (or an
index) in a recursive helper: read a token, '#' -> None, otherwise build
(int(token), recurse left, recurse right). Mind deep trees: a chain of
1000 nodes must not blow the recursion limit unless you raise it knowingly
(or write it iteratively).

Run: python3 serialize_tree.py
"""


def serialize(tree) -> str:
    out = []
    stack = [tree]
    while stack:
        node = stack.pop()
        if node is None:
            out.append("#")
        else:
            out.append(str(node[0]))
            stack.append(node[2])
            stack.append(node[1])
    return ",".join(out)


def deserialize(s: str):
    import sys
    sys.setrecursionlimit(max(sys.getrecursionlimit(), 10000))
    tokens = iter(s.split(","))

    def build():
        tok = next(tokens)
        if tok == "#":
            return None
        left = build()
        right = build()
        return (int(tok), left, right)

    return build()


def _run_tests():
    t = (1, (2, None, None), (3, (4, None, None), None))
    assert serialize(t) == "1,2,#,#,3,4,#,#,#"
    assert serialize(None) == "#"
    assert serialize((7, None, None)) == "7,#,#"
    assert deserialize("#") is None
    assert deserialize("7,#,#") == (7, None, None)
    assert deserialize(serialize(t)) == t
    neg = (-5, (-10, None, (0, None, None)), None)
    assert deserialize(serialize(neg)) == neg
    assert serialize((1, None, (2, None, (3, None, None)))) == "1,#,2,#,3,#,#"
    chain = None
    for v in range(500):
        chain = (v, chain, None)
    assert deserialize(serialize(chain)) == chain
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
