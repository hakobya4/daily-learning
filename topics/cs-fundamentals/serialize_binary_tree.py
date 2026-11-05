"""
Day 45, Task 10 -- CS fundamentals: serialize / deserialize a binary tree.

THE PROBLEM
------------
Implement serialize(root) -> str and deserialize(s) -> root so that
deserialize(serialize(t)) rebuilds a tree structurally equal to t (same
shape and values). Values are ints (may be negative); the empty tree is None.
Use any format (hint: preorder with a marker such as "#" for None, joined by
commas).

Run: python3 serialize_binary_tree.py
"""


class Node:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def serialize(root):
    out = []
    stack = [root]
    while stack:
        node = stack.pop()
        if node is None:
            out.append("#")
        else:
            out.append(str(node.val))
            stack.append(node.right)
            stack.append(node.left)
    return ",".join(out)


def deserialize(s):
    tokens = s.split(",")
    if not tokens or tokens[0] == "#":
        return None
    root = Node(int(tokens[0]))
    # stack of (node, next child slot to fill: 0=left, 1=right)
    stack = [[root, 0]]
    for tok in tokens[1:]:
        while stack and stack[-1][1] == 2:
            stack.pop()
        if not stack:
            break
        top = stack[-1]
        child = None if tok == "#" else Node(int(tok))
        if top[1] == 0:
            top[0].left = child
        else:
            top[0].right = child
        top[1] += 1
        if child is not None:
            stack.append([child, 0])
    return root


def same(a, b):
    if a is None or b is None:
        return a is b
    return a.val == b.val and same(a.left, b.left) and same(a.right, b.right)


def _run_tests():
    assert deserialize(serialize(None)) is None
    t1 = Node(1)
    assert same(deserialize(serialize(t1)), t1)
    t2 = Node(1, Node(2), Node(3, Node(4), Node(5)))
    assert same(deserialize(serialize(t2)), t2)
    t3 = Node(-1, None, Node(-20, Node(300), None))  # skewed, negatives
    assert same(deserialize(serialize(t3)), t3)
    d = None
    for v in range(1500):  # deep chain
        d = Node(v, d, None)
    assert same(deserialize(serialize(d)), d)
    assert isinstance(serialize(t2), str)
    print("all tests passed")


if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(10000)
    _run_tests()
