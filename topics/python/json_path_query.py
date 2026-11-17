"""
Day 58, Task 2 -- Python: a tiny JSONPath evaluator (tokenizer + recursive descent).

THE PROBLEM
------------
Implement query(doc, path) -> list, evaluating a small subset of JSONPath against a
document made of dicts, lists and scalars (as produced by json.loads).

Path grammar (whitespace is NOT allowed anywhere):
  path     := "$" step*
  step     := "." NAME          child by key           ($.store.book)
            | "." "*"           all children           ($.store.*)
            | "[" INT "]"       list index, negative counts from the end  ($.a[0], $.a[-1])
            | "[" "*" "]"       all children           ($.a[*])
            | "[" "'" KEY "'" "]"  child by key that may contain dots/spaces ($['a.b'])
            | ".." NAME         recursive descent: every value stored under key NAME
                                at ANY depth below (and including) the current node
  NAME     := [A-Za-z_][A-Za-z0-9_]*
  INT      := -?[0-9]+
  KEY      := any characters except "'"

Semantics:
  * The result is a list of matched VALUES in document order (dict insertion order,
    list index order). "$" alone returns [doc].
  * "all children" of a dict = its values; of a list = its elements; of a scalar = none.
  * A key/index step on something that is not a dict/list, a missing key or an
    out-of-range index simply produces NO match (never an exception).
  * Recursive descent "..name" visits nodes in PRE-ORDER: for each node, first emit
    node[name] if the node is a dict that has that key, then descend into the node's
    children in order (so a value can be emitted and then searched inside too).
  * A malformed path (missing "$", bad NAME, unterminated bracket, "..*", trailing
    ".", empty brackets...) raises ValueError.

Example:
  doc = {"store": {"book": [{"title": "A", "price": 8}, {"title": "B", "price": 12}],
                   "bike": {"price": 20}}}
  query(doc, "$.store.book[*].title") -> ["A", "B"]
  query(doc, "$..price")              -> [8, 12, 20]
  query(doc, "$.store.book[-1]")      -> [{"title": "B", "price": 12}]
  query(doc, "$.store.car")           -> []

Hint: first TOKENIZE the path into steps like ("key", "store"), ("index", -1),
("wild",), ("descend", "price"), raising ValueError on anything unexpected. Then
evaluate step by step: current = [doc]; for each step, current = flat list of results
of applying the step to every node in current.

Run: python3 json_path_query.py
"""


def query(doc, path):
    raise NotImplementedError


def _run_tests():
    doc = {"store": {"book": [{"title": "A", "price": 8}, {"title": "B", "price": 12}],
                     "bike": {"price": 20}}}
    assert query(doc, "$.store.book[*].title") == ["A", "B"]
    assert query(doc, "$..price") == [8, 12, 20]
    assert query(doc, "$.store.book[-1]") == [{"title": "B", "price": 12}]
    assert query(doc, "$.store.car") == []
    assert query(doc, "$") == [doc]
    assert query(doc, "$.store.*") == [doc["store"]["book"], doc["store"]["bike"]]
    assert query(doc, "$.store.book[5]") == []
    assert query(doc, "$.store.book[-3]") == []
    assert query(doc, "$.store.book.title") == []          # key step on a list
    assert query(doc, "$.store.bike.price.x") == []        # key step on a scalar
    assert query(doc, "$.store.bike[0]") == []             # index step on a dict
    assert query(doc, "$.store.bike.price[*]") == []
    assert query(doc, "$..book[0].title") == ["A"]

    weird = {"a.b": {"c d": 1}, "x": [[1, 2], [3]]}
    assert query(weird, "$['a.b']['c d']") == [1]
    assert query(weird, "$.x[*][*]") == [1, 2, 3]
    assert query(weird, "$.x[*][0]") == [1, 3]
    assert query(weird, "$.x[-1][-1]") == [3]

    # pre-order recursive descent, values may contain the same key again
    nested = {"n": {"n": {"n": 3, "z": 0}, "v": 1}, "list": [{"n": 9}]}
    assert query(nested, "$..n") == [nested["n"], nested["n"]["n"], 3, 9]
    assert query(nested, "$..n..n") == [nested["n"]["n"], 3, 3]
    assert query(nested, "$..missing") == []
    assert query(5, "$..n") == []
    assert query([1, [2, {"k": "v"}]], "$..k") == ["v"]

    for bad in ["", "store", "$.", "$..", "$..*", "$.1abc", "$[", "$[]", "$[1",
                "$['a", "$[x]", "$. a", "$.a b", "$[--1]", "$.a..", "$['a'"]:
        try:
            query(doc, bad)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError for %r" % bad)
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
