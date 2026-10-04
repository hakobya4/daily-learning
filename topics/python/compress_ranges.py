"""
Day 13, Task 3 -- Python: compress sorted integers into ranges.

THE PROBLEM
------------
Implement compress_ranges(nums) -> str. Given integers (any order,
duplicates allowed) return a comma-separated string where runs of
consecutive values collapse to "lo-hi" and singletons stay as is:

    [1, 2, 3, 5, 7, 8, 9]  ->  "1-3,5,7-9"
    [4, 4, 5]               ->  "4-5"
    []                      ->  ""

Two consecutive numbers form a range ("1-2"), not "1,2".
Negative numbers work: [-2, -1, 0] -> "-2-0".

Also implement expand_ranges(s) -> list[int], the inverse
("1-3,5" -> [1, 2, 3, 5]); it must parse negatives ("-2-0" -> [-2,-1,0]).
Use a regex like r"^(-?\\d+)(?:-(-?\\d+))?$" per piece.

Run: python3 compress_ranges.py
"""


def compress_ranges(nums: list[int]) -> str:
    vals = sorted(set(nums))
    parts = []
    i = 0
    while i < len(vals):
        j = i
        while j + 1 < len(vals) and vals[j + 1] == vals[j] + 1:
            j += 1
        parts.append(str(vals[i]) if i == j else f"{vals[i]}-{vals[j]}")
        i = j + 1
    return ",".join(parts)


def expand_ranges(s: str) -> list[int]:
    import re
    if not s:
        return []
    out: list[int] = []
    for piece in s.split(","):
        m = re.match(r"^(-?\d+)(?:-(-?\d+))?$", piece)
        if not m:
            raise ValueError(f"bad range piece {piece!r}")
        lo = int(m.group(1))
        hi = int(m.group(2)) if m.group(2) is not None else lo
        out.extend(range(lo, hi + 1))
    return out


def _run_tests() -> None:
    assert compress_ranges([]) == ""
    assert compress_ranges([5]) == "5"
    assert compress_ranges([1, 2, 3, 5, 7, 8, 9]) == "1-3,5,7-9"
    assert compress_ranges([9, 7, 8, 1, 3, 2, 5]) == "1-3,5,7-9"
    assert compress_ranges([4, 4, 5]) == "4-5"
    assert compress_ranges([-2, -1, 0, 3]) == "-2-0,3"
    assert compress_ranges([1, 3, 5]) == "1,3,5"
    assert expand_ranges("") == []
    assert expand_ranges("1-3,5,7-9") == [1, 2, 3, 5, 7, 8, 9]
    assert expand_ranges("-2-0,3") == [-2, -1, 0, 3]
    data = [-5, -4, 0, 1, 2, 10, 12, 13]
    assert expand_ranges(compress_ranges(data)) == data
    print("All compress_ranges tests passed.")


if __name__ == "__main__":
    _run_tests()
