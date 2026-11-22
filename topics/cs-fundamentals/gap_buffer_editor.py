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
        raise NotImplementedError

    @property
    def cursor(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def text(self):
        raise NotImplementedError

    def gap_size(self):
        raise NotImplementedError

    def move_to(self, pos):
        raise NotImplementedError

    def left(self, n=1):
        raise NotImplementedError

    def right(self, n=1):
        raise NotImplementedError

    def insert(self, s):
        raise NotImplementedError

    def backspace(self, n=1):
        raise NotImplementedError

    def delete(self, n=1):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError

    def redo(self):
        raise NotImplementedError


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
