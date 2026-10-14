"""
Day 23, Task 4 -- Python: Conway's Game of Life, one step.

THE PROBLEM
------------
board is a list of lists of 0 (dead) / 1 (alive). Return the NEXT
generation as a NEW board (do not mutate the input). Rules, using the 8
neighbours (cells outside the board count as dead):

  * live cell with < 2 or > 3 live neighbours dies
  * live cell with 2 or 3 live neighbours survives
  * dead cell with exactly 3 live neighbours becomes alive

  game_of_life([[0,1,0],[0,1,0],[0,1,0]]) == [[0,0,0],[1,1,1],[0,0,0]]

An empty board returns []. Raise ValueError if rows differ in length.

Run: python3 game_of_life.py
"""


def game_of_life(board: list) -> list:
    if not board:
        return []
    width = len(board[0])
    if any(len(row) != width for row in board):
        raise ValueError("rows differ in length")
    height = len(board)
    result = [[0] * width for _ in range(height)]
    for r in range(height):
        for c in range(width):
            live = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < height and 0 <= cc < width:
                        live += board[rr][cc]
            if board[r][c]:
                result[r][c] = 1 if live in (2, 3) else 0
            else:
                result[r][c] = 1 if live == 3 else 0
    return result


def _run_tests():
    blinker = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
    assert game_of_life(blinker) == [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
    assert blinker == [[0, 1, 0], [0, 1, 0], [0, 1, 0]]  # not mutated
    block = [[1, 1], [1, 1]]
    assert game_of_life(block) == block
    glider = [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]
    assert game_of_life(glider) == [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]
    assert game_of_life([]) == []
    assert game_of_life([[1]]) == [[0]]
    assert game_of_life([[0, 0], [0, 0]]) == [[0, 0], [0, 0]]
    try:
        game_of_life([[1, 0], [1]])
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
    print("all tests passed")


if __name__ == "__main__":
    _run_tests()
