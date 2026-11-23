"""
Day 63, Task 7 -- CS fundamentals: a gap buffer (the data structure behind Emacs' text
buffers) with cursor movement, amortised O(1) typing, and undo/redo.

THE PROBLEM
------------
Store the text in ONE Python list `self.buf` of single characters with a "gap" of unused
slots at the cursor:   buf = [h, e, l, l, o, _, _, _, _, w, o, r, l, d]
                                         ^gap_start    ^gap_end (exclusive)
Text = buf[:gap_start] + buf[gap_end:], and the cursor sits at gap_start.
Typing at the cursor fills the gap (O(1)); moving the cursor shifts characters across the
gap (cost proportional to the distance moved); when the gap is full, grow the list
(at least double the total capacity) so typing stays amortised O(1).
You may NOT keep the text in a str or a second list and rebuild it -- the gap is the point.

class GapBuffer(text="", capacity=16)
  The buffer starts with `text` in it and the cursor at the END of the text; the initial
  capacity is `capacity`, or len(text) + 16 if that is larger (but at least 1).
  Attributes the tests look at:
    self.buf          the backing list (len(self.buf) == capacity)
    self.gap_start, self.gap_end
    self.moves        number of characters copied ACROSS the gap by cursor moves
                      (NOT counting copies made while growing). Moving the cursor by d
                      positions must add exactly d to self.moves.
  Methods:
    cursor -> int (property)            position 0..len(text)
    __len__()                           length of the text (not the capacity)
    text() -> str                       the whole text (build it only when asked)
    gap_size() -> int
    move_to(pos)                        absolute move; clamp pos to [0, len]
    left(n=1), right(n=1)               relative moves, clamped
    insert(s)                           insert string s at the cursor; cursor ends AFTER s
    backspace(n=1) -> str               delete up to n chars BEFORE the cursor, return them
                                        (in text order)
    delete(n=1) -> str                  delete up to n chars AFTER the cursor, return them
    undo() -> bool / redo() -> bool     see below; return False if there is nothing to do

  Undo/redo rules:
    - every insert / backspace / delete call that changed the text is ONE undo step
      (calls that removed nothing, or inserted "", are not recorded);
    - undo() reverts the most recent step: the text is restored and the cursor goes to
      where it was just BEFORE that step;
    - redo() re-applies the most recently undone step; the cursor goes to where it was
      just AFTER that step;
    - any new recorded edit clears the redo history; cursor moves do not.
  Record the minimal info per step (kind, position, the string inserted or removed) --
  NOT a full copy of the text.

Growth: if s does not fit in the gap, allocate new capacity = max(2 * capacity,
len(text) + len(s) + 16) and copy, keeping the gap at the cursor.

Run: python3 gap_buffer_editor.py
"""


class GapBuffer:
    def __init__(self, text="", capacity=16):
        cap = max(capacity, len(text) + 16, 1)
        self.buf = [None] * cap
        n = len(text)
        self.buf[:n] = list(text)
        self.gap_start = n
        self.gap_end = cap
        self.moves = 0
        self._undo = []   # (kind, pos, s) with kind in {"ins", "bs", "del"}
        self._redo = []

    # ---- basic queries ----
    @property
    def cursor(self):
        return self.gap_start

    def __len__(self):
        return len(self.buf) - (self.gap_end - self.gap_start)

    def text(self):
        return "".join(self.buf[:self.gap_start]) + "".join(self.buf[self.gap_end:])

    def gap_size(self):
        return self.gap_end - self.gap_start

    # ---- cursor movement ----
    def move_to(self, pos):
        pos = max(0, min(pos, len(self)))
        gs, ge = self.gap_start, self.gap_end
        if pos < gs:
            d = gs - pos
            self.buf[ge - d:ge] = self.buf[pos:gs]
            self.gap_start, self.gap_end = pos, ge - d
            self.moves += d
        elif pos > gs:
            d = pos - gs
            self.buf[gs:gs + d] = self.buf[ge:ge + d]
            self.gap_start, self.gap_end = gs + d, ge + d
            self.moves += d

    def left(self, n=1):
        self.move_to(self.cursor - max(0, n))

    def right(self, n=1):
        self.move_to(self.cursor + max(0, n))

    # ---- raw edits (no undo bookkeeping) ----
    def _grow(self, need):
        cap = len(self.buf)
        new_cap = max(2 * cap, len(self) + need + 16)
        tail = self.buf[self.gap_end:]
        new = self.buf[:self.gap_start] + [None] * (new_cap - self.gap_start - len(tail)) + tail
        self.buf = new
        self.gap_end = new_cap - len(tail)

    def _insert_here(self, s):
        if len(s) > self.gap_size():
            self._grow(len(s))
        gs = self.gap_start
        self.buf[gs:gs + len(s)] = list(s)
        self.gap_start = gs + len(s)

    def _delete_after(self, n):
        n = max(0, min(n, len(self.buf) - self.gap_end))
        ge = self.gap_end
        out = "".join(self.buf[ge:ge + n])
        self.buf[ge:ge + n] = [None] * n
        self.gap_end = ge + n
        return out

    def _delete_before(self, n):
        n = max(0, min(n, self.gap_start))
        gs = self.gap_start
        out = "".join(self.buf[gs - n:gs])
        self.buf[gs - n:gs] = [None] * n
        self.gap_start = gs - n
        return out

    def _record(self, step):
        self._undo.append(step)
        self._redo.clear()

    # ---- public edits ----
    def insert(self, s):
        if not s:
            return
        pos = self.cursor
        self._insert_here(s)
        self._record(("ins", pos, s))

    def backspace(self, n=1):
        out = self._delete_before(n)
        if out:
            self._record(("bs", self.cursor, out))
        return out

    def delete(self, n=1):
        out = self._delete_after(n)
        if out:
            self._record(("del", self.cursor, out))
        return out

    def undo(self):
        if not self._undo:
            return False
        kind, pos, s = step = self._undo.pop()
        if kind == "ins":
            self.move_to(pos)
            self._delete_after(len(s))          # cursor before = pos
        elif kind == "bs":
            self.move_to(pos)
            self._insert_here(s)                # cursor before = pos + len(s)
        else:  # "del"
            self.move_to(pos)
            self._insert_here(s)
            self.move_to(pos)                   # cursor before = pos
        self._redo.append(step)
        return True

    def redo(self):
        if not self._redo:
            return False
        kind, pos, s = step = self._redo.pop()
        self.move_to(pos)
        if kind == "ins":
            self._insert_here(s)                # cursor after = pos + len(s)
        else:
            self._delete_after(len(s))          # cursor after = pos
        self._undo.append(step)
        return True


def _run_tests():
    import random
    import time

    g = GapBuffer()
    assert g.text() == "" and len(g) == 0 and g.cursor == 0
    g.insert("hello")
    assert g.text() == "hello" and g.cursor == 5 and len(g) == 5
    assert len(g.buf) == 16 and g.gap_size() == 11
    g.insert(" world")
    g.move_to(5)
    g.insert(",")
    assert g.text() == "hello, world" and g.cursor == 6
    assert g.backspace() == ","
    assert g.text() == "hello world" and g.cursor == 5
    assert g.delete(100) == " world" and g.text() == "hello"
    assert g.delete() == "" and g.backspace(0) == ""
    g.left(2)
    assert g.cursor == 3
    assert g.backspace(10) == "hel" and g.text() == "lo" and g.cursor == 0
    g.left(5)
    assert g.cursor == 0
    g.right(99)
    assert g.cursor == 2
    g.move_to(-4)
    assert g.cursor == 0
    g.move_to(1000)
    assert g.cursor == 2

    # initial text: cursor at the END of it
    g = GapBuffer("abc")
    assert g.text() == "abc" and g.cursor == 3 and len(g.buf) >= 16

    # move cost accounting: moving by d copies exactly d characters across the gap
    g = GapBuffer("x" * 1000)
    m0 = g.moves
    g.move_to(0)
    assert g.moves - m0 == 1000
    g.move_to(10)
    g.move_to(4)
    assert g.moves - m0 == 1016
    g.move_to(4)
    assert g.moves - m0 == 1016

    # growth keeps the content and the gap at the cursor, and at least doubles
    g = GapBuffer(capacity=4)
    g.insert("ab")
    g.insert("cdefg")
    assert g.text() == "abcdefg" and g.cursor == 7 and len(g.buf) >= 8
    g.move_to(3)
    cap = len(g.buf)
    g.insert("X" * (g.gap_size() + 1))
    assert len(g.buf) >= 2 * cap
    assert g.text() == "abc" + "X" * (cap - 7 + 1) + "defg"

    # undo / redo
    g = GapBuffer()
    g.insert("hello")              # step 1
    g.insert(" world")             # step 2
    g.move_to(0)
    g.delete(1)                    # step 3: "ello world"
    g.move_to(4)
    g.backspace(2)                 # step 4: "el world"
    g.backspace(0)                 # not recorded
    g.delete(0)                    # not recorded
    assert g.text() == "el world" and g.cursor == 2
    assert g.undo() and g.text() == "ello world" and g.cursor == 4
    assert g.undo() and g.text() == "hello world" and g.cursor == 0
    assert g.redo() and g.text() == "ello world" and g.cursor == 0
    assert g.undo() and g.undo() and g.text() == "hello" and g.cursor == 5
    assert g.undo() and g.text() == "" and g.cursor == 0
    assert not g.undo()
    assert g.redo() and g.text() == "hello" and g.cursor == 5
    g.move_to(0)                   # cursor moves keep the redo history
    assert g.redo() and g.text() == "hello world" and g.cursor == 11
    assert g.undo() and g.undo()
    g.insert("X")                  # new edit clears redo history
    assert g.text() == "X" and not g.redo()

    # differential test against a plain Python string model, including undo/redo
    rng = random.Random(63)
    g = GapBuffer(capacity=1)
    model, cur = "", 0
    undo, redo = [], []
    for step in range(20000):
        op = rng.randrange(8)
        if op == 0:
            s = "".join(rng.choice("abcxyz \n") for _ in range(rng.randrange(0, 6)))
            g.insert(s)
            if s:
                undo.append((model, cur, model[:cur] + s + model[cur:], cur + len(s)))
                redo.clear()
                model, cur = undo[-1][2], undo[-1][3]
        elif op == 1:
            n = rng.randrange(0, 4)
            got = g.backspace(n)
            k = min(n, cur)
            assert got == model[cur - k:cur]
            if k:
                undo.append((model, cur, model[:cur - k] + model[cur:], cur - k))
                redo.clear()
                model, cur = undo[-1][2], undo[-1][3]
        elif op == 2:
            n = rng.randrange(0, 4)
            got = g.delete(n)
            assert got == model[cur:cur + n]
            if got:
                undo.append((model, cur, model[:cur] + model[cur + n:], cur))
                redo.clear()
                model, cur = undo[-1][2], undo[-1][3]
        elif op == 3:
            pos = rng.randrange(-2, len(model) + 3)
            g.move_to(pos)
            cur = max(0, min(pos, len(model)))
        elif op == 4:
            n = rng.randrange(0, 5)
            g.left(n)
            cur = max(0, cur - n)
        elif op == 5:
            n = rng.randrange(0, 5)
            g.right(n)
            cur = min(len(model), cur + n)
        elif op == 6:
            ok = g.undo()
            assert ok == bool(undo)
            if undo:
                before, bcur, after, acur = undo.pop()
                redo.append((before, bcur, after, acur))
                model, cur = before, bcur
        else:
            ok = g.redo()
            assert ok == bool(redo)
            if redo:
                before, bcur, after, acur = redo.pop()
                undo.append((before, bcur, after, acur))
                model, cur = after, acur
        assert g.cursor == cur and len(g) == len(model), step
        if step % 97 == 0:
            assert g.text() == model, step
    assert g.text() == model

    # amortised O(1) typing: 200k single-character inserts in the middle
    g = GapBuffer("start|end")
    g.move_to(6)
    t0 = time.perf_counter()
    for i in range(200000):
        g.insert("k")
    assert time.perf_counter() - t0 < 3.0, "inserts are not amortised O(1)"
    assert len(g) == 200009 and g.cursor == 200006
    assert g.text().startswith("start|k") and g.text().endswith("kend")

    print("all gap buffer tests passed")


if __name__ == "__main__":
    _run_tests()
