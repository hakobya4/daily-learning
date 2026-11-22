"""
Day 62, Task 7 -- CS fundamentals: DFA simulation, reachability, and minimization
(Moore / Hopcroft partition refinement), plus an equivalence check.

THE PROBLEM
------------
A DFA here is a dict:
    {
      "alphabet": ["0", "1"],          # list of single-character symbols
      "start": "A",
      "accept": {"C", "E"},            # set of accepting states
      "delta": {("A", "0"): "B", ("A", "1"): "C", ...},
    }
delta may be PARTIAL: a missing (state, symbol) means "go to an implicit dead state"
(a non-accepting sink). States can be any hashable values.

1) accepts(dfa, word) -> bool
   Run the DFA; a missing transition rejects immediately. A symbol not in the
   alphabet also rejects.

2) reachable_states(dfa) -> set
   States reachable from start (BFS). Do not include the implicit dead state.

3) minimize(dfa) -> new DFA (same dict shape) with the MINIMUM number of states:
     a) drop unreachable states;
     b) complete the DFA by adding an explicit dead state if any transition is
        missing (use a fresh object as its name, e.g. a unique sentinel);
     c) refine the partition {accepting, non-accepting} until stable -- two states
        stay together only if, for every symbol, their successors lie in the same
        block (Moore), or use Hopcroft's worklist algorithm for O(n k log n);
     d) build the quotient DFA. Name each new state by the frozenset of original
        states it contains. After minimization there is at most ONE block from
        which no accepting state can be reached (the "dead" block -- it contains
        your sentinel if you added one). Drop that block together with every
        transition into it, so the result is partial again. The new start is the
        block containing the old start -- if THAT block is the dead one (the
        language is empty), return a DFA whose only state is a non-accepting
        start state frozenset(), with accept == set() and delta == {}.
     The original state names inside the frozensets must NOT include your
     dead-state sentinel.

4) equivalent(d1, d2) -> bool
   True if both accept the same language (same alphabet assumed). Do it with a BFS
   over pairs of states (product construction): the languages differ iff some
   reachable pair has exactly one accepting component. Treat missing transitions as
   the dead state on either side.

Run: python3 dfa_minimize.py
"""

from itertools import product


def accepts(dfa, word):
    state = dfa["start"]
    alphabet = set(dfa["alphabet"])
    for ch in word:
        if ch not in alphabet:
            return False
        key = (state, ch)
        if key not in dfa["delta"]:
            return False
        state = dfa["delta"][key]
    return state in dfa["accept"]


def reachable_states(dfa):
    from collections import deque
    seen = {dfa["start"]}
    queue = deque([dfa["start"]])
    while queue:
        s = queue.popleft()
        for a in dfa["alphabet"]:
            nxt = dfa["delta"].get((s, a))
            if nxt is not None and nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen


def minimize(dfa):
    alphabet = list(dfa["alphabet"])
    states = reachable_states(dfa)
    DEAD = object()                                    # unique sentinel
    delta = {}
    need_dead = False
    for s in states:
        for a in alphabet:
            nxt = dfa["delta"].get((s, a))
            if nxt is None:
                nxt, need_dead = DEAD, True
            delta[(s, a)] = nxt
    all_states = set(states)
    if need_dead:
        all_states.add(DEAD)
        for a in alphabet:
            delta[(DEAD, a)] = DEAD
    accept = {s for s in states if s in dfa["accept"]}

    # Moore refinement: block id per state, refine by signature until stable
    block = {s: (1 if s in accept else 0) for s in all_states}
    while True:
        sigs = {}
        new_block = {}
        for s in all_states:
            sig = (block[s],) + tuple(block[delta[(s, a)]] for a in alphabet)
            new_block[s] = sigs.setdefault(sig, len(sigs))
        if len(sigs) == len(set(block.values())):
            break
        block = new_block
    block = new_block

    groups = {}
    for s in all_states:
        groups.setdefault(block[s], set()).add(s)

    # live blocks: those from which an accepting block is reachable
    preds = {b: set() for b in groups}
    for (s, a), t in delta.items():
        preds[block[t]].add(block[s])
    live = {block[s] for s in accept}
    stack = list(live)
    while stack:
        b = stack.pop()
        for p in preds[b]:
            if p not in live:
                live.add(p)
                stack.append(p)

    start_block = block[dfa["start"]]
    if start_block not in live:
        return {"alphabet": alphabet, "start": frozenset(), "accept": set(), "delta": {}}

    name = {b: frozenset(x for x in groups[b] if x is not DEAD) for b in groups if b in live}
    new_delta = {}
    for b in name:
        rep = next(iter(groups[b]))
        for a in alphabet:
            tb = block[delta[(rep, a)]]
            if tb in live:
                new_delta[(name[b], a)] = name[tb]
    new_accept = {name[b] for b in name if groups[b] & accept}
    return {"alphabet": alphabet, "start": name[start_block], "accept": new_accept, "delta": new_delta}


def equivalent(d1, d2):
    from collections import deque
    DEAD = object()
    alphabet = list(dict.fromkeys(list(d1["alphabet"]) + list(d2["alphabet"])))

    def step(d, s, a):
        if s is DEAD:
            return DEAD
        return d["delta"].get((s, a), DEAD)

    def acc(d, s):
        return s is not DEAD and s in d["accept"]

    start = (d1["start"], d2["start"])
    seen = {start}
    queue = deque([start])
    while queue:
        p, q = queue.popleft()
        if acc(d1, p) != acc(d2, q):
            return False
        for a in alphabet:
            pair = (step(d1, p, a), step(d2, q, a))
            if pair not in seen:
                seen.add(pair)
                queue.append(pair)
    return True


def _all_words(alphabet, max_len):
    for n in range(max_len + 1):
        for tup in product(alphabet, repeat=n):
            yield "".join(tup)


def _mod3_dfa():
    # binary numbers divisible by 3, with redundant duplicate states and an unreachable one
    d = {}
    names = {0: ["r0", "r0b"], 1: ["r1", "r1b"], 2: ["r2", "r2b"]}
    for r in range(3):
        for i, s in enumerate(names[r]):
            for bit in "01":
                nr = (2 * r + int(bit)) % 3
                d[(s, bit)] = names[nr][(i + int(bit)) % 2]
    d[("orphan", "0")] = "r0"
    return {"alphabet": ["0", "1"], "start": "r0", "accept": {"r0", "r0b", "orphan"}, "delta": d}


def _run_tests():
    ends_ab = {
        "alphabet": ["a", "b"], "start": 0, "accept": {2},
        "delta": {(0, "a"): 1, (0, "b"): 0, (1, "a"): 1, (1, "b"): 2, (2, "a"): 1, (2, "b"): 0},
    }
    assert accepts(ends_ab, "ab") and accepts(ends_ab, "bbaab")
    assert not accepts(ends_ab, "") and not accepts(ends_ab, "aba")
    assert not accepts(ends_ab, "abc")                         # c not in alphabet

    m3 = _mod3_dfa()
    assert reachable_states(m3) == {"r0", "r0b", "r1", "r1b", "r2", "r2b"}
    mm = minimize(m3)
    assert len(reachable_states(mm)) == 3, reachable_states(mm)
    assert mm["start"] == frozenset({"r0", "r0b"})
    for w in _all_words("01", 10):
        assert accepts(mm, w) == accepts(m3, w) == (w == "" or int(w, 2) % 3 == 0), w
    assert equivalent(m3, mm)

    # partial DFA for a*b (one b at the end); missing transitions = dead
    a_star_b = {"alphabet": ["a", "b"], "start": "s", "accept": {"t"},
                "delta": {("s", "a"): "s", ("s", "b"): "t"}}
    mab = minimize(a_star_b)
    assert len(reachable_states(mab)) == 2
    assert all(isinstance(s, frozenset) for s in reachable_states(mab))
    assert all(len(s) > 0 for s in reachable_states(mab))      # no dead block kept
    for w in _all_words("ab", 7):
        assert accepts(mab, w) == accepts(a_star_b, w), w

    # language "contains aa" built wastefully: 6 states -> 3
    contains_aa = {"alphabet": ["a", "b"], "start": "q0", "accept": {"q2", "q3", "q4"},
                   "delta": {("q0", "a"): "q1", ("q0", "b"): "q5", ("q5", "a"): "q1", ("q5", "b"): "q0",
                             ("q1", "a"): "q2", ("q1", "b"): "q0", ("q2", "a"): "q3", ("q2", "b"): "q4",
                             ("q3", "a"): "q2", ("q3", "b"): "q4", ("q4", "a"): "q4", ("q4", "b"): "q3"}}
    mca = minimize(contains_aa)
    assert len(reachable_states(mca)) == 3
    assert mca["start"] == frozenset({"q0", "q5"})
    assert frozenset({"q2", "q3", "q4"}) in mca["accept"]

    # empty language: accepting state unreachable
    empty = {"alphabet": ["x"], "start": 1, "accept": {9}, "delta": {(1, "x"): 2, (2, "x"): 1}}
    me = minimize(empty)
    assert me["start"] == frozenset() and me["accept"] == set() and me["delta"] == {}
    assert not any(accepts(me, w) for w in _all_words("x", 6))

    assert equivalent(contains_aa, mca) and equivalent(empty, me)
    assert not equivalent(ends_ab, contains_aa)
    assert not equivalent(a_star_b, {"alphabet": ["a", "b"], "start": "s", "accept": {"t"},
                                     "delta": {("s", "a"): "s", ("s", "b"): "t", ("t", "b"): "t"}})

    # minimization is idempotent and canonical in size
    assert len(reachable_states(minimize(mm))) == 3
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
