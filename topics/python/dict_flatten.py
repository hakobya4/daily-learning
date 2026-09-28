"""
Day 7, Task 3 -- Python: flatten / unflatten nested dictionaries.

THE PROBLEM
------------
Write two functions:

  flatten(d: dict) -> dict
      Takes an arbitrarily nested dict and returns a single-level dict
      whose keys are the original nested keys joined with '.', e.g.
      {"a": {"b": 1, "c": {"d": 2}}} -> {"a.b": 1, "a.c.d": 2}.
      A value that is a dict gets recursed into; a value that is
      anything else (int, str, list, ...) is a LEAF and is not
      touched, even if it's a list containing dicts -- only recurse
      through dict values, nothing else.

  unflatten(d: dict) -> dict
      The exact inverse: given a single-level dict with dot-joined
      keys, rebuild the original nested structure.

For any nested dict `x` with no literal '.' inside any of its own
keys, unflatten(flatten(x)) == x should hold.

HOW TO WORK THROUGH THIS
-------------------------
flatten: recursive helper that carries the "prefix so far" -- for each
key/value pair, if the value is a dict, recurse with
prefix + key + "."; otherwise write prefix + key straight into the
result dict.

unflatten: for each dot-joined key, split it on '.' into parts, then
walk/create nested dicts one part at a time (setdefault is handy
here), placing the value at the final part.

Run: python3 dict_flatten.py
"""


def flatten(d: dict) -> dict:
    result = {}

    def _walk(current: dict, prefix: str) -> None:
        for key, value in current.items():
            full_key = f"{prefix}{key}"
            if isinstance(value, dict):
                _walk(value, f"{full_key}.")
            else:
                result[full_key] = value

    _walk(d, "")
    return result


def unflatten(d: dict) -> dict:
    result: dict = {}
    for compound_key, value in d.items():
        parts = compound_key.split(".")
        node = result
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = value
    return result


def _run_tests() -> None:
    nested = {"a": {"b": 1, "c": {"d": 2, "e": 3}}, "f": 4}
    flat = flatten(nested)
    assert flat == {"a.b": 1, "a.c.d": 2, "a.c.e": 3, "f": 4}, flat
    assert unflatten(flat) == nested, unflatten(flat)

    # a value that's a list (even one holding dicts) is a leaf -- it's
    # never recursed into, so it should come back untouched.
    with_list = {"a": [1, {"x": 2}], "b": {"c": "hi"}}
    flat2 = flatten(with_list)
    assert flat2 == {"a": [1, {"x": 2}], "b.c": "hi"}, flat2
    assert unflatten(flat2) == with_list, unflatten(flat2)

    # empty dict round-trips to itself
    assert flatten({}) == {}
    assert unflatten({}) == {}

    print("All dict_flatten tests passed.")


if __name__ == "__main__":
    _run_tests()
