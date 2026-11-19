"""
Day 59, Task 2 -- Python: a minimal line diff and unified-diff hunks (no difflib).

THE PROBLEM
------------
Implement two functions WITHOUT importing difflib.

diff_ops(a, b) -> list of (tag, line)
    a and b are lists of strings (lines without "\\n"). Return an edit script where tag
    is " " (line kept), "-" (line only in a) or "+" (line only in b) such that:
      * reading the " " and "-" lines in order gives back a, and the " " and "+" lines
        give back b;
      * it is MINIMAL: the number of " " lines equals the length of a longest common
        subsequence of a and b (so #"-" + #"+" is as small as possible);
      * inside every maximal run of changed lines, all "-" lines come before all "+"
        lines (like git/GNU diff print them).
    When several minimal scripts exist, any of them is accepted by the tests.

unified(a, b, n=3) -> list of str
    The hunks of a unified diff with n lines of context, WITHOUT the "---"/"+++" file
    header lines: each hunk is a header "@@ -A +B @@" followed by its lines, each
    prefixed with " ", "-" or "+". Rules (same as GNU diff / difflib):
      * every changed line is shown with up to n unchanged lines before and after it;
        two changes whose separating run of unchanged lines has length <= 2*n go in the
        SAME hunk (the context would touch or overlap), otherwise in separate hunks;
      * a range is "start,length" with 1-based start; when length == 1 print just
        "start"; when length == 0 print "start,0" where start is the line BEFORE the
        empty range (so "-0,0" for an insertion at the top);
      * identical inputs -> [] (no hunks).

Example:
  unified(list("abcdefghij"), list("abcXefghij"))
    -> ["@@ -1,7 +1,7 @@", " a", " b", " c", "-d", "+X", " e", " f", " g"]
  unified(["a", "b", "c"], ["a", "b", "c", "d"], n=1) -> ["@@ -3 +3,2 @@", " c", "+d"]

Hint: classic O(len(a)*len(b)) LCS table filled from the END (L[i][j] = LCS of a[i:]
and b[j:]); walk forward from (0, 0): equal lines -> " ", otherwise step in the
direction that keeps the larger L. Then reorder each change block (-'s first). For
unified(): remember each op's (line_in_a, line_in_b) position, group change indices
by the 2*n gap rule, and slice [first_change - n, last_change + n] per group.

Run: python3 unified_diff_hunks.py
"""


def diff_ops(a, b):
    na, nb = len(a), len(b)
    # L[i][j] = LCS length of a[i:] and b[j:]
    L = [[0] * (nb + 1) for _ in range(na + 1)]
    for i in range(na - 1, -1, -1):
        row, nxt = L[i], L[i + 1]
        for j in range(nb - 1, -1, -1):
            if a[i] == b[j]:
                row[j] = nxt[j + 1] + 1
            else:
                row[j] = max(nxt[j], row[j + 1])
    raw = []
    i = j = 0
    while i < na and j < nb:
        if a[i] == b[j] and L[i][j] == L[i + 1][j + 1] + 1:
            raw.append((" ", a[i]))
            i += 1
            j += 1
        elif L[i + 1][j] >= L[i][j + 1]:
            raw.append(("-", a[i]))
            i += 1
        else:
            raw.append(("+", b[j]))
            j += 1
    raw += [("-", x) for x in a[i:]]
    raw += [("+", y) for y in b[j:]]
    # Reorder each maximal change block: all "-" before all "+".
    ops, block = [], []

    def flush():
        ops.extend(o for o in block if o[0] == "-")
        ops.extend(o for o in block if o[0] == "+")
        block.clear()

    for op in raw:
        if op[0] == " ":
            flush()
            ops.append(op)
        else:
            block.append(op)
    flush()
    return ops


def unified(a, b, n=3):
    ops = diff_ops(a, b)
    # Position (index into a, index into b) at which each op starts.
    pos, ia, ib = [], 0, 0
    for t, _ in ops:
        pos.append((ia, ib))
        if t in " -":
            ia += 1
        if t in " +":
            ib += 1
    changes = [k for k, (t, _) in enumerate(ops) if t != " "]
    if not changes:
        return []
    groups = [[changes[0], changes[0]]]
    for k in changes[1:]:
        if k - groups[-1][1] - 1 <= 2 * n:
            groups[-1][1] = k
        else:
            groups.append([k, k])

    def rng(start0, length):
        if length == 0:
            return "%d,0" % start0
        if length == 1:
            return "%d" % (start0 + 1)
        return "%d,%d" % (start0 + 1, length)

    out = []
    for first, last in groups:
        lo = max(0, first - n)
        hi = min(len(ops) - 1, last + n)
        chunk = ops[lo:hi + 1]
        a0, b0 = pos[lo]
        alen = sum(1 for t, _ in chunk if t in " -")
        blen = sum(1 for t, _ in chunk if t in " +")
        out.append("@@ -%s +%s @@" % (rng(a0, alen), rng(b0, blen)))
        out += [t + line for t, line in chunk]
    return out


def _lcs(a, b):
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b):
            cur.append(prev[j] + 1 if x == y else max(prev[j + 1], cur[j]))
        prev = cur
    return prev[-1]


def _check_ops(a, b, ops):
    assert [l for t, l in ops if t in " -"] == a, (a, b, ops)
    assert [l for t, l in ops if t in " +"] == b, (a, b, ops)
    assert all(t in " -+" for t, _ in ops)
    assert sum(1 for t, _ in ops if t == " ") == _lcs(a, b), (a, b, ops)
    for k in range(1, len(ops)):
        assert not (ops[k - 1][0] == "+" and ops[k][0] == "-"), ("'+' before '-'", ops)


def _apply(a, hunks):
    # Apply hunks (as produced by unified) to a; checks the context lines too.
    out, i, k = [], 0, 0
    while k < len(hunks):
        head = hunks[k]
        assert head.startswith("@@ -") and head.endswith(" @@"), head
        old = head[4:head.index(" +")]
        start = int(old.split(",")[0])
        length = int(old.split(",")[1]) if "," in old else 1
        start0 = start if length == 0 else start - 1
        out += a[i:start0]
        i = start0
        k += 1
        while k < len(hunks) and not hunks[k].startswith("@@"):
            t, line = hunks[k][0], hunks[k][1:]
            if t in " -":
                assert a[i] == line, ("context mismatch", a[i], line)
                i += 1
            if t in " +":
                out.append(line)
            k += 1
    return out + a[i:]


def _run_tests():
    import random

    for a, b in [([], []), (["x"], []), ([], ["x"]), (list("abc"), list("abc")),
                 (list("abcabba"), list("cbabac")), (list("ABCDEF"), list("FEDCBA"))]:
        _check_ops(a, b, diff_ops(a, b))

    assert unified(list("abcdefghij"), list("abcXefghij")) == \
        ["@@ -1,7 +1,7 @@", " a", " b", " c", "-d", "+X", " e", " f", " g"]
    assert unified(["a", "b", "c"], ["a", "b", "c", "d"], n=1) == ["@@ -3 +3,2 @@", " c", "+d"]
    assert unified(list("abc"), []) == ["@@ -1,3 +0,0 @@", "-a", "-b", "-c"]
    assert unified([], ["x", "y"]) == ["@@ -0,0 +1,2 @@", "+x", "+y"]
    assert unified(["x", "a", "b"], ["a", "b"], n=0) == ["@@ -1 +0,0 @@", "-x"]
    assert unified(list("abc"), list("abc")) == []
    a16, b16 = list("abcdefghijklmnop"), list("aBcdefghijklmnoP")
    assert unified(a16, b16, n=2) == ["@@ -1,4 +1,4 @@", " a", "-b", "+B", " c", " d",
                                      "@@ -14,3 +14,3 @@", " n", " o", "-p", "+P"]
    assert unified(a16, b16, n=5)[0] == "@@ -1,7 +1,7 @@"
    assert len([h for h in unified(a16, b16, n=7) if h.startswith("@@")]) == 1  # gap 13 <= 14

    rng = random.Random(59)
    for _ in range(400):
        a = [rng.choice("abcd") for _ in range(rng.randint(0, 12))]
        b = [rng.choice("abcd") for _ in range(rng.randint(0, 12))]
        ops = diff_ops(a, b)
        _check_ops(a, b, ops)
        n = rng.randint(0, 3)
        hunks = unified(a, b, n)
        assert _apply(a, hunks) == b, (a, b, n, hunks)
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
